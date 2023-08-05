#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from contextlib import contextmanager
from copy import copy
import json
import logging
import six
import time
from kazoo.client import KazooClient, KazooState
from kazoo import exceptions as kze
from kazoo.recipe.lock import Lock

from nodepool import exceptions as npe

# States:
# We are building this image but it is not ready for use.
BUILDING = 'building'
# The image is being uploaded.
UPLOADING = 'uploading'
# The image/upload is ready for use.
READY = 'ready'
# The image/upload should be deleted.
DELETING = 'deleting'
# The build failed.
FAILED = 'failed'

STATES = set([BUILDING, UPLOADING, READY, DELETING, FAILED])

class ZooKeeperConnectionConfig(object):
    '''
    Represents the connection parameters for a ZooKeeper server.
    '''

    def __eq__(self, other):
        if isinstance(other, ZooKeeperConnectionConfig):
            if other.__dict__ == self.__dict__:
                return True
        return False

    def __init__(self, host, port=2181, chroot=None):
        '''Initialize the ZooKeeperConnectionConfig object.

        :param str host: The hostname of the ZooKeeper server.
        :param int port: The port on which ZooKeeper is listening.
            Optional, default: 2181.
        :param str chroot: A chroot for this connection.  All
            ZooKeeper nodes will be underneath this root path.
            Optional, default: None.

        (one per server) defining the ZooKeeper cluster servers. Only
        the 'host' attribute is required.'.

        '''
        self.host = host
        self.port = port
        self.chroot = chroot or ''


def buildZooKeeperHosts(host_list):
    '''
    Build the ZK cluster host list for client connections.

    :param list host_list: A list of
        :py:class:`~nodepool.zk.ZooKeeperConnectionConfig` objects (one
        per server) defining the ZooKeeper cluster servers.
    '''
    if not isinstance(host_list, list):
        raise Exception("'host_list' must be a list")
    hosts = []
    for host_def in host_list:
        host = '%s:%s%s' % (host_def.host, host_def.port, host_def.chroot)
        hosts.append(host)
    return ",".join(hosts)


class ZooKeeperWatchEvent(object):
    '''
    Class representing a watch trigger event.

    This is mostly used to not pass the kazoo event object to the function
    registered by the caller and maintain a consistent API. Attributes of
    this object include::

        * `type` - Event type. E.g., CREATED/DELETED
        * `state` - Event state. E.g., CONNECTED
        * `path` - Event path. E.g., /nodepool/image/trusty/request-build
        * `image` - Image name this event is based on. E.g., trusty
    '''
    def __init__(self, e_type, e_state, e_path, image):
        self.type = e_type
        self.state = e_state
        self.path = e_path
        # Pass image name so callback func doesn't need to parse from the path
        self.image = image


class BaseBuilderModel(object):
    def __init__(self, o_id):
        if o_id:
            self.id = o_id
        self._state = None
        self.state_time = None
        self.stat = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, six.string_types):
            raise TypeError("'id' attribute must be a string type")
        self._id = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value not in STATES:
            raise TypeError("'%s' is not a valid state" % value)
        self._state = value
        self.state_time = time.time()

    def toDict(self):
        '''
        Convert a BaseBuilderModel object's attributes to a dictionary.
        '''
        d = {}
        d['state'] = self.state
        d['state_time'] = self.state_time
        return d

    def fromDict(self, d):
        '''
        Set base attributes based on the given dict.

        Unlike the derived classes, this should NOT return an object as it
        assumes self has already been instantiated.
        '''
        if 'state' in d:
            self.state = d['state']
        if 'state_time' in d:
            self.state_time = d['state_time']


