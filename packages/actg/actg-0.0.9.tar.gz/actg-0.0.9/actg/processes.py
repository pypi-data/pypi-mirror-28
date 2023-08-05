from .biofiles.vcf import Vcf
from .biofiles.bed import Bed
from .biofiles.tab import Tab

import sys
import os

def vcf_peek(args):
    """Function to show first lines of a VCF file

    Input
    -----
    args : parser.parse_args()
        Dictionary with arguments given by user

    """

    filepath = os.path.abspath(args.vcf)
    lines = args.lines
    pretty = args.pretty

    vcf = Vcf(filepath)

    if all([args.head, args.tail]) is False:
        vcf.head(lines, pretty)
        vcf.tail(lines, pretty)

    if args.head:
        vcf.head(lines, pretty)

    if args.tail:
        vcf.tail(lines, pretty)


def bed_sort(args):
    """Function to sort a bed file

    Input
    -----
    args : parser.parse_args()
        Dictionary with arguments given by user

    """

    filepath = os.path.abspath(args.bed)

    bed = Bed(filepath)

    bed.sort()


def transpose_lines(args):
    """Function to transpose first lines of a file

    Input
    -----
    args : parser.parse_args()
        Dictionary with arguments given by user

    """

    from collections import OrderedDict

    # Create variables in function
    nlines = args.lines
    color = args.color
    n = 0

    # Initiate filehandler
    if type(args.input) is str:
        # Open given filepath
        filepath = os.path.abspath(args.input)
        infhand = open(filepath, 'r')
    else:
        infhand = args.input

    values = OrderedDict()
    lines = False

    for line in infhand:
        line = line.strip('\n').split('\t')

        if lines is False:
            for key in line:
                values[key] = []
            lines = True
            continue

        for key, value in zip(values.keys(), line):
            values[key].append(value)

        n += 1

        if n >= nlines:
            break

    c = 0
    for key, value in values.items():
        value = " || ".join(value)
        if color is True:
            print(f"{c: <2} <> \033[95m{key}\033[0m <> {value: <8}")
        else:
            print(f"{c: <2} <> {key} <> {value: <8}")
        c += 1


def ucsc_get_gene_regions(args):
    from .dbs import ucsc_db
    ucsc = ucsc_db.connect_ucsc()
    data = ucsc.queryStructureByGene(['BRCA1'])
    ucsc.close_conn()

    for d in data:
        print(d)


def ucsc_rs_to_region(args):
    from .dbs import ucsc_db
    ucsc = ucsc_db.connect_ucsc()
    data = ucsc.queryRs(args.rs, args.dbsnp_version)
    print(data)
    ucsc.close_conn()

    for snp in data:
        print("\t".join([str(d) if type(d) is not bytes else d.decode('utf-8') for d in snp]))


def hgnc_get_official_name(args):
    import requests
    import json

    headers = {'Accept': 'application/json'}
    url = f"http://rest.genenames.org/search/alias_symbol/{args.gene}"

    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    for entry in data['response']['docs']:
        print(f"{{'official_name': {entry['symbol']}, 'synonym': {args.gene}, 'official': False}}")

    if data['response']['numFound'] == 0:
        url = f"http://rest.genenames.org/search/symbol/{args.gene}"

        r = requests.get(url, headers=headers)
        data = json.loads(r.text)

        if data['response']['numFound'] == 1:
            entry = data['response']['docs'][0]
            print(f"{{'official_name': {entry['symbol']}, 'synonym': '', 'official': True}}")
