import sys

def lines(x):
##  create a dictionary with unique drug names, no repeats which include % etc.
    drugnames = {}
    output = {}
   # print x
 #   n=0
    for line in x:
         # print line.strip()
          if line not in drugnames:
                  drugnames[line] = line
                  filtereddrug = ""
                  for drugelement in line.split():
                    if (drugelement not in notallowedwords) and (len(str(drugelement)) > 2) :
                      for element in drugelement:
                          if element not in notalloweddigits:
                              filtereddrug += str(element)
                      filtereddrug += " "
   #               print filtereddrug
                    
                  if filtereddrug not in output:
                                output[filtereddrug] = filtereddrug
   # print output                                                
    for drug in output:
        if len(drug) > 2:
            drugs.write("'#" + (output[drug].strip()).lower() + "', ")


def main():
    global sent_file
    inputdrugs = open(sys.argv[1])
    global drugs
    drugs = open("fdadrugs.txt", "w")
    global notalloweddigits
    global notallowedwords
    notalloweddigits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/","%", "-", "#", "in",
                      "+", "_", ",", "&", ".", "(", ")",";", ":", "'"]
    notallowedwords = ["PLASTIC", "CONTAINER", "IN","AND", "UNITS"]
    lines(inputdrugs)

if __name__ == '__main__':
    main()
