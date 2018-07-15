import json


class MemeInfo:
    """
    Struct with basic information about parsed meme.
    """
    def __init__(self, title, id, web_page_name, url_to_meme, author, category, tags):
        self.title = title  # str
        self.id = id  # str
        self.web_page_name = web_page_name  # str
        self.url_to_meme = url_to_meme  # str
        self.author_id = author  # str
        self.category = category  # str
        self.tags = tags  # array of str
        self.__json = {}
        self.__json_calculated = False

    def __calc_json(self):
        if self.__json_calculated is False:
            self.__json['title'] = self.title
            self.__json['id'] = self.id
            self.__json['web_page'] = self.web_page_name
            self.__json['url'] = self.url_to_meme
            self.__json['author'] = self.author_id
            self.__json['category'] = self.category
            self.__json['tags'] = self.tags
            self.__json_calculated = True
        else:
            pass

    def save_json(self, path):
        if self.__json_calculated is False:
            self.__calc_json()
        with open(path + ".json", 'w') as f:
            json.dump(self.__json, f, sort_keys = True, indent = 4, ensure_ascii=False)
