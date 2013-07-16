##########################################################
#
# Author: Longbo Qiao
# email: longboqiao@gmail.com
# date: June 2013
#
##########################################################
import csv
inputPath ='processed/'
inputFile = 'matrix.csv'
outputPath = '../../Dictionaries/'
outputFile = 'newWL_new.csv'

r =csv.reader(open(inputPath + inputFile,'r'))
line1 = r.next()
text = str(line1)
textinput = open(outputPath + outputFile,'wb')
for item in line1:
	text = str(item)
	textinput.write(text)
	textinput.write('\n')