
from numpy import integer
from controller.base_transform import BaseTransform


class AutoScale(BaseTransform):

	description = 'shift and scale all values to have zero mean and unit standard deviation; not guaranteed to have these properties for test data'
	options = []

	def learn(self, row):
		if issubclass(row.dtype.type, integer):
			row = row.astype(float)
		self.params['mean'] = row.min()
		self.params['std'] = row.std()

	def do(self, row):
		if issubclass(row.dtype.type, integer):
			row = row.astype(float)
		return (row - self.params['mean']) / self.params['std']


