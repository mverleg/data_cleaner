
from collections import OrderedDict
from numpy import copy, array


def get_cols(data, names, copy_data = True):
	"""
		Convert raw loaded data to a dict of columns.

		:param data: ndarray of data.
		:param names: List of column names.
		:param copy_data: Copy the data if true, otherwise use a view
		:return: An OrderedDict of data columns (ordered for converting back to array).
	"""
	assert data.shape[1] == len(names)
	columns = OrderedDict()
	for k, name in enumerate(names):
		if copy_data:
			columns[name] = copy(data[:, k])
		else:
			columns[name] = data[:, k]
	# for name in extra_names:
	# 	if name not in columns:
	# 		columns[name] = None
	return columns


def get_array(columns):
	"""
		Inverse of get_cols
	"""
	#todo: check for None columns
	#todo: and other mismatch columns
	names = list(columns.keys())
	data = array(list(columns.values())).T
	return data, names
