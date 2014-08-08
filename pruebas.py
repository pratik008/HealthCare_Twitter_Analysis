import calculate_frequencies as cf
import time

start_time = time.time()

cf.insert_total_number_ngrams()
print repr(time.time() - start_time)+' s'