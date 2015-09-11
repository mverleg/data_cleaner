
from functools import lru_cache
from importlib import import_module
from inspect import isclass
from os.path import realpath
from os.path import dirname


BASE_DIR = realpath(dirname(__file__))


def is_number(obj):
	#todo: delete?
	"""
		Shorter name for is_probably_a_number_since_it_behaves_like_one().
	"""
	try:
		obj + 3.7
	except TypeError:
		return False
	return True


@lru_cache()
def load_cls(path):
	"""
		Load a class by import path, like here: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
	"""
	filepath, classname = path.rsplit('.', 1)
	mod = import_module(filepath)
	assert hasattr(mod, classname), 'path "{0:s}" has no "{1:s}"'.format(filepath, classname)
	Cls = getattr(mod, classname, None)
	assert isclass(Cls), '"{0:s}" imported but is not a class'.format(path)
	return Cls


