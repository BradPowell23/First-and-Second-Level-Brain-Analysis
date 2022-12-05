#!/usr/bin/env python
import sys
sys.path.insert(0, 'src')

from src import single_run

def main(targets):
    '''
    Runs target test on the test data
    '''
    if 'test' in targets:
        single_run('test/testdata/test_data.nii.gz', 'test/testdata/events_view.tsv', 'test/testdata/events_recall.tsv', 'test/testdata/confounds.txt')       
    return

if __name__ == '__main__':
    targets = sys.argv[0:]
    main(targets)
