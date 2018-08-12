import parsers
from config_reader import ConfigParser
from tests import WebScrapperTester

cp = ConfigParser()
print(cp.project_name())
print(cp.path_on_disk_for_memes())
print(cp.download_images())
print(cp.download_jsons())
print(cp.make_folders_for_meme_download_date())
print(cp.make_folders_for_meme_pages())
print(cp.tests_can_download_memes())




#tester = WebScrapperTester()
#tester.test_ninegag_download()

# ONLY KWEJK PARSER
#kwejk_parser = parsers.KwejkParser()
#kwejk_parser.download_memes()

# ONLY 9GAG PARSER
#ninegag_parser = NineGagParser()
#ninegag_parser.download_memes()
