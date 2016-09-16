#!/usr/bin/env python


import sys
import tempfile
import xml.etree.ElementTree as ET
import os
import argparse
import petl
from StringIO import StringIO
from settings import settings
import requests


def main(argv):
    parser = argparse.ArgumentParser(description='Loads TSV file into custom Birthplace field in CCB.')
    parser.add_argument("--id-pob-tsv-filename", required=True, help='Input TSV file with two columns: '
        'Individual ID <tab> Place of Birth.')
    parser.add_argument('--trace', action='store_true', help="If specified, prints tracing/progress messages to "
        "stdout")
    args = parser.parse_args()

    assert os.path.isfile(args.id_pob_tsv_filename), "Error: cannot open file '" + args.id_pob_tsv_filename + "'"

    table = petl.fromtsv(args.id_pob_tsv_filename)
    header = petl.header(table)
    assert len(header) == 2, "Error: there must be exactly two columns (id, pob) in '" + args.id_pob_tsv_filename + "'"
    col_name_id = header[0]
    col_name_pob = header[1]
    for row in petl.records(table):
        id = row[col_name_id]
        pob = row[col_name_pob]
        update_pob(id, pob)

    sys.stdout.flush()
    sys.stderr.flush()


def update_pob(id, pob):
    # if id != str(5):
    #     print 'Skipping addition of mapping ' + str(id) + ' -> ' + str(pob)
    #     return
    print 'Adding mapping ' + str(id) + ' -> ' + str(pob)
    data = {
        'udf_text_5': str(pob) # This is the actual underlying Individual field for 'Birthplace'
    }
    params = {
        'individual_id': str(id)
    }
    response = requests.post('https://ingomar.ccbchurch.com/api.php?srv=update_individual', data=data,
        params=params, auth=(settings.ccbapi.username, settings.ccbapi.password))
    assert response.status_code == 200, "REST POST failure (http code " + str(response.status_code) + ") updating " + \
        "Individual ID " + str(id) + " to Place of Birth: " + str(pob)


def trace(msg_str, trace_flag, banner=False):
    if trace_flag:
        if banner:
            print
            print '*************************************************************************************************' \
                '**********************'
            print '*** ' + msg_str
        else:
            print msg_str
        if banner:
            print '*************************************************************************************************' \
                '**********************'
            print


if __name__ == "__main__":
    main(sys.argv[1:])
