from logging import getLogger
import importlib

import numpy as np

logger = getLogger(__name__)


def get_faucet_class(faucet_type):
	faucet_module = importlib.import_module('.'+faucet_type.lower(), 'icomputer')
	faucet_class = getattr(faucet_module, faucet_type)
	return faucet_class


class Faucet:
	# status of the faucet - True if faucet is currently open, False if closed
	isopen = False
	# timers associated with the faucet
	timers = []

	def __init__(self, name, computer_name, local_computer_name, faucet_type='generic', relay='0', counter='none', default_duration=30, **kwargs):
		'''Init the faucet

		Parameters
		----------
		name : str
			name of the faucet (i.e. 'roses drips')
		computer_name : str or None
			name of the computer the faucet is connected to or None for current computer name
		local_computer : IComputer
			the current computer this faucet is connected to
		faucet_type : str (optional)
			the relay type - can be 'numato'
		relay_idx : str or int
			the relay in the faucet controller (i.e. 0-F for numato 16 relay board
		default_duration: int (optional)
			the default duration of the faucet when opened manually/new timer added
		'''
		self.name = name
		self.local_computer_name = local_computer_name
		self.computer_name = computer_name
		self.faucet_type = faucet_type
		self.relay_idx = relay
		self.counter = counter
		self.default_duration = default_duration
		self.flow_counts = []

		# all_alone is set to True when opened, and turns False if more than one open on the same water counter
		self.all_alone = False
		logger.debug('Init faucet %s on computer %s' % (name, computer_name))

	def __repr__(self):
		return "Faucet: " + ', '.join("%s: %s" % item for item in vars(self).items())

	def open(self):
		'''Open the faucet (water on)
		'''
		self.isopen = True
		self.all_alone = True
		self.flow_counts = []
		return False

	def close(self):
		'''Close the faucet (water off)
		'''
		self.isopen = False
		return False

	def get_median_flow(self):
		'''Get the median water flow for the faucet

		Returns
		-------
		str
		The median flow (when the faucet was open alone on t)e counter) or "no counter", or "not alone"
		'''
		if self.counter == 'none':
			return 'no counter'
		if len(self.flow_counts) < 1:
			return 'not alone'
		return '%.2f' % np.median(self.flow_counts)