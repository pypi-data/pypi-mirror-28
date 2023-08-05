#!/usr/bin/env python

# Copyright (C) 2011-2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

import os_client_config
from six.moves import configparser as ConfigParser
import time
import yaml

import fakeprovider
import zk


class ConfigValue(object):
    def __eq__(self, other):
        if isinstance(other, ConfigValue):
            if other.__dict__ == self.__dict__:
                return True
        return False


class Config(ConfigValue):
    pass


class Provider(ConfigValue):
    def __eq__(self, other):
        if (other.cloud_config != self.cloud_config or
            other.nodepool_id != self.nodepool_id or
            other.max_servers != self.max_servers or
            other.pool != self.pool or
            other.image_type != self.image_type or
            other.rate != self.rate or
            other.api_timeout != self.api_timeout or
            other.boot_timeout != self.boot_timeout or
            other.launch_timeout != self.launch_timeout or
            other.networks != self.networks or
            other.ipv6_preferred != self.ipv6_preferred or
            other.clean_floating_ips != self.clean_floating_ips or
            other.azs != self.azs):
            return False
        new_images = other.images
        old_images = self.images
        # Check if images have been added or removed
        if set(new_images.keys()) != set(old_images.keys()):
            return False
        # check if existing images have been updated
        for k in new_images:
            if (new_images[k].min_ram != old_images[k].min_ram or
                new_images[k].name_filter != old_images[k].name_filter or
                new_images[k].key_name != old_images[k].key_name or
                new_images[k].username != old_images[k].username or
                new_images[k].user_home != old_images[k].user_home or
                new_images[k].private_key != old_images[k].private_key or
                new_images[k].meta != old_images[k].meta or
                new_images[k].config_drive != old_images[k].config_drive):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Provider %s>" % self.name


class ProviderImage(ConfigValue):
    def __repr__(self):
        return "<ProviderImage %s>" % self.name


class Target(ConfigValue):
    def __repr__(self):
        return "<Target %s>" % self.name


class Label(ConfigValue):
    def __repr__(self):
        return "<Label %s>" % self.name


class LabelProvider(ConfigValue):
    def __repr__(self):
        return "<LabelProvider %s>" % self.name


class Cron(ConfigValue):
    def __repr__(self):
        return "<Cron %s>" % self.name


class ZMQPublisher(ConfigValue):
    def __repr__(self):
        return "<ZMQPublisher %s>" % self.name


class GearmanServer(ConfigValue):
    def __repr__(self):
        return "<GearmanServer %s>" % self.name


class DiskImage(ConfigValue):
    def __repr__(self):
        return "<DiskImage %s>" % self.name


class Network(ConfigValue):
    def __repr__(self):
        return "<Network name:%s id:%s>" % (self.name, self.id)


