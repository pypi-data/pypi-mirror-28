# tile-generator
#
# Copyright (c) 2015-Present Pivotal Software, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import json
import os
import unittest
import sys
import tempfile
import yaml

from contextlib import contextmanager
from StringIO import StringIO

from . import config
from .config import Config


@contextmanager
def capture_output():
	new_out, new_err = StringIO(), StringIO()
	old_out, old_err = sys.stdout, sys.stderr
	try:
		sys.stdout, sys.stderr = new_out, new_err
		yield sys.stdout, sys.stderr
	finally:
		sys.stdout, sys.stderr = old_out, old_err


class BaseTest(unittest.TestCase):
	def setUp(self):
		self.latest_stemcell_patcher = mock.patch('tile_generator.config.Config.latest_stemcell', return_value='1234')
		self.latest_stemcell = self.latest_stemcell_patcher.start()

		self._update_compilation_vm_disk_size_patcher = mock.patch('tile_generator.config.package_definitions.flag._update_compilation_vm_disk_size', return_value='1234')
		self._update_compilation_vm_disk_size = self._update_compilation_vm_disk_size_patcher.start()

		self.icon_file = tempfile.NamedTemporaryFile()
		self.config = Config(name='validname', icon_file=self.icon_file.name,
												 label='some_label', description='This is required')

	def tearDown(self):
		self.latest_stemcell_patcher.stop()
		self._update_compilation_vm_disk_size_patcher.stop()
		self.icon_file.close()


@mock.patch('tile_generator.config.Config.read_history')
class TestUltimateForm(BaseTest):
	def test_diff_final_config_obj(self, mock_read_history):
		test_path = os.path.dirname(__file__)
		cfg_file_path = os.path.join(test_path, 'test_sample_tile.yml')

		with mock.patch('tile_generator.config.CONFIG_FILE', cfg_file_path):
			cfg = self.config.read()
		cfg.set_version(None)
		cfg.set_verbose(False)
		cfg.set_sha1(False)
		cfg.set_cache(None)

		with open(test_path + '/test_config_expected_output.json', 'r') as f:
			expected_output = json.load(f)

		ignored_keys = ['history', 'icon_file', 'compilation_vm_disk_size','requires_cf_cli',
						'is_broker_app', 'is_decorator',
						'requires_meta_buildpack', 'is_static',
						'requires_docker_bosh', 'version']

		# Remove obsolete keys from expected output
		def remove_ignored_keys(obj):
			if type(obj) is dict:
				for k,v in obj.items():
					if k in ignored_keys:
						obj.pop(k)
					remove_ignored_keys(v)
			if type(obj) is list:
				for item in obj:
					remove_ignored_keys(item)

		def fix_path(obj):
			for release in obj['releases']:
				for package in release.get('packages', []):
					for f in package.get('files', []):
						if 'tile_generator/templates/src/common/utils.sh' in f.get('path'):
							f['path'] = 'tile_generator/templates/src/common/utils.sh'
						if 'tile_generator/templates/src/templates/all_open.json' in f.get('path'):
							f['path'] = 'tile_generator/templates/src/templates/all_open.json'

		# Massage expected output to be compared
		def handle_renamed_keys(obj):
			for release in obj['releases']:
				if release.get('consumes_cross_deployment'):
					release['consumes_for_deployment'] = release.pop('consumes_cross_deployment')
				if release.get('type'):
					release['package-type'] = release.pop('type')
				for package in release.get('packages', []):
					if package.get('type'):
						package['package-type'] = package.pop('type')
				for job in release.get('jobs', []):
					if job.get('package', {}).get('type'):
						job['package']['package-type'] = job['package'].pop('type')
			for package in obj['packages']:
				package['package-type'] = package.pop('type')

		remove_ignored_keys(expected_output)
		handle_renamed_keys(expected_output)
		fix_path(expected_output)

		# Convert releases to a list of dicts instead of dict of dicts
		cfg['releases'] = cfg['releases'].values()

		def new_comparer(expected, given, path):
			if type(expected) is dict:
				self.assertTrue(type(given) is dict, (path, 'Expected to be a dict, but got %s' % type(given)))
				for key in expected.keys():
					self.assertTrue(given.has_key(key), 'The key %s is missing' % (path % key))
					new_comparer(expected[key], given[key], path % key + '[%s]')

			elif type(expected) is list:
				total_length = len(expected)
				self.assertTrue(type(given) is list, (path, 'Expected to be a list, but got %s' % type(given)))
				self.assertEquals(total_length, len(given), (path, 'Expected to have length %s, but got %s' % (total_length, len(given))))
				for index in range(total_length):
					if type(expected[index]) is dict:
						if expected[index].has_key('name'):
							given_next = [e for e in given if e.get('name') == expected[index]['name']][0] or {}
						else:
							given_next = given[index]
						new_comparer(expected[index], given_next, path % index + '[%s]')
					elif type(expected[index]) is list:
						expected = sorted(expected)
						given = sorted(given)
						new_comparer(expected[index], given[index], path % index + '[%s]')
					else:
						self.assertIn(expected[index], given, (path % index, 'Expected value:\n%s\nIs missing' % expected[index]))

			else:
				self.assertEquals(expected, given, (path, 'Expected to have the value:\n%s\nHowever, instead got:\n%s' % (expected, given)))

		for release in cfg['releases']:
			if release.has_key('consumes_for_deployment'):
				self.assertDictEqual({'from': 'redis'}, release['consumes_for_deployment']['redis'])
				# Remove it so it is compatible with the OLD expected output
				release['consumes_for_deployment'].pop('redis')

		# Hacky way to turn config object into a plain dict
		d_cfg = json.loads(json.dumps(cfg))
		# Change the paths to files to be consistent
		fix_path(d_cfg)
		new_comparer(expected_output, d_cfg, '[%s]')

		# Just to be double sure :)
		expected = json.dumps(expected_output, sort_keys=True, indent=1).split('\n')
		remove_ignored_keys(d_cfg)
		generated = json.dumps(d_cfg, sort_keys=True, indent=1).split('\n')
		self.assertEquals(len(expected), len(generated))
		for line in expected:
			self.assertIn(line, generated)


