
from copy import deepcopy
from collections import OrderedDict
from misc import load_cls


class BaseTransform():

	name = None     # default value is the class name
	description = 'transforms data'
	options = []    # dictionaries with name, type, default and required

	class NotInitialized(Exception):
		""" Tried to apply a transformation that hasn't learned parameters yet. """

	def __init__(self):
		"""
			Set initial configuration and parameters.
		"""
		self.conf = {}
		for option in self.options:
			self.conf[option['name']] = option['default']
		self.set_params({})

	def get_name(self):
		"""
			If name is None, get is from the class.
		"""
		return self.name or self.__class__.__name__.lower()

	def __repr__(self):
		"""
			String representation of instances.
		"""
		confstr = ','.join('{0:}={1:}'.format(k, v) for k, v in self.conf.items()) or 'noconf'
		return '{0:s}:{1:s}'.format(self.get_name().replace(' ', '_'), confstr)

	def learn(self, row):
		"""
			Learn any parameters from the data.

			:param row: The data row to learn from.
		"""

	def do(self, row):
		"""
			Apply the transformation on the given row(s).

			:param data: Iterable of equal-length numpy 1D data arrays.
			:return: Collection of transformed equal-length numpy 1D data arrays.
		"""
		return row

	def get_conf(self):
		"""
			:return: JSON-able dictionary containing configuration options.
		"""
		return deepcopy(self.conf)

	def set_conf(self, input):
		"""
			Update configuration.

			:param loaded: A JSON-able dictionary containing configuration options.

			Works for empty dictionary (set defaults). Rejects invalid configurations.
		"""
		option_names = [option['name'] for option in self.options]
		for name, value in input.items():
			assert name in option_names, 'Unknown option "{0:s}" for "{1:s}"; accepted options are "{2:s}"'.format(name, type(self), '", "'.join(option_names))
		#todo: check/cast default types

	def get_params(self):
		"""
			:return: JSON-able dictionary containing learned parameters.
		"""
		return deepcopy(self.params)

	def set_params(self, input):
		"""
			Set parameters to previously learned ones, resetting any existing ones.

			:param loaded: A JSON-able dictionary containing parameters.

			There is less error checking here than for configuration, since this data is supposed to come directly from this class.
		"""
		self.params = deepcopy(input)

	def to_json(self):
		"""
			An encoder, converting this instance to JSON-able primary types.

			:return: A dictionary representing this instance.
		"""
		pypath = '{0:s}.{1:s}'.format(self.__class__.__module__, self.__class__.__name__)
		return OrderedDict([
			('transformation', pypath),
			('conf', self.get_conf()),
			('params', self.get_params()),
		])

	@classmethod
	def from_json(cls, di):
		"""
			A constructor/decoder to create instances from primary types (JSON-serializable ones), as created by to_json().

			:param str: A dictionary representing the transform instance.
			:return: An instance of the appropriate transform with the loaded attributes.
		"""
		for key in di.keys():
			assert key in ('transformation', 'conf', 'params',), 'unknown transform property {0:s}'.format(key)
		assert 'transformation' in di, 'type of transformation not found (should have \'transformation\': pythonpath)'
		Trns = load_cls(di['transformation'])
		trns = Trns()
		if 'conf' in di:
			trns.set_conf(di['conf'])
		if 'params' in di:
			trns.set_params(di['params'])
		return trns


