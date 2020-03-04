#!/usr/bin/env python
import serial, click

@click.command()
@click.option('--port', '-p', default='/dev/ttyMbed')
@click.option('--baud', '-b', default=57600)
def reset_mbed(port, baud):
    ser = serial.Serial(port=port, baudrate=baud, timeout=8)
    if not ser.is_open: ser.open()
    ser.send_break(duration=2.0)
    ser.close()

if __name__ == '__main__':
    reset_mbed()
