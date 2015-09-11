

def apply_transforms(operations, columns):
	"""
		Apply a chain of transformations to the data.
	"""
	for name, ops in operations.items():
		try:
			col = columns[name]
		except ValueError:
			raise ValueError('row key "{0:s}" is not an integer'.format(name))
		except IndexError:
			col = None
			#todo: maybe we're trying to make a new column?
		refshape = col.shape
		for op in ops:
			try:
				col = op.do(col)
			except op.NotInitialized as err:
				raise op.NotInitialized('"{0:s}" for row {1:} did not learn parameters yet; use .learn(row) first {2:}'.format(str(op), name, str(err)))
			assert col.shape == refshape, 'Operation "{0:s}" changed the shape from {1:} to {2:}, which is not allowed'.format(str(op, col.shape, refshape))
	return columns


def train_transforms(operations, columns):
	"""
		Train a chain of transformations to the data.

		:return: Returns the trained operations for style, although they are also changed in-place.
	"""
	for name in operations.keys():
		col = columns[name]
		for op in operations[name]:
			op.learn(col)
	return operations


