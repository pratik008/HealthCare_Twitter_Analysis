from auth_manager import AuthManager
from tag_manager import TagManager
from logger import Logger
from custom_listener import CustomListener
from custom_stream import CustomStream
import os
import sys

CREDENTIALS_FILE_PATH = 'resources/credentials.json'
TAG_FILE_PATH = 'resources/tagsList.txt'
MAIN_PROGRAM_FILE_PATH = 'stream_tweets_main.py'


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "$ stream_tweets_main [downloadFolder]"
        quit()
    DATA_DIRECTORY = os.path.join(sys.argv[1])
    LOG_FILE_DIRECTORY = os.path.join(sys.argv[1],'log')
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
    if not os.path.exists(LOG_FILE_DIRECTORY):
        os.makedirs(LOG_FILE_DIRECTORY)

    auth_manager = AuthManager(CREDENTIALS_FILE_PATH)
    num_handlers = len(auth_manager.auth_handlers)
    tag_manager = TagManager(TAG_FILE_PATH, num_handlers)
    logger = Logger(LOG_FILE_DIRECTORY)

    for i in xrange(num_handlers):
        listener = CustomListener(i, DATA_DIRECTORY, MAIN_PROGRAM_FILE_PATH, logger)
        stream = CustomStream(listener, auth_manager.auth_handlers[i], tag_manager.distributed_tag_list[i])
        stream.stream(async=True)

# TODO: Handle error (disconnected from internet)
