import calculate_frequencies as cf
import time

start_time = time.time()

f=cf.calculate_frequency(['feel','sick'],'all','Cancer')
print f
print repr(time.time() - start_time)+' s'