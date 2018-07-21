import os
import sys
import inspect

class ConfigParser:
    """
    Reader config.ini from utils folder.

    Example of how to add new config:
    1. Add new config to config.ini:
    new_config_options = abc  (also can be int 0 or 1)
    2. Please add function using this template:
    def new_config_options(self);
        return self._config[self.__get_func_name()]
    3. Done.
    """
    def __init__(self):
        self._path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "utils" + os.sep + "config.ini"
        with open(self._path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        self._config = {}
        for line in content:
            value = line[:line.find(" ")]
            key = line[line.find("= ")+2:]
            self._config[value] = self.__parse_key(key)

    def __parse_key(self, key):
        try:
            return bool(int(key))
        except ValueError:
            return str(key)

    def __get_func_name(self):
        return inspect.stack()[1][3]

    def project_name(self):
        return self._config[self.__get_func_name()]

    def path_on_disk_for_memes(self):
        return self._config[self.__get_func_name()]

    def download_images(self):
        return self._config[self.__get_func_name()]

    def download_jsons(self):
        return self._config[self.__get_func_name()]

    def make_folders_for_meme_pages(self):
        return self._config[self.__get_func_name()]

    def make_folders_for_meme_download_date(self):
        return self._config[self.__get_func_name()]

    def tests_can_download_memes(self):
        return self._config[self.__get_func_name()]

