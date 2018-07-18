import json
import hashlib
from error_logger import Logger
from datetime import date, datetime
from html_getter import HtmlGetter
import os


class Utils:

    @staticmethod
    def calc_meme_hash(id):
        return hashlib.sha224(id).hexdigest()

    @staticmethod
    def get_current_date():
        today = date.today()
        return today.strftime("%d/%m/%Y")


class MemeInfo:
    """
    Struct with basic information about parsed meme.
    """
    def __init__(self, title="", id="", web_page_name="",
                 url_to_img="", url_to_meme="", author="",
                 category=[], tags=[]):
        Logger.is_istance(title, str)
        Logger.is_istance(id, str)
        Logger.is_istance(web_page_name, str)
        Logger.is_istance(url_to_img, str)
        Logger.is_istance(url_to_meme, str)
        Logger.is_istance(author, str)
        Logger.is_istance(category, list)
        Logger.is_istance(tags, list)
        self.title = title  # str
        self.id = id  # array of str. Index 0 says about original first meme.
        self.web_page_name = web_page_name  # array of str
        self.url_to_img = url_to_img  # str (raw link to image)
        self.url_to_meme = url_to_meme  # str   its url to page with meme (with comments etc)
        self.author_id = author  # str (author of first meme)
        self.category = category  # array of str
        self.tags = tags  # array of str
        self.histogram_hash = ""  # str
        self.__json = {}
        self.__json_calculated = False

    def __calc_json(self):
        if self.__json_calculated is False:
            self.__json['title'] = self.title
            self.__json['uuid'] = Utils.calc_meme_hash(self.id.encode('utf-8'))
            self.__json['id'] = self.id
            self.__json['web_page'] = self.web_page_name
            self.__json['url_to_image'] = self.url_to_img
            self.__json['url_to_meme'] = self.url_to_meme
            self.__json['author'] = self.author_id
            self.__json['category'] = self.category
            self.__json['tags'] = self.tags
            self.__json['histogram_hash'] = self.histogram_hash
            self.__json['download_date'] = Utils.get_current_date()
            self.__json_calculated = True
        else:
            pass

    def __save_json(self, path):
        if self.__json_calculated is False:
            self.__calc_json()
        with open(path + ".json", 'w') as f:
            json.dump(self.__json, f, sort_keys=True, indent=4, ensure_ascii=False)

    def save_on_disk(self):
        storage_dir = "C:\\Users\\szymon\\Desktop\memestok\\temp_folder"  # TODO: make config file and get rid of this
        # storage_dir = "c:/xampp/htdocs/memes_storage"
        image_raw = HtmlGetter.simple_get(self.url_to_img)
        now = datetime.now()
        path_to_save = storage_dir + os.sep + self.web_page_name + os.sep \
            + str(now.year) + os.sep + str(now.month) + os.sep + str(now.day)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        path_to_save = path_to_save + os.sep + self.id
        with open(path_to_save + ".jpg", 'wb') as f:
            f.write(image_raw)
        self.__save_json(path_to_save)

