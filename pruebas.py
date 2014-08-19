import calculate_frequencies as cf
import time

start_time = time.time()

#cf.insert_total_number_ngrams()

#f=cf.calculate_relative_frequency(['anxious'],'disease','Ulcers')
#f=cf.calculate_all_relative_frequencies(1,'disease','Ulcers')
#print repr(f)

#cf.insert_all_relative_frequencies()

f=cf.calculate_all_frequencies(2,'all','Blood')
print f