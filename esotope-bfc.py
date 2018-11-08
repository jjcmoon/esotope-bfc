import sys
import argparse

from bfc.compiler import Compiler
from bfc.parser import brainfuck as parser_bf, bfrle as parser_bfrle
from bfc.codegen import c as codegen_c

PARSERS = {'brainfuck': parser_bf, 'bfrle': parser_bfrle}
CODEGENS = {'c': codegen_c}


def main(argv):
	arg_parser = argparse.ArgumentParser(
		description = "Esotope Brainfuck Compiler."
	)
	arg_parser.add_argument(
		'-i', '--input-format', 
		default = 'brainfuck',
		help = '''Sets the parser module. FORMAT can be "brainfuck" or "bfrle", and defaults to brainfuck.'''
	)
	arg_parser.add_argument(
		'-f', '--output-format',
		default = 'c',
		help = 'Sets the code generator module. FORMAT can be "c", and defaults to "c" currently.'
	)
	arg_parser.add_argument(
		'-c', '--cellsize', type=int,
		default = 8,
		help = 'Sets the size of each memory size. BITS can be 8, 16 or 32, and defaults to 8.'
	)
	arg_parser.add_argument(
		'--debug',
		default = False,
		help = 'Enables debugging output (as C comment) in the code.'
	)
	arg_parser.add_argument(
		'file',
		metavar='FILE',
		help='File to read, use "-" to read from stdin'
	)
	args = arg_parser.parse_args()

	if args.cellsize not in (8, 16, 32):
		raise ValueError("Error: Invalid cellsize {}!".format(args.cellsize))

	if args.file == '-':
		fp = sys.stdin
	else:
		fp = open(args.file, 'r')

	compiler = Compiler(
		parser = PARSERS[args.input_format].Parser,
		codegen = CODEGENS[args.output_format].Generator,
		cellsize = args.cellsize, 
		debugging = args.debug
	)

	compiler.compile(fp)
	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

