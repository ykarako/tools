#!/usr/bin/env python
import os, glob, shutil, click
import numpy as np

USER = os.environ['USER']
FROM_DIR = '/home/{}/Downloads/'.format(USER)
TO_DIR = '/media/{}/MBED/'.format(USER)

if __name__ == '__main__':
    bin_paths = glob.glob(FROM_DIR + '*.bin')
    ctimes = [os.stat(x).st_ctime for x in bin_paths]
    bin_newest = bin_paths[np.argmax(ctimes)]
    click.secho('[{}] -> [{}]'.format(bin_newest, TO_DIR), fg='cyan', bold=True)
    yes = click.confirm('Will you copy?')
    if yes:
        shutil.copy(bin_newest, TO_DIR)
        print('Copied')
    else:
        print('Abort')
