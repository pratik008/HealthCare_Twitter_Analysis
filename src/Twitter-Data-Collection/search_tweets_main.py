from auth_manager import AuthManager
from tag_manager import TagManager
from logger import Logger
from tweets_downloader import TweetsDownloader
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "$ search_tweets_main [destinationFolder] [credentials] [tagList]"
        quit()
    DATA_DIRECTORY = os.path.join(sys.argv[1])
    LOG_FILE_DIRECTORY = os.path.join(sys.argv[1],'log')
    CREDENTIALS_FILE_PATH = os.path.join(sys.argv[2])
    TAG_FILE_PATH = os.path.join(sys.argv[3])
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
    if not os.path.exists(LOG_FILE_DIRECTORY):
        os.makedirs(LOG_FILE_DIRECTORY)
    
    auth_manager = AuthManager(CREDENTIALS_FILE_PATH)
    num_handlers = len(auth_manager.auth_handlers)
    tag_manager = TagManager(TAG_FILE_PATH, num_handlers)
    logger = Logger(LOG_FILE_DIRECTORY)
    for tag in tag_manager.tag_list:
        TweetsDownloader(DATA_DIRECTORY,tag,auth_manager)