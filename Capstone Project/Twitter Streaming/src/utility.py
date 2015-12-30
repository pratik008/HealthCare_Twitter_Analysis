import os

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def get_all_files(root_dir, ext=''):
    """
    :param dir: Root directory path
    :param ext: Optional file extension to filter
    :return: All files with this file extension (if specified) within the root directory (recursive)
    """
    file_list = []
    for root, subdirs, files in os.walk(root_dir):
        if ext != '':
            for current_file in files:
                if current_file.endswith('.' + ext):
                    current_file_path = os.path.join(root, current_file)
                    file_list.append(current_file_path)
        else:
            for current_file in files:
                current_file_path = os.path.join(root, current_file)
                file_list.append(current_file_path)
        for current_subdir in subdirs:
            file_list = file_list + get_all_files(current_subdir, ext=ext)
    return file_list
