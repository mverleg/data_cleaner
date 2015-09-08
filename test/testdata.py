
from numpy import save
from numpy.random import normal, exponential, randint


def get_data(N = 100):
	return [
		normal(2, 1.3, size = N),
		randint(-10, +30, size = N) + 100 * (randint(0, 4, size = N) == 0),
		exponential(37, size = N),
	]


if __name__ == '__main__':
	data = get_data(N = 100)
	#save('demo_data_100x3.npy', data)
	print(data)


