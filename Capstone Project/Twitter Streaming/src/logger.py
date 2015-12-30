import os
from datetime import datetime


class Logger:

    def __init__(self, log_file_dir):
        self.log_file_dir = log_file_dir

    def log(self, error_code, index, error_message):
        dir = self.log_file_dir
        if not os.path.exists(dir):
            os.makedirs(dir)

        now = datetime.utcnow()
        error_message = '' if error_message is None else error_message
        message = 'Error code {0} | Stream {1} | {2} | {3}\n'.format(error_code, index, now, error_message)

        log = open('{0}/{1}.log'.format(dir, now.strftime('%Y-%m-%d')), 'a')
        log.write(message)
        log.close()
