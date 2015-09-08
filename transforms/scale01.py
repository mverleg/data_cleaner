
from numpy import integer
from controller.base_transform import BaseTransform


class Scale01(BaseTransform):

	name = 'scale to [0, 1]'
	description = 'shift and scale all values to be between 0 and 1 (inclusive); not guaranteed to be in [0, 1] for test data'
	options = []

	def learn(self, row):
		self.params['mean'] = row.mean()
		self.params['std'] = row.std()  # already does mean-centering

	def do(self, row):
		if not ('mean' in self.params and 'std' in self.params):
			raise self.NotInitialized()
		if issubclass(row.dtype.type, integer):
			row = row.astype(float)
		return row - self.params['mean']


