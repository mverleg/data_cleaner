
from controller.base_transform import BaseTransform


class Shift(BaseTransform):

	description = 'increases all values by a given constant'
	options = [
		{
			'name': 'delta',
			'type': None,
			'default': 0,
			'required': True,
		},
	]

	def do(self, row):
		return row + self.conf['delta']

	def set_conf(self, input):
		super(Shift, self).set_conf(input)
		#assert is_number(self.conf['index']), 'Option "delta" should be numerical for "{0:s}"'.format(type(self))  #todo


