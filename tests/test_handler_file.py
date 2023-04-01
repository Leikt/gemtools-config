import shutil
import unittest
from pathlib import Path

from gemtoolsio import generate_key, encrypt_file

from gemtoolsconfig.handlers import get_file_handler

TEMP_DIR = 'tmp'


class TestHandlerFile(unittest.TestCase):
    def setUp(self):
        self.directory = Path(TEMP_DIR)
        self.directory.mkdir(exist_ok=True, parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    def test_get_file_handler(self):
        # Setup
        (self.directory / 'config.toml').write_text('key1 = "value1"\n[section]\nkey2 = "value2"')

        # Test
        handler = get_file_handler(self.directory)
        result = handler({'path': 'config.toml'})
        expected_result = {'key1': 'value1', 'section': {'key2': 'value2'}}
        self.assertEqual(expected_result, result['__result__'])
        self.assertEqual(self.directory / 'config.toml', result['full_path'])

    def test_get_file_handler_encryption(self):
        # Setup
        (self.directory / 'config.toml').write_text('key1 = "value1"\n[section]\nkey2 = "value2"')
        key = generate_key()
        encrypt_file((self.directory / 'config.toml'), key)

        # Test
        handler = get_file_handler(self.directory, key)
        result = handler({'path': 'config.toml'})
        expected_result = {'key1': 'value1', 'section': {'key2': 'value2'}}
        self.assertEqual(expected_result, result['__result__'])
        self.assertEqual(self.directory / 'config.toml', result['full_path'])

    def test_directory_not_found(self):
        with self.assertRaises(NotADirectoryError):
            get_file_handler(Path('not_found'))

    def test_nested_files(self):
        # Setup
        (self.directory / 'somedir').mkdir(exist_ok=True, parents=True)
        (self.directory / 'somedir' / 'config.toml').write_text('key1 = "value1"\n[section]\nkey2 = "value2"')

        # Test
        handler = get_file_handler(self.directory)
        result = handler({'path': 'somedir/config.toml'})
        expected_result = {'key1': 'value1', 'section': {'key2': 'value2'}}
        self.assertEqual(expected_result, result['__result__'])
        self.assertEqual(self.directory / 'somedir' / 'config.toml', result['full_path'])
