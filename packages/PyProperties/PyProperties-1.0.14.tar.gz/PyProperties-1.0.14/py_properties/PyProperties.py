# coding=utf-8

import os


class PyProperties:

    def __init__(self, path=None):
        self.__properties__ = {}
        self.__lines__ = []
        if not path:
            return
        self.load(path)

    def __setitem__(self, key, value):
        self.__properties__[key] = value

    def __getitem__(self, item):
        return self.__properties__.get(item)

    def load(self, path):
        self.__properties__ = {}
        self.__lines__ = []
        if not path or not os.path.exists(path):
            return
        path_file = open(path, 'r')
        if not path_file:
            return
        for line in path_file:
            line = line.rstrip(os.linesep)
            self.__lines__.append(line)
            if not line:
                continue
            if line.startswith('#'):
                continue
            equal_position = line.find('=')
            if equal_position > 0:
                self[line[0:equal_position]] = line[equal_position + 1:]
        print 'load, len of lines: %d.' % len(self.__lines__)

    def save(self, path):
        if not self.__lines__:
            return
        if os.path.exists(path):
            os.remove(path)
        path_file = open(path, 'a')
        if not path_file:
            return
        print 'save, len of lines: %d.' % len(self.__lines__)
        for i in range(0, len(self.__lines__)):
            if not self.__lines__[i]:
                path_file.write('' + '\n')
                continue
            if self.__lines__[i].startswith('#'):
                path_file.write(self.__lines__[i] + '\n')
                continue
            equal_position = self.__lines__[i].find('=')
            if equal_position > 0:
                path_file.write(self.__lines__[i][0:equal_position] + '=' + self.__properties__[self.__lines__[i][0:equal_position]] + '\n')
                continue
            path_file.write(self.__lines__[i] + '\n')
