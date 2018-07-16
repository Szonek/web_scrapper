import parsers
from request_scrapper import NineGagParser




storage_dir = "C:\\Users\\szymon\\Desktop\memestok\\temp_folder"
#storage_dir = "c:/xampp/htdocs/memes_storage"

kwejk_parser = parsers.KwejkParser(storage_dir)
kwejk_parser.download_memes()

NineGagParser.downloadMemes(storage_dir)