def loadConfig(config_path):
    retry = 3

    # Since some nodepool code attempts to dynamically re-read its config
    # file, we need to handle the race that happens if an outside entity
    # edits it (causing it to temporarily not exist) at the same time we
    # attempt to reload it.
    while True:
        try:
            config = yaml.load(open(config_path))
            break
        except IOError as e:
            if e.errno == 2:
                retry = retry - 1
                time.sleep(.5)
            else:
                raise e
            if retry == 0:
                raise e

    cloud_config = os_client_config.OpenStackConfig()

    newconfig = Config()
    newconfig.db = None
    newconfig.dburi = None
    newconfig.providers = {}
    newconfig.targets = {}
    newconfig.labels = {}
    newconfig.elementsdir = config.get('elements-dir')
    newconfig.imagesdir = config.get('images-dir')
    newconfig.dburi = None
    newconfig.provider_managers = {}
    newconfig.jenkins_managers = {}
    newconfig.zmq_publishers = {}
    newconfig.gearman_servers = {}
    newconfig.zookeeper_servers = {}
    newconfig.diskimages = {}
    newconfig.crons = {}

    for name, default in [
        ('cleanup', '* * * * *'),
        ('check', '*/15 * * * *'),
        ]:
        c = Cron()
        c.name = name
        newconfig.crons[c.name] = c
        c.job = None
        c.timespec = config.get('cron', {}).get(name, default)

    for addr in config.get('zmq-publishers', []):
        z = ZMQPublisher()
        z.name = addr
        z.listener = None
        newconfig.zmq_publishers[z.name] = z

    for server in config.get('gearman-servers', []):
        g = GearmanServer()
        g.host = server['host']
        g.port = server.get('port', 4730)
        g.name = g.host + '_' + str(g.port)
        newconfig.gearman_servers[g.name] = g

    for server in config.get('zookeeper-servers', []):
        z = zk.ZooKeeperConnectionConfig(server['host'],
                                         server.get('port', 2181),
                                         server.get('chroot', None))
        name = z.host + '_' + str(z.port)
        newconfig.zookeeper_servers[name] = z

    for provider in config.get('providers', []):
        p = Provider()
        p.name = provider['name']
        newconfig.providers[p.name] = p

        cloud_kwargs = _cloudKwargsFromProvider(provider)
        p.cloud_config = _get_one_cloud(cloud_config, cloud_kwargs)
        p.nodepool_id = provider.get('nodepool-id', None)
        p.region_name = provider.get('region-name')
        p.max_servers = provider['max-servers']
        p.pool = provider.get('pool', None)
        p.rate = provider.get('rate', 1.0)
        p.api_timeout = provider.get('api-timeout')
        p.boot_timeout = provider.get('boot-timeout', 60)
        p.launch_timeout = provider.get('launch-timeout', 3600)
        p.networks = []
        for network in provider.get('networks', []):
            n = Network()
            p.networks.append(n)
            if 'net-id' in network:
                n.id = network['net-id']
                n.name = None
            elif 'net-label' in network:
                n.name = network['net-label']
                n.id = None
            else:
                n.name = network.get('name')
                n.id = None
        p.ipv6_preferred = provider.get('ipv6-preferred')
        p.clean_floating_ips = provider.get('clean-floating-ips')
        p.azs = provider.get('availability-zones')
        p.template_hostname = provider.get(
            'template-hostname',
            'template-{image.name}-{timestamp}'
        )
        p.image_type = provider.get(
            'image-type', p.cloud_config.config['image_format'])
        p.images = {}
        for image in provider['images']:
            i = ProviderImage()
            i.name = image['name']
            p.images[i.name] = i
            i.min_ram = image['min-ram']
            i.name_filter = image.get('name-filter', None)
            i.key_name = image.get('key-name', None)
            i.username = image.get('username', 'jenkins')
            i.user_home = image.get('user-home', '/home/jenkins')
            i.pause = bool(image.get('pause', False))
            i.private_key = image.get('private-key',
                                      '/var/lib/jenkins/.ssh/id_rsa')
            i.config_drive = image.get('config-drive', True)

            # This dict is expanded and used as custom properties when
            # the image is uploaded.
            i.meta = image.get('meta', {})
            # 5 elements, and no key or value can be > 255 chars
            # per Nova API rules
            if i.meta:
                if len(i.meta) > 5 or \
                   any([len(k) > 255 or len(v) > 255
                        for k, v in i.meta.iteritems()]):
                    # soft-fail
                    #self.log.error("Invalid metadata for %s; ignored"
                    #               % i.name)
                    i.meta = {}

    if 'diskimages' in config:
        for diskimage in config['diskimages']:
            d = DiskImage()
            d.name = diskimage['name']
            newconfig.diskimages[d.name] = d
            if 'elements' in diskimage:
                d.elements = u' '.join(diskimage['elements'])
            else:
                d.elements = ''
            # must be a string, as it's passed as env-var to
            # d-i-b, but might be untyped in the yaml and
            # interpreted as a number (e.g. "21" for fedora)
            d.release = str(diskimage.get('release', ''))
            d.rebuild_age = int(diskimage.get('rebuild-age', 86400))
            d.env_vars = diskimage.get('env-vars', {})
            if not isinstance(d.env_vars, dict):
                #self.log.error("%s: ignoring env-vars; "
                #               "should be a dict" % d.name)
                d.env_vars = {}
            d.image_types = set(diskimage.get('formats', []))
            d.pause = bool(diskimage.get('pause', False))
        # Do this after providers to build the image-types
        for provider in newconfig.providers.values():
            for image in provider.images.values():
                diskimage = newconfig.diskimages[image.name]
                diskimage.image_types.add(provider.image_type)

    for label in config.get('labels', []):
        l = Label()
        l.name = label['name']
        newconfig.labels[l.name] = l
        l.image = label['image']
        l.min_ready = label.get('min-ready', 2)
        l.subnodes = label.get('subnodes', 0)
        l.ready_script = label.get('ready-script')
        l.providers = {}
        for provider in label['providers']:
            p = LabelProvider()
            p.name = provider['name']
            l.providers[p.name] = p

    for target in config.get('targets', []):
        t = Target()
        t.name = target['name']
        newconfig.targets[t.name] = t
        jenkins = target.get('jenkins', {})
        t.online = True
        t.rate = target.get('rate', 1.0)
        t.jenkins_test_job = jenkins.get('test-job')
        t.jenkins_url = None
        t.jenkins_user = None
        t.jenkins_apikey = None
        t.jenkins_credentials_id = None

        t.assign_via_gearman = target.get('assign-via-gearman', False)

        t.hostname = target.get(
            'hostname',
            '{label.name}-{provider.name}-{node_id}'
        )
        t.subnode_hostname = target.get(
            'subnode-hostname',
            '{label.name}-{provider.name}-{node_id}-{subnode_id}'
        )

    return newconfig


def loadSecureConfig(config, secure_config_path):
    secure = ConfigParser.ConfigParser()
    secure.readfp(open(secure_config_path))

    config.dburi = secure.get('database', 'dburi')

    for target in config.targets.values():
        section_name = 'jenkins "%s"' % target.name
        if secure.has_section(section_name):
            target.jenkins_url = secure.get(section_name, 'url')
            target.jenkins_user = secure.get(section_name, 'user')
            target.jenkins_apikey = secure.get(section_name, 'apikey')

        try:
            target.jenkins_credentials_id = secure.get(
                section_name, 'credentials')
        except:
            pass


def _cloudKwargsFromProvider(provider):
    cloud_kwargs = {}
    for arg in ['region-name', 'api-timeout', 'cloud']:
        if arg in provider:
            cloud_kwargs[arg] = provider[arg]

    # These are named from back when we only talked to Nova. They're
    # actually compute service related
    if 'service-type' in provider:
        cloud_kwargs['compute-service-type'] = provider['service-type']
    if 'service-name' in provider:
        cloud_kwargs['compute-service-name'] = provider['service-name']

    auth_kwargs = {}
    for auth_key in (
            'username', 'password', 'auth-url', 'project-id', 'project-name'):
        if auth_key in provider:
            auth_kwargs[auth_key] = provider[auth_key]

    cloud_kwargs['auth'] = auth_kwargs
    return cloud_kwargs


def _get_one_cloud(cloud_config, cloud_kwargs):
    '''This is a function to allow for overriding it in tests.'''
    if cloud_kwargs.get('auth', {}).get('auth-url', '') == 'fake':
        return fakeprovider.fake_get_one_cloud(cloud_config, cloud_kwargs)
    return cloud_config.get_one_cloud(**cloud_kwargs)
