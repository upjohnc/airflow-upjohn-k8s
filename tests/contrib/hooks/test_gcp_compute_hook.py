# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import unittest

from tests.contrib.utils.base_gcp_mock import mock_base_gcp_hook_no_default_project_id, \
    mock_base_gcp_hook_default_project_id, GCP_PROJECT_ID_HOOK_UNIT_TEST
from tests.compat import mock

from airflow import AirflowException
from airflow.contrib.hooks.gcp_compute_hook import GceHook

GCE_ZONE = 'zone'
GCE_INSTANCE = 'instance'
GCE_INSTANCE_TEMPLATE = 'instance-template'
GCE_REQUEST_ID = 'request_id'
GCE_INSTANCE_GROUP_MANAGER = 'instance_group_manager'


class TestGcpComputeHookNoDefaultProjectId(unittest.TestCase):

    def setUp(self):
        with mock.patch('airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook.__init__',
                        new=mock_base_gcp_hook_no_default_project_id):
            self.gce_hook_no_project_id = GceHook(gcp_conn_id='test')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_start_instance_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        start_method = get_conn.return_value.instances.return_value.start
        execute_method = start_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.start_instance(
            project_id='example-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        start_method.assert_called_once_with(instance='instance', project='example-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_start_instance_no_project_id(self, wait_for_operation_to_complete, get_conn):
        start_method = get_conn.return_value.instances.return_value.start
        execute_method = start_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.start_instance(
                zone=GCE_ZONE,
                resource_id=GCE_INSTANCE)
        start_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_stop_instance_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        stop_method = get_conn.return_value.instances.return_value.stop
        execute_method = stop_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.stop_instance(
            project_id='example-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        stop_method.assert_called_once_with(instance='instance', project='example-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_stop_instance_no_project_id(self, wait_for_operation_to_complete, get_conn):
        stop_method = get_conn.return_value.instances.return_value.stop
        execute_method = stop_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.stop_instance(
                zone=GCE_ZONE,
                resource_id=GCE_INSTANCE)
        stop_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_set_machine_type_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        set_machine_type_method = get_conn.return_value.instances.return_value.setMachineType
        execute_method = set_machine_type_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.set_machine_type(
            body={},
            project_id='example-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        set_machine_type_method.assert_called_once_with(body={}, instance='instance',
                                                        project='example-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_set_machine_type_no_project_id(self, wait_for_operation_to_complete, get_conn):
        set_machine_type_method = get_conn.return_value.instances.return_value.setMachineType
        execute_method = set_machine_type_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.set_machine_type(
                body={},
                zone=GCE_ZONE,
                resource_id=GCE_INSTANCE)
        set_machine_type_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_template_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceTemplates.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.get_instance_template(
            resource_id=GCE_INSTANCE_TEMPLATE,
            project_id='example-project'
        )
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceTemplate='instance-template', project='example-project')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_template_no_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceTemplates.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.get_instance_template(
                resource_id=GCE_INSTANCE_TEMPLATE
            )
        get_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_insert_instance_template_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        insert_method = get_conn.return_value.instanceTemplates.return_value.insert
        execute_method = insert_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.insert_instance_template(
            project_id=GCP_PROJECT_ID_HOOK_UNIT_TEST,
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        insert_method.assert_called_once_with(body={}, project='example-project', requestId='request_id')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_insert_instance_template_no_project_id(self, wait_for_operation_to_complete, get_conn):
        insert_method = get_conn.return_value.instanceTemplates.return_value.insert
        execute_method = insert_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.insert_instance_template(
                body={},
                request_id=GCE_REQUEST_ID
            )
        insert_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_group_manager_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceGroupManagers.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.get_instance_group_manager(
            project_id=GCP_PROJECT_ID_HOOK_UNIT_TEST,
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER
        )
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceGroupManager='instance_group_manager',
                                           project='example-project',
                                           zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_group_manager_no_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceGroupManagers.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.get_instance_group_manager(
                zone=GCE_ZONE,
                resource_id=GCE_INSTANCE_GROUP_MANAGER
            )
        get_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_patch_instance_group_manager_overridden_project_id(self,
                                                                wait_for_operation_to_complete, get_conn):
        patch_method = get_conn.return_value.instanceGroupManagers.return_value.patch
        execute_method = patch_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook_no_project_id.patch_instance_group_manager(
            project_id=GCP_PROJECT_ID_HOOK_UNIT_TEST,
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER,
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        patch_method.assert_called_once_with(
            body={},
            instanceGroupManager='instance_group_manager',
            project='example-project',
            requestId='request_id',
            zone='zone'
        )
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(operation_name='operation_id',
                                                               project_id='example-project',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_patch_instance_group_manager_no_project_id(self, wait_for_operation_to_complete, get_conn):
        patch_method = get_conn.return_value.instanceGroupManagers.return_value.patch
        execute_method = patch_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        with self.assertRaises(AirflowException) as cm:
            self.gce_hook_no_project_id.patch_instance_group_manager(
                zone=GCE_ZONE,
                resource_id=GCE_INSTANCE_GROUP_MANAGER,
                body={},
                request_id=GCE_REQUEST_ID
            )
        patch_method.assert_not_called()
        execute_method.assert_not_called()
        err = cm.exception
        self.assertIn("The project id must be passed", str(err))
        wait_for_operation_to_complete.assert_not_called()


class TestGcpComputeHookDefaultProjectId(unittest.TestCase):
    def setUp(self):
        with mock.patch('airflow.contrib.hooks.gcp_api_base_hook.GoogleCloudBaseHook.__init__',
                        new=mock_base_gcp_hook_default_project_id):
            self.gce_hook = GceHook(gcp_conn_id='test')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_start_instance(self, wait_for_operation_to_complete, get_conn):
        start_method = get_conn.return_value.instances.return_value.start
        execute_method = start_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.start_instance(
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        start_method.assert_called_once_with(instance='instance', project='example-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_start_instance_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        start_method = get_conn.return_value.instances.return_value.start
        execute_method = start_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.start_instance(
            project_id='new-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        start_method.assert_called_once_with(instance='instance', project='new-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='new-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_stop_instance(self, wait_for_operation_to_complete, get_conn):
        stop_method = get_conn.return_value.instances.return_value.stop
        execute_method = stop_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.stop_instance(
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        stop_method.assert_called_once_with(instance='instance', project='example-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_stop_instance_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        stop_method = get_conn.return_value.instances.return_value.stop
        execute_method = stop_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.stop_instance(
            project_id='new-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        stop_method.assert_called_once_with(instance='instance', project='new-project', zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='new-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_set_machine_type_instance(self, wait_for_operation_to_complete, get_conn):
        execute_method = get_conn.return_value.instances.return_value.setMachineType.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.set_machine_type(
            body={},
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_set_machine_type_instance_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        execute_method = get_conn.return_value.instances.return_value.setMachineType.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.set_machine_type(
            project_id='new-project',
            body={},
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE)
        self.assertIsNone(res)
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='new-project',
                                                               operation_name='operation_id',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_template(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceTemplates.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.get_instance_template(
            resource_id=GCE_INSTANCE_TEMPLATE)
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceTemplate='instance-template', project='example-project')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_template_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceTemplates.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.get_instance_template(
            project_id='new-project',
            resource_id=GCE_INSTANCE_TEMPLATE)
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceTemplate='instance-template', project='new-project')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_insert_instance_template(self, wait_for_operation_to_complete, get_conn):
        insert_method = get_conn.return_value.instanceTemplates.return_value.insert
        execute_method = insert_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.insert_instance_template(
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        insert_method.assert_called_once_with(body={}, project='example-project', requestId='request_id')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='example-project',
                                                               operation_name='operation_id')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_insert_instance_template_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        insert_method = get_conn.return_value.instanceTemplates.return_value.insert
        execute_method = insert_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.insert_instance_template(
            project_id='new-project',
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        insert_method.assert_called_once_with(body={}, project='new-project', requestId='request_id')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(project_id='new-project',
                                                               operation_name='operation_id')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_group_manager(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceGroupManagers.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.get_instance_group_manager(
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER
        )
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceGroupManager='instance_group_manager',
                                           project='example-project',
                                           zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_get_instance_group_manager_overridden_project_id(self, wait_for_operation_to_complete, get_conn):
        get_method = get_conn.return_value.instanceGroupManagers.return_value.get
        execute_method = get_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.get_instance_group_manager(
            project_id='new-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER
        )
        self.assertIsNotNone(res)
        get_method.assert_called_once_with(instanceGroupManager='instance_group_manager',
                                           project='new-project',
                                           zone='zone')
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_not_called()

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_patch_instance_group_manager(self, wait_for_operation_to_complete, get_conn):
        patch_method = get_conn.return_value.instanceGroupManagers.return_value.patch
        execute_method = patch_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.patch_instance_group_manager(
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER,
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        patch_method.assert_called_once_with(
            body={},
            instanceGroupManager='instance_group_manager',
            project='example-project',
            requestId='request_id',
            zone='zone'
        )
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(operation_name='operation_id',
                                                               project_id='example-project',
                                                               zone='zone')

    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook.get_conn')
    @mock.patch('airflow.contrib.hooks.gcp_compute_hook.GceHook._wait_for_operation_to_complete')
    def test_patch_instance_group_manager_overridden_project_id(self,
                                                                wait_for_operation_to_complete,
                                                                get_conn):
        patch_method = get_conn.return_value.instanceGroupManagers.return_value.patch
        execute_method = patch_method.return_value.execute
        execute_method.return_value = {"name": "operation_id"}
        wait_for_operation_to_complete.return_value = None
        res = self.gce_hook.patch_instance_group_manager(
            project_id='new-project',
            zone=GCE_ZONE,
            resource_id=GCE_INSTANCE_GROUP_MANAGER,
            body={},
            request_id=GCE_REQUEST_ID
        )
        self.assertIsNone(res)
        patch_method.assert_called_once_with(
            body={},
            instanceGroupManager='instance_group_manager',
            project='new-project',
            requestId='request_id',
            zone='zone'
        )
        execute_method.assert_called_once_with(num_retries=5)
        wait_for_operation_to_complete.assert_called_once_with(operation_name='operation_id',
                                                               project_id='new-project',
                                                               zone='zone')
