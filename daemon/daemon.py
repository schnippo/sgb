from time import sleep, time
import os
import relay
from file_handler import cache_properties, sync_properties
import logger

last_modified = os.path.getmtime("remote_properties")
properties, relays = cache_properties()









while True:
	sleep(1)
	if last_modified != os.path.getmtime("remote_properties"):
		sync_properties()
		properties, relays = cache_properties()
		last_modified = os.path.getmtime("remote_properties")
	