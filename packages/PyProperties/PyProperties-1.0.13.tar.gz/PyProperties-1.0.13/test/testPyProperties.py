# coding=utf-8

import os
import unittest
from PyProperties import PyProperties


class PyPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_demo(self):
        self.assertTrue(self, True)
        self.assertEqual('test_demo', 'test_demo', 'test_demo read wrong!')

    def test_load(self):
        properties = PyProperties(os.path.abspath('./') + '/resources/test.properties')
        self.assertEqual(properties['key_ha_ha'], 'key_ha_ha')
        self.assertEqual(properties['key_wa'], '大户')

    def test_save(self):
        properties = PyProperties(os.path.abspath('./') + '/resources/test.properties')
        properties.save(os.path.abspath('./') + '/resources/test_1.properties')
        source_file = open(os.path.abspath('./') + '/resources/test.properties', 'r')
        save_file = open(os.path.abspath('./') + '/resources/test_1.properties', 'r')
        source_file_content = source_file.readlines()
        source_file.close()
        save_file_content = save_file.readlines()
        save_file.close()
        try:
            self.assertIsNotNone(save_file_content)
            self.assertIsNotNone(source_file_content)
            self.assertEqual(len(save_file_content), len(source_file_content))
            for i in range(0, len(save_file_content)):
                self.assertEqual(save_file_content[i].rstrip(os.linesep), source_file_content[i].rstrip(os.linesep))
        finally:
            os.remove(os.path.abspath('./') + '/resources/test_1.properties')

    def tearDown(self):
        pass


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(PyPropertiesTestCase)

if __name__ == '__main__':
    unittest.main()
