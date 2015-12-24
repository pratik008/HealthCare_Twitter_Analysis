from auth_manager import AuthManager
from tag_manager import TagManager
from logger import Logger
from custom_listener import CustomListener
from custom_stream import CustomStream


CREDENTIALS_FILE_PATH = '../resources/credentials.json'
TAG_FILE_PATH = '../resources/tagsList.txt'
DATA_DIRECTORY = '../data'
MAIN_PROGRAM_FILE_PATH = 'stream_tweets_main.py'
LOG_FILE_DIRECTORY = '../log'


if __name__ == '__main__':

    auth_manager = AuthManager(CREDENTIALS_FILE_PATH)
    num_handlers = len(auth_manager.auth_handlers)
    tag_manager = TagManager(TAG_FILE_PATH, num_handlers)
    logger = Logger(LOG_FILE_DIRECTORY)

    for i in xrange(num_handlers):
        listener = CustomListener(i, DATA_DIRECTORY, MAIN_PROGRAM_FILE_PATH, logger)
        stream = CustomStream(listener, auth_manager.auth_handlers[i], tag_manager.distributed_tag_list[i])
        stream.stream(async=True)
