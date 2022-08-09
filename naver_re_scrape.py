from functions import *

time_check_and_delete()

prc_max = 32000

alert(watch_list_a, prc_max, 'data_1')

time.sleep(random.uniform(61, 120))

alert(watch_list_b, prc_max, 'data_2')

time.sleep(random.uniform(150, 300))

alert(watch_list_c, 29990, 'data_3')
