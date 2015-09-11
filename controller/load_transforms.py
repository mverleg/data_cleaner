
from collections import OrderedDict
from json import load, dump, dumps
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
			assert 'transformation' in transform, 'No transformation specified for column "{0:s}" transformation {1:d}'.format(name, tnr + 1)
			Trns = load_cls(transform['transformation'])
			trns = Trns()
			if 'conf' in transform:
				trns.set_conf(transform['conf'])
			else:
				print('No configuration options specified for column "{0:s}" transformation {1:d}'.format(name, tnr + 1))
			if 'params' in transform:
				trns.set_params(transform['params'])
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
	for key, value in chain.items():
		di[key] = value
	return dumps(di, indent = 2)


