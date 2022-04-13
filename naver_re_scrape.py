from functions import *

prc_max = 35000

alert(watch_list_a, prc_max, 'data_1')

time.sleep(random.uniform(61, 120))

alert(watch_list_b, prc_max, 'data_2')

time.sleep(random.uniform(61, 120))

alert(watch_list_c, prc_max, 'data_3')