class TestConfigValidation(BaseTest):
	def test_accepts_minimal_config(self):
		self.config.validate()

	def test_latest_stemcell_config(self):
		# Disable patching latest_stemcell
		self.latest_stemcell_patcher.stop()

		self.config.validate()

		# Enable so that tearDown does not barf
		self.latest_stemcell_patcher.start()

		# Ensure we are using the real latest_stemcell
		self.assertNotEquals(self.config['stemcell_criteria']['version'], '1234')

	def test_requires_package_names(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				self.config['packages'] = [{'name': 'validname', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}, {'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
				self.config.validate()
		self.assertIn("'name': ['required field']", err.getvalue())

	def test_requires_package_types(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				self.config['packages'] = [{'name': 'validname', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}, {'name': 'name'}]
				self.config.validate()
		self.assertIn("has invalid type None\nvalid types are", err.getvalue())

	def test_refuses_invalid_type(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				self.config['packages'] = [{'name': 'validname', 'type': 'nonsense'}]
				self.config.validate()
		self.assertIn("has invalid type nonsense\nvalid types are", err.getvalue())

	def test_accepts_valid_job_name(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'validname'}]}]
		self.config.validate()

	def test_accepts_valid_job_name_with_hyphen(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'valid-name'}]}]
		self.config.validate()

	def test_accepts_valid_job_name_with_underscore(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'valid_name'}]}]
		self.config.validate()

	def test_accepts_valid_job_name_with_number(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'valid2name'}]}]
		self.config.validate()

	def test_accepts_valid_job_name_with_capital(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'validName'}]}]
		self.config.validate()

	def test_accepts_valid_job_name_with_starting_capital(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'bosh-release', 'jobs': [{'name': 'Validname'}]}]
		self.config.validate()

	def test_accepts_valid_package_name(self):
		self.config['packages'] = [{'name': 'validname', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
		self.config.validate()

	def test_accepts_valid_package_name_with_hyphen(self):
		self.config['packages'] = [{'name': 'valid-name', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
		self.config.validate()

	def test_accepts_valid_package_name_with_hyphens(self):
		self.config['packages'] = [{'name': 'valid-name-too', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
		self.config.validate()

	def test_accepts_valid_package_name_with_number(self):
		self.config['packages'] = [{'name': 'valid-name-2', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
		self.config.validate()

	def test_refuses_spaces_in_package_name(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': 'invalid name', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
			self.config.validate()

	def test_refuses_capital_letters_in_package_name(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': 'Invalid', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
			self.config.validate()

	def test_refuses_underscores_in_package_name(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': 'invalid_name', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
			self.config.validate()

	def test_refuses_package_name_starting_with_number(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': '1-invalid-name', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
			self.config.validate()

	def test_requires_product_versions(self):
		self.config['packages'] = [{'name': 'packagename', 'type': 'app', 'manifest': {'buildpack': 'app_buildpack'}}]
		self.config.validate()
		self.assertIn('requires_product_versions', self.config.tile_metadata)
		requires_product_versions = self.config.tile_metadata['requires_product_versions']
		self.assertIn('name', requires_product_versions[0])
		self.assertIn('version', requires_product_versions[0])

	def test_refuses_docker_bosh_package_without_image(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{
				'name': 'bad-docker-bosh',
				'type': 'docker-bosh',
				'manifest': 'containers: [name: a]'
			}]
			self.config.validate()

	def test_accepts_docker_bosh_package_with_image(self):
		self.config['packages'] = [{
            'name': 'good-docker-bosh',
            'type': 'docker-bosh',
            'docker_images': ['my/image'],
            'manifest': 'containers: [name: a]'
        }]
		self.config.validate()

	def test_refuses_docker_bosh_package_without_manifest(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{
                'name': 'bad-docker-bosh',
                'type': 'docker-bosh',
                'docker_images': ['my/image']
            }]
			self.config.validate()

	def test_refuses_docker_bosh_package_with_bad_manifest(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{
                'name': 'bad-docker-bosh',
                'type': 'docker-bosh',
                'docker_images': ['my/image'],
                'manifest': '!^%'
            }]
			self.config.validate()

	def test_validates_docker_bosh_container_names(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{
				'name': 'good-docker-bosh',
				'type': 'docker-bosh',
				'docker_images': ['cholick/foo'],
				'manifest': '''
		containers:
		- name: bad-name
		  image: "cholick/foo"
		  bind_ports:
		  - '9000:9000'
	'''
			}]
			self.config.validate()

	def test_requires_buildpack_for_app_broker(self):
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': 'packagename', 'type': 'app', 'manifest': {}}]
			self.config.validate()
		with self.assertRaises(SystemExit):
			self.config['packages'] = [{'name': 'packagename', 'type': 'app-broker', 'manifest': {}}]
			self.config.validate()

	def test_buildpack_not_required_for_docker_app(self):
		self.config['packages'] = [{'name': 'packagename', 'type': 'docker-app', 'manifest': {}}]
		self.config.validate()


class TestVersionMethods(unittest.TestCase):

	def test_accepts_valid_semver(self):
		self.assertTrue(config.is_semver('11.2.25'))

	def test_accepts_valid_semver_with_prerelease(self):
		self.assertTrue(config.is_semver('11.2.25-alpha.1'))

	def test_accepts_valid_semver_with_config(self):
		self.assertTrue(config.is_semver('11.2.25+gb.23'))

	def test_accepts_valid_semver_with_prerelease_and_config(self):
		self.assertTrue(config.is_semver('11.2.25-alpha.1+gb.23'))

	def test_rejects_short_semver(self):
		self.assertFalse(config.is_semver('11.2'))

	def test_rejects_long_semver(self):
		self.assertFalse(config.is_semver('11.2.25.3'))

	def test_rejects_non_numeric_semver(self):
		self.assertFalse(config.is_semver('11.2.25dev1'))

	def test_initial_version(self):
		config = Config(history={})
		config.set_version(None)
		self.assertEquals(config['version'], '0.0.1')
		self.assertEquals(config.tile_metadata['product_version'], '0.0.1')

	def test_default_version_update(self):
		config = Config(history={'version':'1.2.3'})
		config.set_version(None)
		self.assertEquals(config['version'], '1.2.4')
		self.assertEquals(config.tile_metadata['product_version'], '1.2.4')

	def test_patch_version_update(self):
		config = Config(history={'version':'1.2.3'})
		config.set_version('patch')
		self.assertEquals(config['version'], '1.2.4')
		self.assertEquals(config.tile_metadata['product_version'], '1.2.4')

	def test_minor_version_update(self):
		config = Config(history={'version':'1.2.3'})
		config.set_version('minor')
		self.assertEquals(config['version'], '1.3.0')
		self.assertEquals(config.tile_metadata['product_version'], '1.3.0')

	def test_major_version_update(self):
		config = Config(history={'version':'1.2.3'})
		config.set_version('major')
		self.assertEquals(config['version'], '2.0.0')
		self.assertEquals(config.tile_metadata['product_version'], '2.0.0')

	def test_explicit_version_update(self):
		config = Config(history={'version':'1.2.3'})
		config.set_version('5.0.1')
		self.assertEquals(config['version'], '5.0.1')
		self.assertEquals(config.tile_metadata['product_version'], '5.0.1')

	def test_annotated_version_update(self):
		config = Config(history={'version':'1.2.3-alpha.1'})
		config.set_version('1.2.4')
		self.assertEquals(config['version'], '1.2.4')
		self.assertEquals(config.tile_metadata['product_version'], '1.2.4')

	def test_illegal_old_version_update(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				Config(history={'version':'nonsense'}).set_version('patch')
		self.assertIn('prior version must be in semver format', err.getvalue())

	def test_illegal_new_version_update(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				Config(history={'version':'1.2.3'}).set_version('nonsense')
		self.assertIn('Argument must specify', err.getvalue())

	def test_illegal_annotated_version_update(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out,err):
				Config(history={'version':'1.2.3-alpha.1'}).set_version(None)
		self.assertIn('The prior version was 1.2.3-alpha.1', err.getvalue())
		self.assertIn('and must not include a label', err.getvalue())

	def test_saves_initial_version(self):
		history = {}
		Config(history=history).set_version('0.0.1')
		self.assertEquals(history.get('version'), '0.0.1')
		self.assertEquals(len(history.get('history', [])), 0)

	def test_saves_initial_history(self):
		history = { 'version': '0.0.1' }
		Config(history=history).set_version('0.0.2')
		self.assertEquals(history.get('version'), '0.0.2')
		self.assertEquals(len(history.get('history')), 1)
		self.assertEquals(history.get('history')[0], '0.0.1')

	def test_saves_additional_history(self):
		history = { 'version': '0.0.2', 'history': [ '0.0.1' ] }
		Config(history=history).set_version('0.0.3')
		self.assertEquals(history.get('version'), '0.0.3')
		self.assertEquals(len(history.get('history')), 2)
		self.assertEquals(history.get('history')[0], '0.0.1')
		self.assertEquals(history.get('history')[1], '0.0.2')


class TestDefaultOptions(BaseTest):
	def test_purge_service_broker_is_true_by_default(self):
		self.config.update({'name': 'tile-generator-unittest'})
		self.config.validate()
		self.assertTrue(self.config['purge_service_brokers'])

	def test_purge_service_broker_is_overridden(self):
		self.config.update({'purge_service_brokers': False,
				 'name': 'tile-generator-unittest'})
		self.config.validate()
		self.assertFalse(self.config['purge_service_brokers'])

	def test_normalize_jobs_default_job_properties(self):
		self.config.update({
			'releases': {'my-job': {
				'jobs': [{
					'name': 'my-job'
				}]
			}}
		})
		self.config.normalize_jobs()
		self.assertEqual(self.config['releases']['my-job']['jobs'][0]['properties'], {})

	def test_default_metadata_version(self):
		self.config.update({'name': 'my-tile'})
		self.config.validate()
		self.assertEqual(self.config['metadata_version'], 1.8)

	def test_default_minimum_version_for_upgrade(self):
		self.config.update({})
		self.assertEqual(self.config.tile_metadata['minimum_version_for_upgrade'], '0.0.1')

	def test_default_rank(self):
		self.config.update({})
		self.assertEqual(self.config.tile_metadata['rank'], 1)

	def test_default_serial(self):
		self.config.update({})
		self.assertTrue(self.config.tile_metadata['serial'])


@mock.patch('os.path.getsize')
class TestVMDiskSize(BaseTest):
	def test_min_vm_disk_size(self, mock_getsize):
		# Don't patch _update_compilation_vm_disk_size_patcher
		self._update_compilation_vm_disk_size_patcher.stop()
		mock_getsize.return_value = 0
		self.config.update({'name': 'tile-generator-unittest'})
		self.config['packages'] = [{
			'name': 'validname', 'type': 'app',
			'manifest': {'buildpack': 'app_buildpack', 'path': 'foo'}
		}]
		expected_size = 10240
		with mock.patch('os.path.exists',return_value = True):
			self.config.validate()

		# Start so teardown does not break
		self._update_compilation_vm_disk_size_patcher.start()
		self.assertEqual(self.config['compilation_vm_disk_size'], expected_size)

	def test_big_default_vm_disk_size(self, mock_getsize):
		# Don't patch _update_compilation_vm_disk_size_patcher
		self._update_compilation_vm_disk_size_patcher.stop()
		self.config.update({'name': 'tile-generator-unittest'})
		self.config['packages'] = [{
			'name': 'validname', 'type': 'app',
			'manifest': {'buildpack': 'app_buildpack', 'path': 'foo'}
		}]
		default_package_size = 10240
		mock_getsize.return_value = default_package_size * 1024 * 1024 # megabytes to bytes.
		expected_size = 4 * default_package_size
		with mock.patch('os.path.exists', return_value=True):
			self.config.validate()

		# Start so teardown does not break
		self._update_compilation_vm_disk_size_patcher.start()
		self.assertEqual(self.config['compilation_vm_disk_size'], expected_size)

class TestTileName(BaseTest):
	def test_process_name_sets_name_in_tile_metadata(self):
		name = 'my-tile'
		self.config.update({'name': name})
		self.config.validate()
		self.assertIn('name', self.config.tile_metadata)
		self.assertEqual(self.config.tile_metadata['name'], name)

	def test_requires_product_name(self):
		with self.assertRaises(SystemExit):
			self.config.pop('name')
			self.config.validate()

	def test_accepts_valid_product_name_with_hyphen(self):
		self.config.update({'name': 'valid-name'})
		self.config.validate()

	def test_accepts_valid_product_name_with_hyphens(self):
		self.config.update({'name': 'valid-name-too'})
		self.config.validate()

	def test_accepts_valid_product_name_with_number(self):
		self.config.update({'name': 'valid-name-2'})
		self.config.validate()

	def test_accepts_valid_product_name_with_one_letter_prefix(self):
		self.config.update({'name': 'p-tile'})
		self.config.validate()

	def test_refuses_spaces_in_product_name(self):
		with self.assertRaises(SystemExit):
			self.config.update({'name': 'an invalid name'})
			self.config.validate()

	def test_refuses_capital_letters_in_product_name(self):
		with self.assertRaises(SystemExit):
			self.config.update({'name': 'Invalid'})
			self.config.validate()

	def test_refuses_underscores_in_product_name(self):
		with self.assertRaises(SystemExit):
			self.config.update({'name': 'invalid_name'})
			self.config.validate()

	def test_refuses_product_name_starting_with_number(self):
		with self.assertRaises(SystemExit):
			self.config.update({'name': '1-invalid-name'})
			self.config.validate()

class TestTileSimpleFields(BaseTest):
	def test_requires_label(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out, err):
				self.config.pop('label')
				self.config.validate()
		self.assertIn('label', err.getvalue())

	def test_sets_label(self):
		self.config.update({'label': 'my-label'})
		self.config.validate()
		self.assertIn('label',self.config.tile_metadata)
		self.assertEqual(self.config.tile_metadata['label'], 'my-label')

	def test_requires_description(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out, err):
				self.config.pop('description')
				self.config.validate()
		self.assertIn('description', err.getvalue())

	def test_sets_description(self):
		self.config.update({'description': 'my tile description'})
		self.config.validate()
		self.assertIn('description',self.config.tile_metadata)
		self.assertEqual(self.config.tile_metadata['description'], 'my tile description')

	def test_sets_metadata_version(self):
		self.config.update({'metadata_version': 1.8})
		self.config.validate()
		self.assertIn('metadata_version', self.config.tile_metadata)
		self.assertEqual(self.config.tile_metadata['metadata_version'], '1.8')

	def test_sets_service_broker(self):
		self.config.update({'service_broker': True})
		self.config.validate()
		self.assertIn('service_broker', self.config.tile_metadata)
		self.assertTrue(self.config.tile_metadata['service_broker'])


class TestTileIconFile(BaseTest):
	def test_requires_icon_file(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out, err):
				cfg = Config({})
				cfg.validate()
		self.assertIn('icon_file', err.getvalue())

	def test_refuses_empty_icon_file(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out, err):
				self.config['icon_file'] = None
				self.config.validate()
		self.assertIn('icon_file', err.getvalue())

	def test_refuses_invalid_icon_file(self):
		with self.assertRaises(SystemExit):
			with capture_output() as (out, err):
				self.config['icon_file'] = '/this/file/does/not/exist'
				self.config.validate()
		self.assertIn('icon_file', err.getvalue())

	def test_sets_icon_image(self):
		self.icon_file.write('foo')
		self.icon_file.flush()
		self.config.validate()
		self.assertIn('icon_image', self.config.tile_metadata)
		# Base64-encoded string from `echo -n foo | base64`
		self.assertEqual(self.config.tile_metadata['icon_image'], 'Zm9v')

if __name__ == '__main__':
	unittest.main()
