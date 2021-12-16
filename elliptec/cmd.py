''' This file contains a dictionary of commands that the devices can accept in 
three different categories: get, set, move. For each command, it returns the 
instruction code to send to the device. '''

# TODO: Each type of device should get it's own list of supported commands.

get_ = {
	'info' : b'in',
	'status' : b'gs',
	'position': b'gp',
	'stepsize' : b'gj',
	'home_offset' : b'go',
    'motor_1_info' : b'i1',
    'motor_2_info' : b'i2',
	}

set_ = {
	'stepsize' : b'sj',
	'isolate'  : b'is'
	}

mov_ = {
	'home_clockwise' : b'ho0',
	'home_anticlockwise' : b'ho1',
	'forward' : b'fw',
	'backward' : b'bw',
	'absolute' : b'ma',
	'relative' : b'mr'
	}

def commands():
	return [get_, set_, mov_]

if __name__ == '__main__':
	keys = cmd.keys()
	print('\n'.join(keys))