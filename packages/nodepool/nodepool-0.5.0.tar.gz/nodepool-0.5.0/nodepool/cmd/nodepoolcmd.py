#!/usr/bin/env python
#
# Copyright 2013 OpenStack Foundation
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

import argparse
import logging.config
import sys

from nodepool import nodedb
from nodepool import nodepool
from nodepool import status
from nodepool import zk
from nodepool.cmd import NodepoolApp
from nodepool.version import version_info as npc_version_info
from config_validator import ConfigValidator
from prettytable import PrettyTable

log = logging.getLogger(__name__)


class NodePoolCmd(NodepoolApp):

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Node pool.')
        parser.add_argument('-c', dest='config',
                            default='/etc/nodepool/nodepool.yaml',
                            help='path to config file')
        parser.add_argument('-s', dest='secure',
                            default='/etc/nodepool/secure.conf',
                            help='path to secure file')
        parser.add_argument('-l', dest='logconfig',
                            help='path to log config file')
        parser.add_argument('--version', action='version',
                            version=npc_version_info.version_string(),
                            help='show version')
        parser.add_argument('--debug', dest='debug', action='store_true',
                            help='show DEBUG level logging')

        subparsers = parser.add_subparsers(title='commands',
                                           description='valid commands',
                                           dest='command',
                                           help='additional help')

        cmd_list = subparsers.add_parser('list', help='list nodes')
        cmd_list.set_defaults(func=self.list)
        cmd_image_list = subparsers.add_parser(
            'image-list', help='list images from providers')
        cmd_image_list.set_defaults(func=self.image_list)

        cmd_dib_image_list = subparsers.add_parser(
            'dib-image-list',
            help='list images built with diskimage-builder')
        cmd_dib_image_list.set_defaults(func=self.dib_image_list)

        cmd_image_build = subparsers.add_parser(
            'image-build',
            help='build image using diskimage-builder')
        cmd_image_build.add_argument('image', help='image name')
        cmd_image_build.set_defaults(func=self.image_build)

        cmd_alien_list = subparsers.add_parser(
            'alien-list',
            help='list nodes not accounted for by nodepool')
        cmd_alien_list.set_defaults(func=self.alien_list)
        cmd_alien_list.add_argument('provider', help='provider name',
                                    nargs='?')

        cmd_alien_image_list = subparsers.add_parser(
            'alien-image-list',
            help='list images not accounted for by nodepool')
        cmd_alien_image_list.set_defaults(func=self.alien_image_list)
        cmd_alien_image_list.add_argument('provider', help='provider name',
                                          nargs='?')

        cmd_hold = subparsers.add_parser(
            'hold',
            help='place a node in the HOLD state')
        cmd_hold.set_defaults(func=self.hold)
        cmd_hold.add_argument('id', help='node id')
        cmd_hold.add_argument('--reason',
                              help='Optional reason this node is held')

        cmd_delete = subparsers.add_parser(
            'delete',
            help='place a node in the DELETE state')
        cmd_delete.set_defaults(func=self.delete)
        cmd_delete.add_argument('id', help='node id')
        cmd_delete.add_argument('--now',
                                action='store_true',
                                help='delete the node in the foreground')

        cmd_image_delete = subparsers.add_parser(
            'image-delete',
            help='delete an image')
        cmd_image_delete.set_defaults(func=self.image_delete)
        cmd_image_delete.add_argument('--provider', help='provider name',
                                      required=True)
        cmd_image_delete.add_argument('--image', help='image name',
                                      required=True)
        cmd_image_delete.add_argument('--upload-id', help='image upload id',
                                      required=True)
        cmd_image_delete.add_argument('--build-id', help='image build id',
                                      required=True)

        cmd_dib_image_delete = subparsers.add_parser(
            'dib-image-delete',
            help='delete image built with diskimage-builder')
        cmd_dib_image_delete.set_defaults(func=self.dib_image_delete)
        cmd_dib_image_delete.add_argument('id', help='dib image id')

        cmd_config_validate = subparsers.add_parser(
            'config-validate',
            help='Validate configuration file')
        cmd_config_validate.set_defaults(func=self.config_validate)

        cmd_job_list = subparsers.add_parser('job-list', help='list jobs')
        cmd_job_list.set_defaults(func=self.job_list)

        cmd_job_create = subparsers.add_parser('job-create', help='create job')
        cmd_job_create.add_argument(
            'name',
            help='job name')
        cmd_job_create.add_argument('--hold-on-failure',
                                    help='number of nodes to hold when this job fails')
        cmd_job_create.set_defaults(func=self.job_create)

        cmd_job_delete = subparsers.add_parser(
            'job-delete',
            help='delete job')
        cmd_job_delete.set_defaults(func=self.job_delete)
        cmd_job_delete.add_argument('id', help='job id')

        self.args = parser.parse_args()

    def setup_logging(self):
        if self.args.debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(levelname)s %(name)s: '
                                       '%(message)s')
        elif self.args.logconfig:
            NodepoolApp.setup_logging(self)
        else:
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(levelname)s %(name)s: '
                                       '%(message)s')
            l = logging.getLogger('kazoo')
            l.setLevel(logging.WARNING)

    def list(self, node_id=None):
        print status.node_list(self.pool.getDB(), node_id)

    def dib_image_list(self):
        print status.dib_image_list(self.zk)

    def image_list(self):
        print status.image_list(self.zk)

    def image_build(self, diskimage=None):
        diskimage = diskimage or self.args.image
        if diskimage not in self.pool.config.diskimages:
            # only can build disk images, not snapshots
            raise Exception("Trying to build a non disk-image-builder "
                            "image: %s" % diskimage)

        if self.pool.config.diskimages[diskimage].pause:
            raise Exception(
                "Skipping build request for image %s; paused" % diskimage)

        self.zk.submitBuildRequest(diskimage)

    def alien_list(self):
        self.pool.reconfigureManagers(self.pool.config, False)

        t = PrettyTable(["Provider", "Hostname", "Server ID", "IP"])
        t.align = 'l'
        with self.pool.getDB().getSession() as session:
            for provider in self.pool.config.providers.values():
                if (self.args.provider and
                        provider.name != self.args.provider):
                    continue
                manager = self.pool.getProviderManager(provider)

                try:
                    for server in manager.listServers():
                        if not session.getNodeByExternalID(
                                provider.name, server['id']):
                            t.add_row([provider.name, server['name'],
                                       server['id'], server['public_v4']])
                except Exception as e:
                    log.warning("Exception listing aliens for %s: %s"
                                % (provider.name, str(e.message)))
        print t

    def alien_image_list(self):
        self.pool.reconfigureManagers(self.pool.config, False)

        t = PrettyTable(["Provider", "Name", "Image ID"])
        t.align = 'l'

        for provider in self.pool.config.providers.values():
            if (self.args.provider and
                    provider.name != self.args.provider):
                continue
            manager = self.pool.getProviderManager(provider)

            # Build list of provider images as known by the provider
            provider_images = []
            try:
                # Only consider images marked as managed by nodepool.
                # Prevent cloud-provider images from showing
                # up in alien list since we can't do anything about them
                # anyway.
                provider_images = [
                    image for image in manager.listImages()
                    if 'nodepool_build_id' in image['properties']]
            except Exception as e:
                log.warning("Exception listing alien images for %s: %s"
                            % (provider.name, str(e.message)))

            alien_ids = []
            uploads = []
            for image in provider.images:
                # Build list of provider images as recorded in ZK
                for bnum in self.zk.getBuildNumbers(image):
                    uploads.extend(
                        self.zk.getUploads(image, bnum,
                                           provider.name,
                                           states=[zk.READY])
                    )

            # Calculate image IDs present in the provider, but not in ZK
            provider_image_ids = set([img['id'] for img in provider_images])
            zk_image_ids = set([img.external_id for img in uploads])
            alien_ids = provider_image_ids - zk_image_ids

            for image in provider_images:
                if image['id'] in alien_ids:
                    t.add_row([provider.name, image['name'], image['id']])

        print t

    def hold(self):
        node_id = None
        with self.pool.getDB().getSession() as session:
            node = session.getNode(self.args.id)
            node.state = nodedb.HOLD
            if self.args.reason:
                node.comment = self.args.reason
            node_id = node.id
        self.list(node_id=node_id)

    def delete(self):
        if self.args.now:
            self.pool.reconfigureManagers(self.pool.config)
        with self.pool.getDB().getSession() as session:
            node = session.getNode(self.args.id)
            if not node:
                print "Node %s not found." % self.args.id
            elif self.args.now:
                self.pool._deleteNode(session, node)
            else:
                node.state = nodedb.DELETE
                self.list(node_id=node.id)

    def dib_image_delete(self):
        (image, build_num) = self.args.id.rsplit('-', 1)
        build = self.zk.getBuild(image, build_num)
        if not build:
            print("Build %s not found" % self.args.id)
            return

        if build.state == zk.BUILDING:
            print("Cannot delete a build in progress")
            return

        build.state = zk.DELETING
        self.zk.storeBuild(image, build, build.id)

    def image_delete(self):
        provider_name = self.args.provider
        image_name = self.args.image
        build_id = self.args.build_id
        upload_id = self.args.upload_id

        image = self.zk.getImageUpload(image_name, build_id, provider_name,
                                       upload_id)
        if not image:
            print("Image upload not found")
            return

        if image.state == zk.UPLOADING:
            print("Cannot delete because image upload in progress")
            return

        image.state = zk.DELETING
        self.zk.storeImageUpload(image.image_name, image.build_id,
                                 image.provider_name, image, image.id)

    def config_validate(self):
        validator = ConfigValidator(self.args.config)
        validator.validate()
        log.info("Configuration validation complete")
        #TODO(asselin,yolanda): add validation of secure.conf

    def job_list(self):
        t = PrettyTable(["ID", "Name", "Hold on Failure"])
        t.align = 'l'
        with self.pool.getDB().getSession() as session:
            for job in session.getJobs():
                t.add_row([job.id, job.name, job.hold_on_failure])
            print t

    def job_create(self):
        with self.pool.getDB().getSession() as session:
            session.createJob(self.args.name,
                              hold_on_failure=self.args.hold_on_failure)
        self.job_list()

    def job_delete(self):
        with self.pool.getDB().getSession() as session:
            job = session.getJob(self.args.id)
            if not job:
                print "Job %s not found." % self.args.id
            else:
                job.delete()

    def _wait_for_threads(self, threads):
        for t in threads:
            if t:
                t.join()

    def main(self):
        self.zk = None

        # commands which do not need to start-up or parse config
        if self.args.command in ('config-validate'):
            return self.args.func()

        self.pool = nodepool.NodePool(self.args.secure, self.args.config)
        config = self.pool.loadConfig()

        # commands needing ZooKeeper
        if self.args.command in ('image-build', 'dib-image-list',
                                 'image-list', 'dib-image-delete',
                                 'image-delete', 'alien-image-list'):
            self.zk = zk.ZooKeeper()
            self.zk.connect(config.zookeeper_servers.values())
        else:
            self.pool.reconfigureDatabase(config)

        self.pool.setConfig(config)
        self.args.func()

        if self.zk:
            self.zk.disconnect()

def main():
    npc = NodePoolCmd()
    npc.parse_arguments()
    npc.setup_logging()
    return npc.main()


if __name__ == "__main__":
    sys.exit(main())
