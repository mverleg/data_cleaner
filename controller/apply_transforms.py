

def apply_transforms(operations, rows):
	"""
		Apply a chain of transformations to the data.
	"""
	for rownr, ops in operations.items():
		try:
			row = rows[int(rownr)]
		except ValueError:
			raise ValueError('row key "{0:s}" is not an integer'.format(rownr))
		except IndexError:
			row = None
			#todo: maybe we're trying to make a new row?
		refshape = row.shape
		for op in ops:
			try:
				row = op.do(row)
			except op.NotInitialized as err:
				raise op.NotInitialized('"{0:s}" for row {1:} did not learn parameters yet; use .learn(row) first {2:}'.format(str(op), rownr, str(err)))
			assert row.shape == refshape, 'Operation "{0:s}" changed the shape from {1:} to {2:}, which is not allowed'.format(str(op, row.shape, refshape))
	return rows


def train_transforms(operations, rows):
	"""
		Train a chain of transformations to the data.

		:return: Returns the trained operations for style, although they are also changed in-place.
	"""
	for rownr, ops in operations.items():
		row = rows[int(rownr)]
		for op in ops:
			op.learn(row)
	return operations


