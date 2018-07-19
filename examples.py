import parsers
from request_scrapper import NineGagParser
from config_reader import ConfigParser

cp = ConfigParser()
print(cp.project_name())
print(cp.path_on_disk_for_memes())
print(cp.download_images())
print(cp.download_jsons())
print(cp.make_folders_for_meme_download_date())
print(cp.make_folders_for_meme_pages())
print(cp.tests_can_download_memes())


# DELETE THIS
#storage_dir = "C:\\Users\\szymon\\Desktop\memestok\\temp_folder"
#storage_dir = "c:/xampp/htdocs/memes_storage"
#

# No need to update AllParsers code, when added new parser.
# New parser need to be added to parsers.py and have name <WebPageName>Parser
#ap = parsers.AllParsers(['Kwejk', 'Test'])
#ap.download_memes()

kwejk_parser = parsers.KwejkParser()
kwejk_parser.download_memes()



#NineGagParser.downloadMemes(storage_dir)  # PLEASE DELETE STROAGE_DIR ARGUMENT
# TODO: PLEASE MOVE NineGagParser to parsers.py (between kwejk parser and AllParsers class)
# TODO: NAME CONVENTION!
# TODO: MAKE BASE CLASS WITH VIRTUAL METHOD download_memes() FOR THIS TYPE OF PARSER. (like its done for kwejk_praser now)
