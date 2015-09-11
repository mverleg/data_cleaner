
from collections import OrderedDict
from numpy import copy


def apply_transforms(operations, columns, in_place = False):
	"""
		Apply a chain of transformations to the data.
	"""
	if in_place:
		converted = columns
	else:
		converted = OrderedDict()
	for name, ops in operations.items():
		try:
			if in_place:
				col = columns[name]
			else:
				col = copy(columns[name])
		except IndexError:
			""" Making a new column """
			col = None
		ref_shape = col.shape
		for op in ops:
			try:
				col = op.do(col)
			except op.NotInitialized as err:
				raise op.NotInitialized('"{0:s}" for row {1:} did not learn parameters yet; use .learn(row) first {2:}'.format(str(op), name, str(err)))
			except AssertionError as err:
				raise op.NotInitialized('"{0:s}" for row {1:} encountered a problem: {2:}'.format(str(op), name, str(err)))
			assert col.shape == ref_shape, 'Operation "{0:s}" changed the shape from {1:} to {2:}, which is not allowed'.format(str(op, col.shape, ref_shape))
		converted[name] = col
	for name, col in columns.items():
		if name not in converted:
			converted[name] = col
	return converted


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


