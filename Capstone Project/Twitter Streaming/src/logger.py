import os
from datetime import datetime


class Logger:

    def __init__(self, log_file_dir):
        self.log_file_dir = log_file_dir

    def log(self, error_code, index):
        dir = self.log_file_dir
        if not os.path.exists(dir):
            os.makedirs(dir)

        now = datetime.utcnow()

        message = 'Error code {0} | Stream {1} | {2}\n'.format(error_code, index, now)

        log = open('{0}/{1}.log'.format(dir, now.strftime('%Y-%m-%d')), 'a')
        log.write(message)
        log.close()