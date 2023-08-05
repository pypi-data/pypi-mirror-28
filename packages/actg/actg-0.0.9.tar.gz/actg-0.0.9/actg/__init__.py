from .messages import *
from .tools import *
from .utils import *

from .biofiles import *
from .processes import *

__version__ = '0.0.9'

import argparse
import os
import io
import actg
import sys


def parse_options():
    parser = argparse.ArgumentParser(description='Any description to be displayed for the program.')

    # Create a subcommand
    subparsers = parser.add_subparsers(help='Add sub commands', dest='command')

    # Define a primary command apply & set child/sub commands for apply
    add_subp = subparsers.add_parser('vcf_peek', help='Different tools to apply to VCF files')
    vcf_peek_sub_commands(add_subp)
    add_subp = subparsers.add_parser('bed_sort', help='Different tools to apply to BED regions files')
    bed_sort_sub_commands(add_subp)
    add_subp = subparsers.add_parser('transpose_lines', help='''Tool that transposes first lines of a file,
    thus showing the information of the file more efficiently''')
    transpose_lines_sub_commands(add_subp)

    # UCSC
    add_subp = subparsers.add_parser('ucsc_get_coordinates', help='''Tool to get the chromosomical
    positions or region of a desired gene/transcript/snp in the selected build''')
    ucsc_get_coordinates_sub_commands(add_subp)
    # add_subp = subparsers.add_parser('ucsc_rs_to_region', help='''UCSC tool to get position of snp''')
    # ucsc_rs_to_region_sub_commands(add_subp)

    # Gene Names
    add_subp = subparsers.add_parser('hgnc_get_official_name', help='''Tool to check a gene name, returning
    if the symbol is the official one or the translation in case there is one''')
    hgnc_get_official_name_sub_commands(add_subp)

    # add_p = subparsers.add_parser('destroy', help='Destroy the infra from system')
    # sub_commands(add_p)
    # add_p = subparsers.add_parser('plan', help='Verify your changes before apply')
    # sub_commands(add_p)
    args = parser.parse_args()
    if args.command == None:
        parser.print_help()
        sys.exit(1)

    return args


def vcf_peek_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--vcf", help='Location to tf state file',
                       required=True)
    add_arg.add_argument("-f", "--head", action='store_true', help='First Variants in VCF')
    add_arg.add_argument("-t", "--tail", action='store_true', help='Lasts Variants in VCF')
    add_arg.add_argument("-p", "--pretty", action='store_true', help='Pretty print VCF')
    add_arg.add_argument("-l", "--lines", type=int, default=5, help='Print this N lines')

    return add_arg

def bed_sort_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--bed", help='Location to tf state file', required=True)

    return add_arg


def ucsc_get_coordinates_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-g", "--gene", help='Get regions of this gene', required=True)

    return add_arg


def transpose_lines_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--input", nargs='?', help="File to transpose", default=sys.stdin)
    add_arg.add_argument("-l", "--lines", type=int, default=1, help="Lines to show")
    add_arg.add_argument("-c", "--color", action='store_true', help="Color the ID column with a different column")
    return add_arg

# def ucsc_rs_to_region_sub_commands(add_arg):
#     # Create child commands
#     # use required option to make the option mandatory
#     # Use metavar to print description for what kind of input is expected
#     add_arg.add_argument("-i", "--rs", required=True, help="rsID")
#     add_arg.add_argument("-d", "--dbsnp_version", default='snp150', help="ucsc DB version [snp150]")
#     add_arg.add_argument("-b", "--build", default='GRCh37', help="Build from which recover the rsID [hg19/GRCh37]")
#     return add_arg

def hgnc_get_official_name_sub_commands(add_arg):
    # Create child commands
    # use required option to make the option mandatory
    # Use metavar to print description for what kind of input is expected
    add_arg.add_argument("-i", "--gene", required=True, help="Gene name to translate to official HGNC name")
    return add_arg


def main():

    args = parse_options()

    dispatcher = {
                'vcf_peek': vcf_peek,
                'bed_sort': bed_sort,
                'transpose_lines': transpose_lines,
                'ucsc_get_gene_regions': ucsc_get_gene_regions,
                'ucsc_rs_to_region': ucsc_rs_to_region,
                'hgnc_get_official_name': hgnc_get_official_name,
                }

    dispatcher[args.command](args)


if __name__ == "__main__":

    main()
