import zipfile


class Virtual_System:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_dir = '/'
        self.file_structure = {}
        self.load_zip()

    def load_access_rights(self):
        access_rights={}
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            with z.open('access_rights.txt') as f:
                for line in f:
                    parts = line.decode().strip().split()
                    if len(parts) == 2:
                        filename, rights = parts
                        access_rights[filename] = rights
        return access_rights

    def load_zip(self):
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            rights_dict = self.load_access_rights()
            for obj_path in z.namelist():
                if obj_path == 'access_rights.txt':
                    continue
                parts = obj_path.strip('/').split('/')
                current_level = self.file_structure
                for part in parts:
                    is_file = part == parts[-1] and not obj_path.endswith('/')
                    if is_file:
                        current_level[part] = {
                            "type": "file",
                            "access_rights": rights_dict.get(part, None)
                        }
                    else:
                        if part not in current_level:
                            current_level[part] = {
                                "type": "folder",
                                "access_rights": rights_dict.get(part, None),
                                "list_f": {}
                            }
                        current_level = current_level[part]["list_f"]


    def cd(self, path):
        if path == '~':
            self.current_dir = '/'
            return
        parsed_path = self.path_parser(path)
        if self.get_dictionary_from_absolute_path(parsed_path) is None:
            print("\033[31m{}\033[0m".format(f"cd: {path}: такого каталога нет"))
        else:
            self.current_dir = parsed_path

    def path_parser(self, path):
        if path.startswith("/"):
            abs_path = path
        else:
            abs_path = self.current_dir + path

        parts = abs_path.split('/')
        final_parts = []
        for part in parts:
            if part == '' or part == '.':
                continue
            elif part == "..":
                if final_parts:
                    final_parts.pop()
            else:
                final_parts.append(part)

        final_path = '/' + '/'.join(final_parts) + '/'

        final_path = final_path.replace('//', '/')
        if final_path == '':
            final_path = '/'
        return final_path

    def get_dictionary_from_absolute_path(self,path):
        if path == "/":
            return self.file_structure
        parts = path.strip('/').split('/')
        current_level = self.file_structure
        for part in parts:
            if part in current_level:
                if current_level[part]["type"] == "folder":
                    current_level = current_level[part]["list_f"]
                else:
                    return None
            else:
                return None
        return current_level

    def pwd(self):
        return self.current_dir

    def ls(self, path="."):
        parsed_path = self.path_parser(path)
        directory_dict = self.get_dictionary_from_absolute_path(parsed_path)

        return path, directory_dict

    def tac(self, filename):
        current_directory_dict = self.get_dictionary_from_absolute_path(self.current_dir)

        if current_directory_dict is None or filename not in current_directory_dict:
            print("\033[31m{}\033[0m".format(f"tac: {filename}: такого файла нет"))
            return

        if current_directory_dict[filename]['type'] != "file":
            print("\033[31m{}\033[0m".format(f"tac: {filename}: это не файл"))
            return

        file_path_in_zip = self.current_dir.strip('/') +'/'+ filename
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            if file_path_in_zip not in z.namelist():
                print("\033[31m{}\033[0m".format(f"tac: {filename}: такого файла нет в архиве"))
                return

            with z.open(file_path_in_zip) as file:
                lines = file.readlines()
                return lines

    def chmod(self,mode,path):
        rights_map = {
            '0': '---',
            '1': '--x',
            '2': '-w-',
            '3': '-wx',
            '4': 'r--',
            '5': 'r-x',
            '6': 'rw-',
            '7': 'rwx',
        }
        new_rights = ''
        abs_path = self.path_parser(path).strip('/')
        for digit in mode:
            new_rights += rights_map[digit]
        if abs_path.find('/')!=-1:
            name_dict=abs_path[abs_path.rfind('/')+1:]
            target_dict = self.get_dictionary_from_absolute_path(abs_path[:abs_path.rfind('/')])
        else:
            name_dict=abs_path
            target_dict = self.get_dictionary_from_absolute_path(self.current_dir)

        if name_dict=='':
            print("\033[31m{}\033[0m".format(f"chmod: Права доступа домашнего каталога пользователя менять нельзя"))
            return
        if target_dict is None or name_dict not in target_dict:
            print("\033[31m{}\033[0m".format(f"chmod: {path}: такого файла или каталога нет"))
            return
        if 'type' in target_dict[name_dict]:
            target_dict[name_dict]['access_rights'] = new_rights
            print("\033[33m{}\033[0m".format(f"Права доступа для '{path}' изменены на '{mode}'"))
        else:
            print("\033[31m{}\033[0m".format(f"chmod: {path}: такого файла или каталога нет"))