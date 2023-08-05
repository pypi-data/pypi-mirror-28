import unittest, os
from time import sleep
from os import \
    rmdir as rmdir, \
    listdir as listdir,\
    remove as remove
from os.path import \
    join as join, \
    abspath as abspath, \
    split as split
from seaborn.file.file import *

TEST_PATH = split(abspath(__file__))[0]
TEST_DIRS = 'mkdir'
TEST_FILE = 'hello.wrld'
TEST_CONT = 'Hello\nWorld'

PATH_NAME = split(TEST_PATH)[1]

class test_file(unittest.TestCase):

    def test_mkdir(self):
        mkdir(join(TEST_PATH,TEST_DIRS))
        try:
            self.assertIn(TEST_DIRS, listdir(TEST_PATH))
        except BaseException as e:
            raise e
        finally:
            for i in listdir(join(TEST_PATH,TEST_DIRS)):
                remove(join(TEST_PATH,TEST_DIRS,i))
            rmdir(join(TEST_PATH, TEST_DIRS))

    def test_mkdir_for_file(self):
        mkdir_for_file(join(TEST_PATH, TEST_DIRS, TEST_FILE))
        try:
            self.assertIn(TEST_DIRS, listdir(TEST_PATH))
        except BaseException as e:
            raise e
        finally:
            for i in listdir(join(TEST_PATH,TEST_DIRS)):
                remove(join(TEST_PATH,TEST_DIRS,i))
            rmdir(join(TEST_PATH, TEST_DIRS))

    def test_find_folder(self):
        self.assertEqual(find_folder(PATH_NAME),TEST_PATH)

    def test_find_file(self):
        self.assertEqual(find_file(TEST_FILE),join(TEST_PATH,TEST_FILE))

    def test_sync_folder(self):
        os.mkdir(TEST_DIRS)
        sync_folder(TEST_PATH, join(TEST_PATH,TEST_DIRS))
        try:
            self.assertListEqual([TEST_FILE, 'test_file.py'],
                                 listdir(join(TEST_PATH,TEST_DIRS)))
        except BaseException as e:
            raise e
        finally:
            for i in listdir(join(TEST_PATH,TEST_DIRS)):
                remove(join(TEST_PATH,TEST_DIRS,i))
            rmdir(join(TEST_PATH,TEST_DIRS))

    def test_read_local_file(self):
        self.assertEqual(read_local_file(TEST_FILE),'Hello\nWorld')

    def test_relative_path(self):
        mkdir(join(TEST_PATH,TEST_DIRS))
        mkdir(join(TEST_PATH,TEST_DIRS,TEST_DIRS))
        try:
            self.assertEqual(
                relative_path(join(TEST_DIRS,TEST_DIRS)),
                join(TEST_PATH,TEST_DIRS,TEST_DIRS))
        except BaseException as e:
            raise e
        finally:
            rmdir(join(TEST_PATH,TEST_DIRS,TEST_DIRS))
            rmdir(join(TEST_PATH,TEST_DIRS))

    def test_mdate(self):
        tested = open('_'+TEST_FILE, 'w')
        first = mdate('_'+TEST_FILE)
        sleep(.5)
        self.assertEqual(first, mdate('_'+TEST_FILE))
        tested.close()
        remove(join(TEST_PATH,'_'+TEST_FILE))

    def test_read_file(self):
        self.assertEqual(read_file(join(TEST_PATH,TEST_FILE)),TEST_CONT)

    def test_copy_file(self):
        copy_file(TEST_FILE, '_'+TEST_FILE)
        try:
            self.assertEqual(''.join([i for i in open('_'+TEST_FILE).read()]),
                            TEST_CONT)
        except BaseException as e:
            raise e
        finally:
            remove(join(TEST_PATH,'_'+TEST_FILE))

    def test_read_folder(self):
        self.assertEqual(read_folder(TEST_PATH)[TEST_FILE],TEST_CONT)

if __name__ == '__main__':
    unittest.main()