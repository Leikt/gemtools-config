import shutil
import unittest
from pathlib import Path

from gemtoolsio import encrypt_file, generate_key

from gemtoolsconfig.presets import preset_file_loader

TEMP_DIR = Path('tmp_preset_file')


class TestPresetFile(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

    def test_not_encrypted(self):
        # Setup
        (TEMP_DIR / 'config.toml').write_text('key = "value"')

        # Test
        loader = preset_file_loader(TEMP_DIR)
        result = loader.load(path='config.toml')
        self.assertEqual({'key': 'value'}, result)

        result = loader.lazy_load('config')
        self.assertEqual({'key': 'value'}, result)

    def test_encrypted(self):
        # Setup
        (TEMP_DIR / 'config.toml').write_text('key = "value"')
        key = generate_key(TEMP_DIR / 'dummy.key')
        encrypt_file(TEMP_DIR / 'config.toml', key)

        # Test
        loader = preset_file_loader(TEMP_DIR, key_file=TEMP_DIR / 'dummy.key')
        result = loader.load(path='config.toml')
        self.assertEqual({'key': 'value'}, result)

        result = loader.lazy_load('config')
        self.assertEqual({'key': 'value'}, result)


