from pymongo import MongoClient
import os
import json
import shutil
import argparse
from utility import get_all_files

DATA_DIRECTORY = '../data'
ARCHIVE_DIRECTORY = '../data-archive'


def main(args):
    host = args.host
    port = args.port
    database = args.database
    collection = args.collection

    client = MongoClient(host=host, port=port)
    db = client[database]
    coll = db[collection]

    document_count = 0

    json_files = get_all_files(DATA_DIRECTORY, 'json')
    for json_file in json_files:
        with open(json_file) as f:
            for line in f:
                if line != '':
                    json_data = json.loads(line)
                    coll.insert_one(json_data)
                    document_count += 1
        f.close()

        # Rename file
        parent_dir_path = os.path.dirname(json_file)
        parent_dir_name = os.path.split(parent_dir_path)[1]  # Tail
        new_file_path = json_file + '_' + parent_dir_name
        os.rename(json_file, new_file_path)

        # Move file into archive directory
        shutil.move(new_file_path, ARCHIVE_DIRECTORY)  # Copy file and its metadata too

    print '{0} records added to MongoDB'.format(document_count)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import data into a MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str)
    parser.add_argument('--collection', type=str)
    args = parser.parse_args()
    main(args)
