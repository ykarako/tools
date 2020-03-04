#!/usr/bin/env python
from __future__ import print_function
import sys, serial, click, time

def confirm(port, retry, wait):
    try:
        ser = serial.Serial(port=port, baudrate=9600)
        ser.close()
    except Exception as e:
        if retry is None or retry > 0:
            print('.', end='')
            sys.stdout.flush()
            time.sleep(wait)
            confirm(port, None if retry is None else (retry - 1), wait)
        else:
            raise RuntimeError()

@click.command()
@click.argument('port')
@click.option('--retry', '-r', default=None)
@click.option('--wait' , '-w', default=1.0)
def main(port, retry, wait):
    print("I'll confirm serial connection. (port: {}, retry: {})".format(port, retry))
    try:
        confirm(port, retry, wait)
    except RuntimeError as e:
        print('\r\nI have gived up!!'.format(port))
        sys.exit(1)
    print("Connection confirmed!!")

if __name__ == '__main__':
    main()()
