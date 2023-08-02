import time
import logging

LOG = logging.getLogger(__name__)

class Timer(object):
	def __init__(self, name, active = True):
		self.name = name
		self.active = active

	def __enter__(self):
		self.start_tmstmp = int(time.time() * 1e9)

	def __exit__(self, type, value, traceback):
		if self.active:
			LOG.debug(f'Timer {self.name} finished. Took {round(((int(time.time() * 1e9)) - self.start_tmstmp) / 1000000, 3)} ms.')