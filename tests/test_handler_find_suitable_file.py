import shutil
import unittest
from pathlib import Path

from gemtoolsconfig.handlers import get_find_suitable_file_handler

TEMP_DIR = Path('tmp_handler_suitable')


class TestHandlerFindSuitableFile(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(exist_ok=True, parents=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    def test_valid(self):
        # Setup
        (TEMP_DIR / 'config.toml').write_text('key = "value"')

        # Test
        handler = get_find_suitable_file_handler(TEMP_DIR)
        result = handler({'name': 'config'})
        self.assertEqual({'name': 'config', 'path': 'config.toml'}, result)

    def test_not_found(self):
        handler = get_find_suitable_file_handler(TEMP_DIR)
        with self.assertRaises(FileNotFoundError):
            handler({'name': 'not_found'})

    def test_directory_not_found(self):
        with self.assertRaises(NotADirectoryError):
            get_find_suitable_file_handler(Path('not_found'))
