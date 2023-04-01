import shutil
import unittest
from pathlib import Path

from gemtoolsconfig.handlers import _find_suitable_file

TEMP_DIR = Path('tmp_suitable_file')


class TestFindSuitableFile(unittest.TestCase):
    def setUp(cls) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    def test_valid(self):
        # Setup
        (TEMP_DIR / 'config.toml').write_text('azerty')

        # Test
        result = _find_suitable_file(TEMP_DIR, 'config')
        self.assertEqual('config.toml', result)

    def test_valid_suffix(self):
        # Setup
        (TEMP_DIR / 'config.toml').write_bytes('azerty'.encode())

        # Test
        result = _find_suitable_file(TEMP_DIR, 'config')
        self.assertEqual('config.toml', result)

    def test_no_suitable_file(self):
        with self.assertRaises(FileNotFoundError):
            _find_suitable_file(TEMP_DIR, 'not_found')
