
"""
	Command-line interface
"""

from argparse import ArgumentParser
from collections import OrderedDict
from os import close
from sys import stdout, stderr
from tempfile import mkstemp
from numpy import load as numpy_load, save as numpy_save
from json import load as json_load
from os.path import exists
from controller.apply_transforms import train_transforms, apply_transforms
from controller.data_io import get_cols, get_array
from controller.transform_io import load_operations, load_chain, save_chain, save_operations
from view.interface_server import run_server

parser = ArgumentParser(description = 'Reads operations from a json file and applies them to data row-by-row.')
parser.add_argument('-w', '--interface', dest = 'interface', action = 'store_true', help = 'Start the web interface server.')
parser.add_argument('-t', '--trans', dest = 'trans', action = 'store', type = str, default = None, help = 'The operations file (json) for the transformations.')
parser.add_argument('-T', '--trans_out', dest = 'trans_out', action = 'store', type = str, default = None, help = 'The output operations file after learning;. By default, the input file is overwritten.')
parser.add_argument('-i', '--data_in', dest = 'data_in', action = 'store', type = str, default = None, help = 'The file with data to apply transformations to.')
parser.add_argument('-o', '--data_out', dest = 'data_out', action = 'store', type = str, default = None, help = 'The filename to write transformed data to.')
parser.add_argument('-n', '--var_names', dest = 'var_names', action = 'store', type = str, default = None, help = 'Specify the variable(column) names as json file (not needed if contained in transformation file).')
parser.add_argument('-m', '--make_names', dest = 'make_names', action = 'store_true', help = 'As an alternative to --var_names, generate number names for variables.')
parser.add_argument('-l', '--limit', dest = 'limit', action= 'store', type = int, default = None, help = 'Load only the first X rows to save memory.')
parser.add_argument('-c', '--cache', dest = 'cache', action = 'count', default = 0, help = 'Increase caching (through files in temporary folder).')
parser.add_argument('--transpose', dest = 'transpose', action = 'store_true', help = 'Transpose input (to make sure that the variables are the second dimension of input data).')
parser.add_argument('-f', '--learn', dest = 'learn', action = 'store_true', help = 'Learn the operations in the transformations file on the input data. Also available through the interface.')
parser.add_argument('-d', '--do', dest = 'do', action = 'store_true', help = 'Apply the operations in the transformations file on the input data. If --learn is specified, it happens before applying transformations.  Also available through the interface.')
parser.add_argument('--host', dest = 'host', type = str, default = '127.0.0.1', help = 'Host IP or domain for the interface; defaults to 127.0.0.1 (localhost).')
parser.add_argument('--port', dest = 'port', type = int, default = 7199, help = 'Host port for the interface; defaults to 7199.')
#parser.add_argument('-s', '--save', dest = 'save', action = 'store_true', help = 'Save the data to --data_out after transformation (--do). Also available through the interface.')
#todo: extra data transformations (comma-separated python import path)

args = parser.parse_args()

opsstr = raw = config = var_names = transformations = None  #todo: remove

if exists(args.trans):
	try:
		opsstr = load_operations(args.trans)
	except IOError:
		stderr.write('transformation file "{0:s}" couldn\'\t be loaded\n'.format(args.trans))
		exit(1)
	try:
		config, transformations = load_chain(opsstr)
	except ValueError as err:
		stderr.write('there is an error in transformation file "{0:s}" (it should be valid json)\n'.format(args.trans))
		stderr.write('{0:s}\n'.format(str(err)))
		exit(2)
else:
	stdout.write('transformation file "{0:s}" doesn\'t exist; using empty transformations\n'.format(args.trans))
	config = {'input_vars': None}
	transformations = OrderedDict()

if args.trans_out is None:
	args.trans_out = args.trans

if not args.data_in:
	stderr.write('please provide an input data file (--help for info)\n')
	exit(3)
try:
	raw = numpy_load(args.data_in)
except FileNotFoundError:
	stderr.write('input file "{0:s}" could not be found\n'.format(args.data_in))
	exit(4)
except OSError:
	stderr.write('there is an error in input file "{0:s}" (it should be a valid npy file)\n'.format(args.data_in))
	exit(5)

if args.transpose:
	raw = raw.T

if args.limit:
	stdout.write('--limit loads the whole array before slicing it (no easy way to partially load npy files)\n')
	raw = raw[:, :args.limit]

if args.var_names:
	if args.make_names:
		stdout.write('--var_names and --make_names are both set; --make_names will be ignored\n')
	try:
		var_names = json_load(open(args.var_names, 'r'))
	except NotImplementedError as err: #todo
		stderr.write('could not load "{0:s}" (should be a json list)\n'.format(args.var_names))
		stderr.write('{0:s}\n'.format(str(err)))
		exit(6)
	if config['input_vars'] and not var_names == config['input_vars']:
		print(var_names, config['input_vars'])
		stdout.write('variable names are already set in the transformation file; they will be ignored\n')
elif config['input_vars']:
	if args.make_names:
		stdout.write('--make_names is set but there are already names in the transformation file; --make_names will be ignored\n')
		var_names = config['input_vars']
elif args.make_names:
	var_names = ['{0:d}'.format(k) for k in range(len(raw.shape[1]))]
else:
	stderr.write('no names found; either provide them using --var_names or --make_names (see --help) or add them to the transformation file\n')
	exit(7)
config['input_vars'] = var_names
if not len(config['input_vars']) == raw.shape[1]:
	stderr.write('found {0:d} names for {1:d} columns; each input column should have one name\n'.format(len(config['input_vars']), raw.shape[1]))
	exit(8)

if not args.data_out:
	fh, nm = mkstemp()
	close(fh)
	args.data_out = '{0:s}.npy'.format(nm)
	stdout.write('no output file given; using "{0:s}"\n'.format(args.data_out))
#todo: maybe check write permissions for the output file if one is specified, but it's a bit of a pain without creating/purging the file

if not args.learn and not args.do and not args.interface:
	stdout.write('no operations requested and no interface opened; nothing to do (see --help, specifically --interface and --learn/--do)\n')
	exit(0)

columns = get_cols(raw, var_names)
del raw

if args.learn:
	stdout.write('learning parameters for transformations from {0:d} columns\n'.format(len(columns)))
	transformations = train_transforms(transformations, columns)
	stdout.write('saving transformations to "{0:s}"\n'.format(args.trans_out))
	opsstr = save_chain(config, transformations)
	save_operations(opsstr, args.trans_out)

if args.do:
	stdout.write('applying transformations to {0:d} columns\n'.format(len(columns)))
	columns = apply_transforms(transformations, columns)
	stdout.write('saving transformed data to "{0:s}"\n'.format(args.data_out))
	data, names = get_array(columns)
	numpy_save(args.data_out, data)

if args.interface:
	run_server(args.host, args.port)

stdout.write('done\n')


