
from numpy import load
from controller.apply_transforms import apply_transforms, train_transforms
from controller.transform_io import load_chain, load_operations


def test_load_chain():
	config, ops = load_chain(load_operations('test/test01.json'))
	data = load('test/demo_data_100x3.npy')
	rows = [row for row in data]
	ops = train_transforms(ops, rows)
	data = apply_transforms(ops, rows)


test_load_chain()


