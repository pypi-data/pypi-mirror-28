import unittest, os
from time import sleep
from os import rmdir, listdir, remove, chdir
from os.path import join, abspath, split
from seaborn.file.file import *

TEST_PATH = split(abspath(__file__))[0]
TEST_DIRS = 'mkdir'
TEST_DATA = 'data'
TEST_FILE = 'hello.wrld'
TEST_CONT = 'Hello\nWorld'
TEST_CODE = 'test_file.py'

PATH_NAME = split(TEST_PATH)[1]

def cleanup(path=TEST_DIRS):
    queue = listdir(join(TEST_PATH,path))
    for item in queue:
        if '.' in item:
            remove(join(TEST_PATH,path,item))
        else:
            cleanup(join(path,item))
    rmdir(join(TEST_PATH,path))

class test_file(unittest.TestCase):

    def test_mkdir(self):
        mkdir(join(TEST_PATH,TEST_DIRS))
        try:
            self.assertIn(TEST_DIRS, listdir(TEST_PATH))
        except BaseException as e:
            raise e
        finally:
            cleanup()

    def test_mkdir_for_file(self):
        mkdir_for_file(join(TEST_PATH, TEST_DIRS, TEST_FILE))
        try:
            self.assertIn(TEST_DIRS, listdir(TEST_PATH))
        except BaseException as e:
            raise e
        finally:
            cleanup()

    def test_find_folder(self):
        self.assertEqual(find_folder(PATH_NAME),TEST_PATH)

    def test_find_file(self):
        self.assertEqual(find_file(TEST_CODE),
                         join(TEST_PATH,TEST_CODE))

    def test_sync_folder(self):
        os.mkdir(TEST_DIRS)
        sync_folder(TEST_PATH, join(TEST_PATH,TEST_DIRS))
        try:
            self.assertListEqual([TEST_DATA, 'test_file.py'],
                                 listdir(join(TEST_PATH,TEST_DIRS)))
        except BaseException as e:
            raise e
        finally:
            cleanup()

    def test_read_local_file(self):
        self.assertEqual(read_local_file(join(TEST_DATA,TEST_FILE)),
                         'Hello\nWorld')

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
            cleanup()

    def test_mdate(self):
        tested = open('_'+TEST_FILE, 'w')
        first = mdate('_'+TEST_FILE)
        sleep(.5)
        self.assertEqual(first, mdate('_'+TEST_FILE))
        tested.close()
        remove(join(TEST_PATH,'_'+TEST_FILE))

    def test_read_file(self):
        self.assertEqual(read_file(join(TEST_PATH,TEST_DATA,TEST_FILE)),
                         TEST_CONT)

    def test_copy_file(self):
        copy_file(join(TEST_DATA,TEST_FILE), '_'+TEST_FILE)
        try:
            self.assertEqual(''.join([i for i in open('_'+TEST_FILE).read()]),
                            TEST_CONT)
        except BaseException as e:
            raise e
        finally:
            remove(join(TEST_PATH,'_'+TEST_FILE))

    def test_read_folder(self):
        actual = read_folder(TEST_PATH)
        test = {k.replace('/','\\'):v for k, v in actual.items()}
        self.assertEqual(TEST_CONT,test[join(TEST_DATA,TEST_FILE)])

if __name__ == '__main__':
    unittest.main()