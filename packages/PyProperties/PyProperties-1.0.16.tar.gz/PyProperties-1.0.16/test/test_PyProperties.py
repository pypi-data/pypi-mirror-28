# coding=utf-8

import os
import unittest

from py_properties import PyProperties


class PyPropertiesTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = __file__[0:__file__.rfind(os.sep)]
        print 'self.dir: %s' % self.dir

    def test_demo(self):
        self.assertTrue(self, True)
        self.assertEqual('test_demo', 'test_demo', 'test_demo read wrong!')

    def test_load(self):
        properties = PyProperties(self.dir + '/resources/test.properties')
        self.assertEqual(properties['key_ha_ha'], 'key_ha_ha')
        self.assertEqual(properties['key_wa'], '大户')

    def test_save(self):
        properties = PyProperties(self.dir + '/resources/test.properties')
        properties.save(self.dir + '/resources/test_1.properties')
        source_file = open(self.dir + '/resources/test.properties', 'r')
        save_file = open(self.dir + '/resources/test_1.properties', 'r')
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
            os.remove(self.dir + '/resources/test_1.properties')

    def tearDown(self):
        pass


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(PyPropertiesTestCase)

if __name__ == '__main__':
    unittest.main()
