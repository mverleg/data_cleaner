
from collections import OrderedDict
from json import load, dump
from misc import load_cls


def load_operations(path):
	with open(path, 'r') as fh:
		return load(fh, object_pairs_hook = OrderedDict)


def save_operations(operations, path):
	with open(path, 'w+') as fh:
		return dump(operations, fh, sort_keys = False)


def load_chain(ops):
	"""
		Load a chain of operations as classes.

		:param ops: JSON-able list of operations.
	"""
	chain = OrderedDict()
	for colnr, rops in ops.items():
		chain[colnr] = []
		#assert 'operations' in rops, 'No key "operations" for batch {0:d}'.format(nr + 1)
		for tnr, transform in enumerate(rops):
			assert 'transformation' in transform, 'No transformation specified for row {0:d} transformation {1:d}'.format(colnr, tnr + 1)
			Trns = load_cls(transform['transformation'])
			trns = Trns()
			if 'conf' in transform:
				trns.set_conf(transform['conf'])
			else:
				print('No configuration options specified for row {0:d} transformation {1:d}'.format(colnr, tnr + 1))
			if 'params' in transform:
				trns.set_params(transform['params'])
			chain[colnr].append(trns)
	return chain