class ImageBuild(BaseBuilderModel):
    '''
    Class representing a DIB image build within the ZooKeeper cluster.
    '''

    def __init__(self, build_id=None):
        super(ImageBuild, self).__init__(build_id)
        self._formats = []
        self.builder = None          # Builder hostname

    def __repr__(self):
        d = self.toDict()
        d['id'] = self.id
        d['stat'] = self.stat
        return '<ImageBuild %s>' % d

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, value):
        if not isinstance(value, list):
            raise TypeError("'formats' attribute must be a list type")
        self._formats = copy(value)

    def addFormat(self, fmt):
        self._formats.append(fmt)

    def toDict(self):
        '''
        Convert an ImageBuild object's attributes to a dictionary.
        '''
        d = super(ImageBuild, self).toDict()
        if self.builder is not None:
            d['builder'] = self.builder
        if len(self.formats):
            d['formats'] = ','.join(self.formats)
        return d

    @staticmethod
    def fromDict(d, o_id=None):
        '''
        Create an ImageBuild object from a dictionary.

        :param dict d: The dictionary.
        :param str o_id: The object ID.

        :returns: An initialized ImageBuild object.
        '''
        o = ImageBuild(o_id)
        super(ImageBuild, o).fromDict(d)
        o.builder = d.get('builder')
        # Only attempt the split on non-empty string
        if d.get('formats', ''):
            o.formats = d.get('formats', '').split(',')
        return o


class ImageUpload(BaseBuilderModel):
    '''
    Class representing a provider image upload within the ZooKeeper cluster.
    '''

    def __init__(self, build_id=None, provider_name=None, image_name=None,
                 upload_id=None):
        super(ImageUpload, self).__init__(upload_id)
        self.build_id = build_id
        self.provider_name = provider_name
        self.image_name = image_name
        self.external_id = None      # Provider ID of the image
        self.external_name = None    # Provider name of the image

    def __repr__(self):
        d = self.toDict()
        d['id'] = self.id
        d['build_id'] = self.build_id
        d['provider_name'] = self.provider_name
        d['image_name'] = self.image_name
        d['stat'] = self.stat
        return '<ImageUpload %s>' % d

    def __eq__(self, other):
        if isinstance(other, ImageUpload):
            return (self.id == other.id and
                    self.provider_name == other.provider_name and
                    self.build_id == other.build_id and
                    self.image_name == other.image_name)
        else:
            return False

    def toDict(self):
        '''
        Convert an ImageUpload object's attributes to a dictionary.
        '''
        d = super(ImageUpload, self).toDict()
        d['external_id'] = self.external_id
        d['external_name'] = self.external_name
        return d

    @staticmethod
    def fromDict(d, build_id, provider_name, image_name, upload_id):
        '''
        Create an ImageUpload object from a dictionary.

        :param dict d: The dictionary.
        :param str build_id: The build ID.
        :param str provider_name: The provider name.
        :param str image_name: The image name.
        :param str upload_id: The upload ID.

        :returns: An initialized ImageUpload object.
        '''
        o = ImageUpload(build_id, provider_name, image_name, upload_id)
        super(ImageUpload, o).fromDict(d)
        o.external_id = d.get('external_id')
        o.external_name = d.get('external_name')
        return o


