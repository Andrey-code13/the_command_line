from zipfile import ZipFile
import sys
import argparse
import zipfile
import os


# Virtual File System
class Virtual_System:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_dir = '/'
        self.file_structure = {}
        self.load_zip()

    def load_zip(self):
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            for obj_path in z.namelist():
                parts = obj_path.strip('/').split('/')
                current_level = self.file_structure
                for part in parts:
                    if part == parts[-1] and not obj_path.endswith('/'):
                        current_level[part] = "f"
                    else:
                        current_level = current_level.setdefault(part, {})




