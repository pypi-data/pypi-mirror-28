# Copyright (C) 2014 OpenStack Foundation
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
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import threading
import time
from unittest import skip

import fixtures

from nodepool import jobs
from nodepool import tests
from nodepool import nodedb
import nodepool.fakeprovider
import nodepool.nodepool


class TestNodepool(tests.DBTestCase):
    log = logging.getLogger("nodepool.TestNodepool")

    def test_db(self):
        db = nodedb.NodeDatabase(self.dburi)
        with db.getSession() as session:
            session.getNodes()

    def test_node(self):
        """Test that an image and node are created"""
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)

    def test_disabled_label(self):
        """Test that an image and node are not created"""
        configfile = self.setup_config('node_disabled_label.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 0)

    def test_node_net_name(self):
        """Test that a node is created with a net name"""
        configfile = self.setup_config('node_net_name.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)

    def test_node_vhd_image(self):
        """Test that a image and node are created vhd image"""
        configfile = self.setup_config('node_vhd.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
        self.assertEqual(len(nodes), 1)

    def test_node_vhd_and_qcow2(self):
        """Test label provided by vhd and qcow2 images builds"""
        configfile = self.setup_config('node_vhd_and_qcow2.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider1', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider1',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            nodes = session.getNodes(provider_name='fake-provider2',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)

    def test_dib_upload_fail(self):
        """Test that an image upload failure is contained."""
        configfile = self.setup_config('node_upload_fail.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider2', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider1',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 0)
            nodes = session.getNodes(provider_name='fake-provider2',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 2)

    def test_subnodes(self):
        """Test that an image and node are created"""
        configfile = self.setup_config('subnodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 2)
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='multi-fake',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 2)
            for node in nodes:
                self.assertEqual(len(node.subnodes), 2)
                for subnode in node.subnodes:
                    self.assertEqual(subnode.state, nodedb.READY)

    def test_subnode_deletion_success(self):
        """Test that subnodes are deleted with parent node"""
        configfile = self.setup_config('subnodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        subnode_ids = []
        node_ids = []

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='multi-fake',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 2)
            for node in nodes:
                self.assertEqual(len(node.subnodes), 2)
                for subnode in node.subnodes:
                    self.assertEqual(subnode.state, nodedb.READY)
                    subnode_ids.append(subnode.id)
                node_ids.append(node.id)

        for node_id in node_ids:
            pool.deleteNode(node_id)

        self.wait_for_threads()
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            for subnode_id in subnode_ids:
                s = session.getSubNode(subnode_id)
                self.assertIsNone(s)

    def test_node_az(self):
        """Test that an image and node are created with az specified"""
        configfile = self.setup_config('node_az.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].az, 'az1')

    def test_node_ipv6(self):
        """Test that a node is created w/ or w/o ipv6 preferred flag"""
        configfile = self.setup_config('node_ipv6.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider1', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        self.waitForImage('fake-provider3', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            # ipv6 preferred set to true and ipv6 address available
            nodes = session.getNodes(provider_name='fake-provider1',
                                     label_name='fake-label1',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].ip, 'fake_v6')
            # ipv6 preferred unspecified and ipv6 address available
            nodes = session.getNodes(provider_name='fake-provider2',
                                     label_name='fake-label2',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].ip, 'fake')
            # ipv6 preferred set to true but ipv6 address unavailable
            nodes = session.getNodes(provider_name='fake-provider3',
                                     label_name='fake-label3',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            self.assertEqual(nodes[0].ip, 'fake')

    def test_node_delete_success(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)
        node_id = -1
        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            node_id = nodes[0].id

        pool.deleteNode(node_id)
        self.wait_for_threads()
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            ready_nodes = session.getNodes(provider_name='fake-provider',
                                           label_name='fake-label',
                                           target_name='fake-target',
                                           state=nodedb.READY)
            deleted_nodes = session.getNodes(provider_name='fake-provider',
                                             label_name='fake-label',
                                             target_name='fake-target',
                                             state=nodedb.DELETE)
            # Make sure we have one node which is a new node
            self.assertEqual(len(ready_nodes), 1)
            self.assertNotEqual(node_id, ready_nodes[0].id)

            # Make sure our old node was deleted
            self.assertEqual(len(deleted_nodes), 0)

    def test_node_delete_failure(self):
        def fail_delete(self, name):
            raise RuntimeError('Fake Error')

        fake_delete = 'nodepool.fakeprovider.FakeJenkins.delete_node'
        self.useFixture(fixtures.MonkeyPatch(fake_delete, fail_delete))

        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)
        node_id = -1
        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            node_id = nodes[0].id

        pool.deleteNode(node_id)
        self.wait_for_threads()
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            ready_nodes = session.getNodes(provider_name='fake-provider',
                                           label_name='fake-label',
                                           target_name='fake-target',
                                           state=nodedb.READY)
            deleted_nodes = session.getNodes(provider_name='fake-provider',
                                             label_name='fake-label',
                                             target_name='fake-target',
                                             state=nodedb.DELETE)
            # Make sure we have one node which is a new node
            self.assertEqual(len(ready_nodes), 1)
            self.assertNotEqual(node_id, ready_nodes[0].id)

            # Make sure our old node is in delete state
            self.assertEqual(len(deleted_nodes), 1)
            self.assertEqual(node_id, deleted_nodes[0].id)

    def test_leaked_node_with_nodepool_id(self):
        self._test_leaked_node('leaked_node_nodepool_id.yaml')

    def test_leaked_node(self):
        self._test_leaked_node('leaked_node.yaml')

    def _test_leaked_node(self, cfgfile):
        """Test that a leaked node is deleted"""
        configfile = self.setup_config(cfgfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.log.debug("Waiting for initial pool...")
        self.waitForNodes(pool)
        self.log.debug("...done waiting for initial pool.")

        # Make sure we have a node built and ready
        provider = pool.config.providers['fake-provider']
        manager = pool.getProviderManager(provider)
        servers = manager.listServers()
        self.assertEqual(len(servers), 1)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            # Delete the node from the db, but leave the instance
            # so it is leaked.
            self.log.debug("Delete node db record so instance is leaked...")
            for node in nodes:
                node.delete()
            self.log.debug("...deleted node db so instance is leaked.")
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 0)

        # Wait for nodepool to replace it, which should be enough
        # time for it to also delete the leaked node
        self.log.debug("Waiting for replacement pool...")
        self.waitForNodes(pool)
        self.log.debug("...done waiting for replacement pool.")

        # Make sure we end up with only one server (the replacement)
        servers = manager.listServers()
        self.assertEqual(len(servers), 1)
        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)

    def test_leaked_node_not_deleted(self):
        """Test that a leaked node is not deleted"""
        configfile = self.setup_config('leaked_node_nodepool_id.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.log.debug("Waiting for initial pool...")
        self.waitForNodes(pool)
        self.log.debug("...done waiting for initial pool.")
        pool.stop()

        # Make sure we have a node built and ready
        provider = pool.config.providers['fake-provider']
        manager = pool.getProviderManager(provider)
        servers = manager.listServers()
        self.assertEqual(len(servers), 1)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)
            # Delete the node from the db, but leave the instance
            # so it is leaked.
            self.log.debug("Delete node db record so instance is leaked...")
            for node in nodes:
                node.delete()
            self.log.debug("...deleted node db so instance is leaked.")
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 0)

        # Wait for nodepool to replace it, which should be enough
        # time for it to also delete the leaked node
        configfile = self.setup_config('leaked_node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        self.log.debug("Waiting for replacement pool...")
        self.waitForNodes(pool)
        self.log.debug("...done waiting for replacement pool.")

        # Make sure we end up with only one server (the replacement)
        provider = pool.config.providers['fake-provider']
        manager = pool.getProviderManager(provider)
        foobar_servers = manager.listServers()
        self.assertEqual(len(servers), 1)
        self.assertEqual(len(foobar_servers), 1)

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.READY)
            self.assertEqual(len(nodes), 1)

        # Just to be safe, ensure we have 2 nodes again.
        self.assertEqual(len(servers), 1)
        self.assertEqual(len(foobar_servers), 1)

    @skip("Disabled for early v3 development")
    def test_building_image_cleanup_on_start(self):
        """Test that a building image is deleted on start"""
        configfile = self.setup_config('node.yaml')
        pool = nodepool.nodepool.NodePool(self.secure_conf, configfile,
                                          watermark_sleep=1)
        try:
            pool.start()
            self.waitForImage(pool, 'fake-provider', 'fake-image')
            self.waitForNodes(pool)
        finally:
            # Stop nodepool instance so that it can be restarted.
            pool.stop()

        with pool.getDB().getSession() as session:
            images = session.getSnapshotImages()
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].state, nodedb.READY)
            images[0].state = nodedb.BUILDING

        # Start nodepool instance which should delete our old image.
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        # Ensure we have a config loaded for periodic cleanup.
        while not pool.config:
            time.sleep(0)
        # Wait for startup to shift state to a state that periodic cleanup
        # will act on.
        while True:
            with pool.getDB().getSession() as session:
                if session.getSnapshotImages()[0].state != nodedb.BUILDING:
                    break
                time.sleep(0)
        # Necessary to force cleanup to happen within the test timeframe
        pool.periodicCleanup()
        self.waitForImage(pool, 'fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            images = session.getSnapshotImages()
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].state, nodedb.READY)
            # should be second image built.
            self.assertEqual(images[0].id, 2)

    @skip("Disabled for early v3 development")
    def test_building_dib_image_cleanup_on_start(self):
        """Test that a building dib image is deleted on start"""
        configfile = self.setup_config('node.yaml')
        pool = nodepool.nodepool.NodePool(self.secure_conf, configfile,
                                          watermark_sleep=1)
        self._useBuilder(configfile)
        try:
            pool.start()
            self.waitForImage(pool, 'fake-provider', 'fake-image')
            self.waitForNodes(pool)
        finally:
            # Stop nodepool instance so that it can be restarted.
            pool.stop()

        with pool.getDB().getSession() as session:
            # We delete the snapshot image too to force a new dib image
            # to be built so that a new image can be uploaded to replace
            # the image that was in the snapshot table.
            images = session.getSnapshotImages()
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].state, nodedb.READY)
            images[0].state = nodedb.BUILDING
            images = session.getDibImages()
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].state, nodedb.READY)
            images[0].state = nodedb.BUILDING

        # Start nodepool instance which should delete our old image.
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        # Ensure we have a config loaded for periodic cleanup.
        while not pool.config:
            time.sleep(0)
        # Wait for startup to shift state to a state that periodic cleanup
        # will act on.
        while True:
            with pool.getDB().getSession() as session:
                if session.getDibImages()[0].state != nodedb.BUILDING:
                    break
                time.sleep(0)
        # Necessary to force cleanup to happen within the test timeframe
        pool.periodicCleanup()
        self.waitForImage(pool, 'fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            images = session.getDibImages()
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0].state, nodedb.READY)
            # should be second image built.
            self.assertEqual(images[0].id, 2)

    def test_job_start_event(self):
        """Test that job start marks node used"""
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        msg_obj = {'name': 'fake-job',
                   'build': {'node_name': 'fake-label-fake-provider-1'}}
        json_string = json.dumps(msg_obj)
        handler = nodepool.nodepool.NodeUpdateListener(pool,
                                                       'tcp://localhost:8881')
        handler.handleEvent('onStarted', json_string)
        self.wait_for_threads()

        with pool.getDB().getSession() as session:
            nodes = session.getNodes(provider_name='fake-provider',
                                     label_name='fake-label',
                                     target_name='fake-target',
                                     state=nodedb.USED)
            self.assertEqual(len(nodes), 1)

    def test_job_end_event(self):
        """Test that job end marks node delete"""
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        msg_obj = {'name': 'fake-job',
                   'build': {'node_name': 'fake-label-fake-provider-1',
                             'status': 'SUCCESS'}}
        json_string = json.dumps(msg_obj)
        # Don't delay when deleting.
        self.useFixture(fixtures.MonkeyPatch(
            'nodepool.nodepool.DELETE_DELAY',
            0))
        handler = nodepool.nodepool.NodeUpdateListener(pool,
                                                       'tcp://localhost:8881')
        handler.handleEvent('onFinalized', json_string)
        self.wait_for_threads()

        with pool.getDB().getSession() as session:
            node = session.getNode(1)
            self.assertEqual(node, None)

    def _test_job_auto_hold(self, result):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self._useBuilder(configfile)
        pool.start()

        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes(pool)

        with pool.getDB().getSession() as session:
            session.createJob('fake-job', hold_on_failure=1)

        msg_obj = {'name': 'fake-job',
                   'build': {'node_name': 'fake-label-fake-provider-1',
                             'status': result}}
        json_string = json.dumps(msg_obj)
        # Don't delay when deleting.
        self.useFixture(fixtures.MonkeyPatch(
            'nodepool.nodepool.DELETE_DELAY',
            0))
        handler = nodepool.nodepool.NodeUpdateListener(pool,
                                                       'tcp://localhost:8881')
        handler.handleEvent('onFinalized', json_string)
        self.wait_for_threads()
        return pool

    def test_job_auto_hold_success(self):
        """Test that a successful job does not hold a node"""
        pool = self._test_job_auto_hold('SUCCESS')
        with pool.getDB().getSession() as session:
            node = session.getNode(1)
            self.assertIsNone(node)

    def test_job_auto_hold_failure(self):
        """Test that a failed job automatically holds a node"""
        pool = self._test_job_auto_hold('FAILURE')
        with pool.getDB().getSession() as session:
            node = session.getNode(1)
            self.assertEqual(node.state, nodedb.HOLD)

    def test_job_auto_hold_failure_max(self):
        """Test that a failed job automatically holds only one node"""
        pool = self._test_job_auto_hold('FAILURE')
        with pool.getDB().getSession() as session:
            node = session.getNode(1)
            self.assertEqual(node.state, nodedb.HOLD)

        # Wait for a replacement node
        self.waitForNodes(pool)
        with pool.getDB().getSession() as session:
            node = session.getNode(2)
            self.assertEqual(node.state, nodedb.READY)

        # Fail the job again
        msg_obj = {'name': 'fake-job',
                   'build': {'node_name': 'fake-label-fake-provider-2',
                             'status': 'FAILURE'}}
        json_string = json.dumps(msg_obj)
        handler = nodepool.nodepool.NodeUpdateListener(pool,
                                                       'tcp://localhost:8881')
        handler.handleEvent('onFinalized', json_string)
        self.wait_for_threads()

        # Ensure that the second node was deleted
        with pool.getDB().getSession() as session:
            node = session.getNode(2)
            self.assertEqual(node, None)


class TestGearClient(tests.DBTestCase):
    def test_wait_for_completion(self):
        wj = jobs.WatchableJob('test', 'test', 'test')

        def call_on_completed():
            time.sleep(.2)
            wj.onCompleted()

        t = threading.Thread(target=call_on_completed)
        t.start()
        wj.waitForCompletion()

    def test_handle_disconnect(self):
        class MyJob(jobs.WatchableJob):
            def __init__(self, *args, **kwargs):
                super(MyJob, self).__init__(*args, **kwargs)
                self.disconnect_called = False

            def onDisconnect(self):
                self.disconnect_called = True
                super(MyJob, self).onDisconnect()

        client = nodepool.nodepool.GearmanClient()
        client.addServer('localhost', self.gearman_server.port)
        client.waitForServer()

        job = MyJob('test-job', '', '')
        client.submitJob(job)

        self.gearman_server.shutdown()
        job.waitForCompletion()
        self.assertEqual(job.disconnect_called, True)
