import unittest
from VFS import Virtual_System
from unittest.mock import patch
import io


class TestFileSystemStructure(unittest.TestCase):

    def setUp(self):
        self.captured_output = io.StringIO()
        self.patched_stdout = patch('sys.stdout', self.captured_output)  # Patch stdout
        self.patched_stdout.start()


        self.file_structure = {
            'system': {
                'type': 'folder',
                'access_rights': 'r-xr-xr-x',
                'list_f': {}
            },
            'etc': {
                'type': 'folder',
                'access_rights': 'r--r-----',
                'list_f': {
                    'bin': {
                        'type': 'folder',
                        'access_rights': 'rwxr-xr-x',
                        'list_f': {
                            'device_data.txt': {
                                'type': 'file',
                                'access_rights': 'rw-r-----'
                            }
                        }
                    },
                    'user': {
                        'type': 'folder',
                        'access_rights': 'rwxr-xr--',
                        'list_f': {
                            'desktop': {
                                'type': 'folder',
                                'access_rights': 'rwxr-xr--',
                                'list_f': {
                                    'user_data.txt': {
                                        'type': 'file',
                                        'access_rights': 'rw-r-----'
                                    }
                                }
                            },
                            'music': {
                                'type': 'folder',
                                'access_rights': 'rwxr-xr--',
                                'list_f': {}
                            }
                        }
                    }
                }
            }
        }
        self.fs = Virtual_System("system.zip")
        self.fs.file_structure = self.file_structure
        self.fs.current_dir = '/'


    def test_cd_command(self):
        self.fs.cd('~')

        self.fs.cd('etc/')
        self.assertEqual(self.fs.current_dir, '/etc/')

        self.fs.cd('~')
        self.assertEqual(self.fs.current_dir, '/')

        self.fs.cd('system/../etc/bin/.././bin')
        self.assertEqual(self.fs.current_dir, '/etc/bin/')


    def test_ls_command(self):
        self.fs.cd('~')

        path, directory_dict = self.fs.ls()
        self.assertEqual(path, '.')
        self.assertEqual(directory_dict, self.file_structure)

        path, directory_dict = self.fs.ls('etc/')
        expected_dict = \
                {
                    'bin':
                    {
                        'type': 'folder',
                        'access_rights': 'rwxr-xr-x',
                        'list_f':
                        {
                            'device_data.txt':
                            {
                                'type': 'file',
                                'access_rights': 'rw-r-----'
                            }
                        }
                    },
                    'user':
                    {
                        'type': 'folder',
                        'access_rights': 'rwxr-xr--',
                        'list_f':
                        {
                            'desktop':
                            {
                                'type': 'folder',
                                'access_rights': 'rwxr-xr--',
                                'list_f':
                                {
                                    'user_data.txt':
                                    {
                                        'type': 'file',
                                        'access_rights': 'rw-r-----'
                                    }
                                }
                            },
                            'music':
                            {
                                'type': 'folder',
                                'access_rights': 'rwxr-xr--',
                                'list_f':
                                {
                                }
                            }
                        }
                    }
                }
        self.assertEqual(path, 'etc/')
        self.assertEqual(directory_dict, expected_dict)

        path, directory_dict = self.fs.ls('system/')
        expected_dict = {}
        self.assertEqual(path, 'system/')
        self.assertEqual(directory_dict, expected_dict)

    def test_tac_command(self):
        self.fs.cd('~')

        test_lines=[b'AMD RYZEN 7000\r\n', b'3200x2100\r\n', b'120 gr\r\n', b'16 gb ram']
        self.fs.cd('etc/bin/')
        lines=self.fs.tac('device_data.txt')
        self.assertEqual(lines, test_lines)

        test_lines = [b'Latin\r\n', b'Andrey\r\n', b'Sergeevich']
        self.fs.cd('~')
        self.fs.cd('etc/user/desktop')
        lines = self.fs.tac('user_data.txt')
        self.assertEqual(lines, test_lines)

        self.fs.tac('file.txt')
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "\033[31m{}\033[0m".format(f"tac: file.txt: такого файла нет"))


    def test_chmod_command(self):
        self.fs.cd('~')

        self.fs.chmod('655', '..')
        output = self.captured_output.getvalue().strip()
        self.assertEqual(output, "\033[31m{}\033[0m".format(f"chmod: Права доступа домашнего каталога пользователя менять нельзя"))

        test_access = 'rw-rw-rw-'
        self.fs.chmod('666','etc')
        access = self.fs.file_structure['etc']['access_rights']
        self.assertEqual(test_access, access)

        test_access = 'r-xr-xr-x'
        self.fs.chmod('555', 'etc/bin/device_data.txt')
        access = self.fs.file_structure['etc']['list_f']['bin']['list_f']['device_data.txt']['access_rights']
        self.assertEqual(test_access, access)





if __name__ == '__main__':
    unittest.main()