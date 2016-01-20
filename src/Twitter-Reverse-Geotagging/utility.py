import json
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

def openWithHeaders(destDir, name, headers=''):
<<<<<<< HEAD
	if not os.path.exists(destDir):
		os.makedirs(destDir)
=======
>>>>>>> e1f1750c014f9de2e78fe17fa9314602ce6d05f0
	file = open(os.path.join(destDir,name),'w+')
	file.write(headers+'\n')
	return file