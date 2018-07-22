from urllib.request import urlopen, urlretrieve
from urllib.error import URLError, HTTPError
import json
import datetime
import os

class NineGagParser:
    urlHot = "https://9gag.com/v1/group-posts/group/default/type/hot"

    @staticmethod
    def downloadMemes(storageDir):
        try:
            response = urlopen(NineGagParser.urlHot).read()
            responseJson = json.loads(response)
            if responseJson['meta']['status'] != 'Success':
                print('Error (9gag)')
                return
            now = datetime.datetime.now()
            storageDirSite = storageDir + os.sep + '9gag' + os.sep + str(now.year) + os.sep + str(now.month)
            if not os.path.exists(storageDirSite):
                os.makedirs(storageDirSite)
            for post in responseJson['data']['posts']:
                # skip gifs
                if post['type'] != 'Photo':
                    continue
                # save meme data to json file
                memePath = storageDirSite + os.sep + post['id']
                with open(memePath + '.json', 'w') as jsonFile:
                    json.dump(post, jsonFile)
                # download meme image
                imageUrl = post['images']['image700']['url']
                urlretrieve(imageUrl, memePath + '.jpg')
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        except Exception as e:
            print('Error: ', str(e))