class ZooKeeper(object):
    '''
    Class implementing the ZooKeeper interface.

    This class uses the facade design pattern to keep common interaction
    with the ZooKeeper API simple and consistent for the caller, and
    limits coupling between objects. It allows for more complex interactions
    by providing direct access to the client connection when needed (though
    that is discouraged). It also provides for a convenient entry point for
    testing only ZooKeeper interactions.

    Most API calls reference an image name only, as the path for the znode
    for that image is calculated automatically. And image names are assumed
    to be unique.
    '''

    log = logging.getLogger("nodepool.zk.ZooKeeper")

    IMAGE_ROOT = "/nodepool/images"

    def __init__(self):
        '''
        Initialize the ZooKeeper object.
        '''
        self.client = None
        self._became_lost = False

    #========================================================================
    # Private Methods
    #========================================================================

    def _imagePath(self, image):
        return "%s/%s" % (self.IMAGE_ROOT, image)

    def _imageBuildRequestPath(self, image):
        return "%s/request-build" % self._imagePath(image)

    def _imageBuildsPath(self, image):
        return "%s/builds" % self._imagePath(image)

    def _imageBuildLockPath(self, image):
        return "%s/lock" % self._imageBuildsPath(image)

    def _imageBuildNumberLockPath(self, image, build_number):
        return "%s/%s/lock" % (self._imageBuildsPath(image),
                               build_number)

    def _imageProviderPath(self, image, build_number):
        return "%s/%s/providers" % (self._imageBuildsPath(image),
                                    build_number)

    def _imageUploadPath(self, image, build_number, provider):
        return "%s/%s/providers/%s/images" % (self._imageBuildsPath(image),
                                              build_number,
                                              provider)

    def _imageUploadLockPath(self, image, build_number, provider):
        return "%s/lock" % self._imageUploadPath(image, build_number,
                                                 provider)

    def _dictToStr(self, data):
        return json.dumps(data)

    def _strToDict(self, data):
        return json.loads(data)

    def _getImageBuildLock(self, image, blocking=True, timeout=None):
        lock_path = self._imageBuildLockPath(image)
        try:
            lock = Lock(self.client, lock_path)
            have_lock = lock.acquire(blocking, timeout)
        except kze.LockTimeout:
            raise npe.TimeoutException(
                "Timeout trying to acquire lock %s" % lock_path)

        # If we aren't blocking, it's possible we didn't get the lock
        # because someone else has it.
        if not have_lock:
            raise npe.ZKLockException("Did not get lock on %s" % lock_path)

        return lock

    def _getImageBuildNumberLock(self, image, build_number,
                                 blocking=True, timeout=None):
        lock_path = self._imageBuildNumberLockPath(image, build_number)
        try:
            lock = Lock(self.client, lock_path)
            have_lock = lock.acquire(blocking, timeout)
        except kze.LockTimeout:
            raise npe.TimeoutException(
                "Timeout trying to acquire lock %s" % lock_path)

        # If we aren't blocking, it's possible we didn't get the lock
        # because someone else has it.
        if not have_lock:
            raise npe.ZKLockException("Did not get lock on %s" % lock_path)

        return lock

    def _getImageUploadLock(self, image, build_number, provider,
                            blocking=True, timeout=None):
        lock_path = self._imageUploadLockPath(image, build_number, provider)
        try:
            lock = Lock(self.client, lock_path)
            have_lock = lock.acquire(blocking, timeout)
        except kze.LockTimeout:
            raise npe.TimeoutException(
                "Timeout trying to acquire lock %s" % lock_path)

        # If we aren't blocking, it's possible we didn't get the lock
        # because someone else has it.
        if not have_lock:
            raise npe.ZKLockException("Did not get lock on %s" % lock_path)

        return lock

    def _connection_listener(self, state):
        '''
        Listener method for Kazoo connection state changes.

        .. warning:: This method must not block.
        '''
        if state == KazooState.LOST:
            self.log.debug("ZooKeeper connection: LOST")
            self._became_lost = True
        elif state == KazooState.SUSPENDED:
            self.log.debug("ZooKeeper connection: SUSPENDED")
        else:
            self.log.debug("ZooKeeper connection: CONNECTED")


    #========================================================================
    # Public Methods and Properties
    #========================================================================

    @property
    def connected(self):
        return self.client.state == KazooState.CONNECTED

    @property
    def suspended(self):
        return self.client.state == KazooState.SUSPENDED

    @property
    def lost(self):
        return self.client.state == KazooState.LOST

    @property
    def didLoseConnection(self):
        return self._became_lost

    def resetLostFlag(self):
        self._became_lost = False

    def connect(self, host_list, read_only=False):
        '''
        Establish a connection with ZooKeeper cluster.

        Convenience method if a pre-existing ZooKeeper connection is not
        supplied to the ZooKeeper object at instantiation time.

        :param list host_list: A list of
            :py:class:`~nodepool.zk.ZooKeeperConnectionConfig` objects
            (one per server) defining the ZooKeeper cluster servers.
        :param bool read_only: If True, establishes a read-only connection.

        '''
        if self.client is None:
            hosts = buildZooKeeperHosts(host_list)
            self.client = KazooClient(hosts=hosts, read_only=read_only)
            self.client.add_listener(self._connection_listener)
            self.client.start()

    def disconnect(self):
        '''
        Close the ZooKeeper cluster connection.

        You should call this method if you used connect() to establish a
        cluster connection.
        '''
        if self.client is not None and self.client.connected:
            self.client.stop()
            self.client.close()
            self.client = None

    def resetHosts(self, host_list):
        '''
        Reset the ZooKeeper cluster connection host list.

        :param list host_list: A list of
            :py:class:`~nodepool.zk.ZooKeeperConnectionConfig` objects
            (one per server) defining the ZooKeeper cluster servers.
        '''
        if self.client is not None:
            hosts = buildZooKeeperHosts(host_list)
            self.client.set_hosts(hosts=hosts)

    @contextmanager
    def imageBuildLock(self, image, blocking=True, timeout=None):
        '''
        Context manager to use for locking image builds.

        Obtains a write lock for the specified image.

        :param str image: Name of the image to lock
        :param bool blocking: Whether or not to block on trying to
            acquire the lock
        :param int timeout: When blocking, how long to wait for the lock
            to get acquired. None, the default, waits forever.

        :raises: TimeoutException if we failed to acquire the lock when
            blocking with a timeout. ZKLockException if we are not blocking
            and could not get the lock, or a lock is already held.
        '''
        lock = None
        try:
            lock = self._getImageBuildLock(image, blocking, timeout)
            yield
        finally:
            if lock:
                lock.release()

    @contextmanager
    def imageBuildNumberLock(self, image, build_number,
                             blocking=True, timeout=None):
        '''
        Context manager to use for locking _specific_ image builds.

        Obtains a write lock for the specified image build number. This is
        used for locking a build number during the cleanup phase of the
        builder.

        :param str image: Name of the image
        :param str build_number: The image build number to lock.
        :param bool blocking: Whether or not to block on trying to
            acquire the lock
        :param int timeout: When blocking, how long to wait for the lock
            to get acquired. None, the default, waits forever.

        :raises: TimeoutException if we failed to acquire the lock when
            blocking with a timeout. ZKLockException if we are not blocking
            and could not get the lock, or a lock is already held.
        '''
        lock = None
        try:
            lock = self._getImageBuildNumberLock(image, build_number,
                                                 blocking, timeout)
            yield
        finally:
            if lock:
                lock.release()

    @contextmanager
    def imageUploadLock(self, image, build_number, provider,
                        blocking=True, timeout=None):
        '''
        Context manager to use for locking image builds.

        Obtains a write lock for the specified image upload.

        :param str image: Name of the image.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param bool blocking: Whether or not to block on trying to
            acquire the lock
        :param int timeout: When blocking, how long to wait for the lock
            to get acquired. None, the default, waits forever.

        :raises: TimeoutException if we failed to acquire the lock when
            blocking with a timeout. ZKLockException if we are not blocking
            and could not get the lock, or a lock is already held.
        '''
        lock = None
        try:
            lock = self._getImageUploadLock(image, build_number, provider,
                                            blocking, timeout)
            yield
        finally:
            if lock:
                lock.release()

    def getImageNames(self):
        '''
        Retrieve the image names in Zookeeper.

        :returns: A list of image names or the empty list.
        '''
        path = self.IMAGE_ROOT

        try:
            images = self.client.get_children(path)
        except kze.NoNodeError:
            return []
        return sorted(images)

    def getBuildNumbers(self, image):
        '''
        Retrieve the builds available for an image.

        :param str image: The image name.

        :returns: A list of image build numbers or the empty list.
        '''
        path = self._imageBuildsPath(image)

        try:
            builds = self.client.get_children(path)
        except kze.NoNodeError:
            return []
        builds = [x for x in builds if x != 'lock']
        return builds

    def getBuildProviders(self, image, build_number):
        '''
        Retrieve the providers which have uploads for an image build.

        :param str image: The image name.
        :param str build_number: The image build number.

        :returns: A list of provider names or the empty list.

        '''
        path = self._imageProviderPath(image, build_number)

        try:
            providers = self.client.get_children(path)
        except kze.NoNodeError:
            return []

        return sorted(providers)

    def getImageUploadNumbers(self, image, build_number, provider):
        '''
        Retrieve upload numbers for a provider and image build.

        :param str image: The image name.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.

        :returns: A list of upload numbers or the empty list.

        '''
        path = self._imageUploadPath(image, build_number, provider)

        try:
            uploads = self.client.get_children(path)
        except kze.NoNodeError:
            return []

        uploads = [x for x in uploads if x != 'lock']
        return uploads

    def getBuild(self, image, build_number):
        '''
        Retrieve the image build data.

        :param str image: The image name.
        :param str build_number: The image build number.

        :returns: An ImageBuild object, or None if not found.
        '''
        path = self._imageBuildsPath(image) + "/%s" % build_number

        try:
            data, stat = self.client.get(path)
        except kze.NoNodeError:
            return None

        d = ImageBuild.fromDict(self._strToDict(data), build_number)
        d.stat = stat
        return d

    def getBuilds(self, image, states=None):
        '''
        Retrieve all image build data matching any given states.

        :param str image: The image name.
        :param list states: A list of build state values to match against.
            A value of None will disable state matching and just return
            all builds.

        :returns: A list of ImageBuild objects.
        '''
        path = self._imageBuildsPath(image)

        try:
            builds = self.client.get_children(path)
        except kze.NoNodeError:
            return []

        matches = []
        for build in builds:
            if build == 'lock':   # skip the build lock node
                continue
            data = self.getBuild(image, build)
            if states is None:
                matches.append(data)
            elif data and data.state in states:
                matches.append(data)

        return matches

    def getMostRecentBuilds(self, count, image, state=None):
        '''
        Retrieve the most recent image build data with the given state.

        :param int count: A count of the most recent builds to return.
            Use None for all builds.
        :param str image: The image name.
        :param str state: The build state to match on. Use None to
            ignore state

        :returns: A list of the most recent ImageBuild objects matching the
            given state, or an empty list if there were no builds matching
            the state. You may get less than 'count' entries if there were
            not enough matching builds.
        '''
        states = None
        if state:
            states = [state]

        builds = self.getBuilds(image, states)
        if not builds:
            return []

        builds.sort(key=lambda x: x.state_time, reverse=True)
        return builds[:count]

    def storeBuild(self, image, build_data, build_number=None):
        '''
        Store the image build data.

        The build data is either created if it does not exist, or it is
        updated in its entirety if it does not. There is no partial updating.
        The build data is expected to be represented as a dict. This dict may
        contain any data, as appropriate.

        If a build number is not supplied, then a new build node/number is
        created. The new build number is available in the return value.

        .. important: You should have the image locked before calling this
            method.

        :param str image: The image name for which we have data.
        :param ImageBuild build_data: The build data.
        :param str build_number: The image build number.

        :returns: A string for the build number that was updated.
        '''
        # Append trailing / so the sequence node is created as a child node.
        build_path = self._imageBuildsPath(image) + "/"

        if build_number is None:
            path = self.client.create(
                build_path,
                value=self._dictToStr(build_data.toDict()),
                sequence=True,
                makepath=True)
            build_number = path.split("/")[-1]
        else:
            path = build_path + build_number
            self.client.set(path, self._dictToStr(build_data.toDict()))

        return build_number

    def getImageUpload(self, image, build_number, provider, upload_number):
        '''
        Retrieve the image upload data.

        :param str image: The image name.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param str upload_number: The image upload number.

        :returns: An ImageUpload object, or None if not found.

        :raises: ZKException if the image upload path is not found.
        '''
        path = self._imageUploadPath(image, build_number, provider)
        path = path + "/%s" % upload_number

        try:
            data, stat = self.client.get(path)
        except kze.NoNodeError:
            return None

        d = ImageUpload.fromDict(
            self._strToDict(data), build_number, provider, image, upload_number
        )
        d.stat = stat
        return d

    def getUploads(self, image, build_number, provider, states=None):
        '''
        Retrieve all image upload data matching any given states.

        :param str image: The image name.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param list states: A list of upload state values to match against.
            A value of None will disable state matching and just return
            all uploads.

        :returns: A list of ImageUpload objects.
        '''
        path = self._imageUploadPath(image, build_number, provider)

        try:
            uploads = self.client.get_children(path)
        except kze.NoNodeError:
            return []

        matches = []
        for upload in uploads:
            if upload == 'lock':
                continue
            data = self.getImageUpload(image, build_number, provider, upload)
            if states is None:
                matches.append(data)
            elif data and data.state in states:
                matches.append(data)

        return matches

    def getMostRecentBuildImageUploads(self, count, image, build_number,
                                       provider, state=None):
        '''
        Retrieve the most recent image upload data with the given state.

        :param int count: A count of the most recent uploads to return.
            Use None for all uploads.
        :param str image: The image name.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param str state: The image upload state to match on. Use None to
            ignore state.

        :returns: A tuple with the most recent upload number and dictionary of
            upload data matching the given state, or None if there was no
            upload matching the state.
        '''
        states = None
        if state:
            states = [state]

        uploads = self.getUploads(image, build_number, provider, states)
        if not uploads:
            return []

        uploads.sort(key=lambda x: x.state_time, reverse=True)
        return uploads[:count]

    def getMostRecentImageUpload(self, image, provider,
                                 state="ready"):
        '''
        Retrieve the most recent image upload data with the given state.

        :param str image: The image name.
        :param str provider: The provider name owning the image.
        :param str state: The image upload state to match on.

        :returns: An ImageUpload object matching the given state, or
            None if there is no recent upload.
        '''

        recent_data = None
        for build_number in self.getBuildNumbers(image):
            path = self._imageUploadPath(image, build_number, provider)

            try:
                uploads = self.client.get_children(path)
            except kze.NoNodeError:
                uploads = []

            for upload in uploads:
                if upload == 'lock':   # skip the upload lock node
                    continue
                data = self.getImageUpload(image, build_number, provider, upload)
                if not data or data.state != state:
                    continue
                elif (recent_data is None or
                      recent_data.state_time < data.state_time):
                    recent_data = data

        return recent_data

    def storeImageUpload(self, image, build_number, provider, image_data,
                         upload_number=None):
        '''
        Store the built image's upload data for the given provider.

        The image upload data is either created if it does not exist, or it
        is updated in its entirety if it does not. There is no partial
        updating. The image data is expected to be represented as a dict.
        This dict may contain any data, as appropriate.

        If an image upload number is not supplied, then a new image upload
        node/number is created. The new upload number is available in the
        return value.

        :param str image: The image name for which we have data.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param ImageUpload image_data: The image data we want to store.
        :param str upload_number: The image upload number to update.

        :returns: A string for the upload number that was updated.

        :raises: ZKException for an invalid image build.
        '''
        # We expect the image builds path to already exist.
        build_path = self._imageBuildsPath(image)
        if not self.client.exists(build_path):
            raise npe.ZKException(
                "Cannot find build %s of image %s" % (build_number, image)
            )

        # Generate a path for the upload. This doesn't have to exist yet
        # since we'll create new provider/upload ID znodes automatically.
        # Append trailing / so the sequence node is created as a child node.
        upload_path = self._imageUploadPath(image, build_number, provider) + "/"

        if upload_number is None:
            path = self.client.create(
                upload_path,
                value=self._dictToStr(image_data.toDict()),
                sequence=True,
                makepath=True)
            upload_number = path.split("/")[-1]
        else:
            path = upload_path + upload_number
            self.client.set(path, self._dictToStr(image_data.toDict()))

        return upload_number

    def hasBuildRequest(self, image):
        '''
        Check if an image has a pending build request.

        :param str image: The image name to check.

        :returns: True if request is pending, False otherwise
        '''
        path = self._imageBuildRequestPath(image)
        if self.client.exists(path) is not None:
            return True
        return False

    def submitBuildRequest(self, image):
        '''
        Submit a request for a new image build.

        :param str image: The image name.
        '''
        path = self._imageBuildRequestPath(image)
        self.client.ensure_path(path)

    def removeBuildRequest(self, image):
        '''
        Remove an image build request.

        :param str image: The image name to check.
        '''
        path = self._imageBuildRequestPath(image)
        try:
            self.client.delete(path)
        except kze.NoNodeError:
            pass

    def deleteBuild(self, image, build_number):
        '''
        Delete an image build from ZooKeeper.

        Any provider uploads for this build must be deleted before the build
        node can be deleted.

        :param str image: The image name.
        :param str build_number: The image build number to delete.

        :returns: True if the build is successfully deleted or did not exist,
           False if the provider uploads still exist.
        '''
        path = self._imageBuildsPath(image)
        path = path + "/%s" % build_number

        # Verify that no upload znodes exist.
        for prov in self.getBuildProviders(image, build_number):
             if self.getImageUploadNumbers(image, build_number, prov):
                 return False

        try:
            # NOTE: Need to do recursively to remove lock znodes
            self.client.delete(path, recursive=True)
        except kze.NoNodeError:
            pass

        return True

    def deleteUpload(self, image, build_number, provider, upload_number):
        '''
        Delete an image upload from ZooKeeper.

        :param str image: The image name.
        :param str build_number: The image build number.
        :param str provider: The provider name owning the image.
        :param str upload_number: The image upload number to delete.
        '''
        path = self._imageUploadPath(image, build_number, provider)
        path = path + "/%s" % upload_number
        try:
            self.client.delete(path)
        except kze.NoNodeError:
            pass
