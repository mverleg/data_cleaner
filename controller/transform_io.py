
from collections import OrderedDict
from commentjson import load, dump
from controller.base_transform import BaseTransform


def load_operations(path):
	with open(path, 'r') as fh:
		return load(fh, object_pairs_hook = OrderedDict)


def save_operations(operations, path, indent = 2):
	with open(path, 'w+') as fh:
		return dump(operations, fh, indent = indent, sort_keys = False)


def load_chain(ops):
	"""
		Load a chain of operations as classes.

		:param ops: a string of JSON-ed (ordered) dict of operations and possibly configuration. Keys starting with _ are skipped.
		:return: (tuple of) configuration dictionary and operations OrderedDict.
	"""
	config = ops['__config__']  #todo: test if config provided
	if not 'var_names' in config:
		config['var_names'] = []
	chain = OrderedDict()
	for name, rops in ops.items():
		if name.startswith('_'):
			continue
		chain[name] = []
		for tnr, transform in enumerate(rops):
			try:
				trns = BaseTransform.from_json(transform)
			except AssertionError as err:
				raise IOError('Problem for columns "{0:s}", transformation {1:d}: "{2:s}"'.format(name, tnr + 1, str(err)))
			chain[name].append(trns)
	return config, chain


def save_chain(config, chain):
	"""
		Encode a chain of operation classes as json.

		:param config: dictionary with settings.
		:param chain: OrderedDict of operation class lists.
		:return: string-encoded version of the above.
	"""
	di = OrderedDict()
	di['__config__'] = config
	for key, ops in chain.items():
		di[key] = [op.to_json() for op in ops]
	return di
	#return dumps(di, indent = 2)


