from __future__ import print_function, absolute_import, unicode_literals
import glob
import os
import random
import multiprocessing
import lxml.etree as et
from ilabs.client.ilabs_predictor import ILabsPredictor


BRS_S = '{http://innodatalabs.com/brs}s'  # BRS label tag from BRS specs

def predict_file(args):
    '''
    Executes prediction on a file content, and saves result to output file
    '''
    domain, input_filename, output_filename, user_key, strip_labels = args

    predictor = ILabsPredictor.init(domain, user_key=user_key)

    try:
        with open(input_filename, 'rb') as f:
            input_bytes = f.read()
            if strip_labels:
                xml = et.fromstring(input_bytes)
                et.strip_tags(xml, BRS_S)
                input_bytes = et.tostring(xml, xml_declaration=True, encoding='utf-8')

        output_bytes = predictor(input_bytes)

        with open(output_filename, 'wb') as f:
            f.write(output_bytes)

    except RuntimeError as e:
        return e

def missing_files(input_dir, output_dir):
    '''
    Finds files that are present in the "input_dir", but missing from the
    "output_dir"
    '''
    input_names = {
        os.path.basename(x)
        for x in glob.glob(input_dir + '/*') if os.path.isfile(x)
    }

    output_names = {
        os.path.basename(x)
        for x in glob.glob(output_dir + '/*') if os.path.isfile(x)
    }

    return sorted(input_names - output_names)

def ilabs_bulk_upload(domain, input_dir, output_dir, num_workers=10, user_key=None, strip_labels=False):

    fileset = missing_files(input_dir, output_dir)
    if not fileset:
        return

    jobs = [
        (domain, os.path.join(input_dir, x), os.path.join(output_dir, x), user_key, strip_labels)
        for x in fileset
    ]

    if num_workers > 1:
        pool = multiprocessing.Pool(num_workers)
        results = pool.map(predict_file, jobs)
        pool.close()
    else:
        results = map(predict_file, jobs)

    for error, filename in zip(results, fileset):
        print(filename, error or 'OK')

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sends all files from the input '
        'directory to prediction service and '
        'places result in the output directory')

    parser.add_argument('--domain', '-d', required=True, help='Prediction domain')
    parser.add_argument('--user_key', '-u', help='Secret user key')
    parser.add_argument('--strip_labels', '-s', action='store_true',
        help='If set, assumes that files are BRS and strips off <brs:s> labels before sending')
    parser.add_argument('input_dir', help='Directory where input files are located')
    parser.add_argument('output_dir', help='Directory where output will be saved')
    parser.add_argument('--num_workers', '-n', type=int, default=10, help='Number of concurrent workers')

    args = parser.parse_args()

    ilabs_bulk_upload(args.domain, args.input_dir, args.output_dir, args.num_workers, args.user_key, args.strip_labels)

if __name__ == '__main__':
    main()
