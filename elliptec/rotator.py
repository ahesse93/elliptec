from .cmd import get_, set_, mov_
from .devices import devices
from .tools import int_to_padded_hex, parse, error_check, move_check
from . import Motor

class Rotator(Motor):
    ''' Rotary Stage (ELL14) '''
    
    def __init__(self, port, debug=True, inverted=False):
        # Patch parent object - elliptec.Motor(port, baud, bytesize, parity)
        super().__init__(port, debug=debug)
    
    ## Position control
    def get_angle(self):
        ''' Finds at which angle (in degrees) the rotator is at the moment. '''
        status = self.get('position')
        angle = self.extract_angle_from_status(status)
        return angle
    
    def set_angle(self, angle):
        ''' Moves the rotator to a particular angle (in degrees). 
        '''
        position = self.angle_to_pos(angle)
        status = self.move('absolute', position)
        angle = self.extract_angle_from_status(status)
        return angle

    def shift_angle(self, angle):
        position = self.angle_to_pos(angle)
        status = self.move('relative', position)
        angle = self.extract_angle_from_status(status)
        return angle

    def jog(self, direction="forward"):
        if direction in ["backward", "forward"]:
            status = self.move(direction)
            angle = self.extract_angle_from_status(status)
            return angle
        else:
            return None

    # Home set/get
    def get_home_offset(self):
        status = self.get('home_offset')
        angle = self.extract_angle_from_status(status)
        return angle

    # Jog step
    def get_jog_step(self):
        status = self.get('stepsize')
        angle = self.extract_angle_from_status(status)
        return angle

    def set_jog_step(self, angle):
        ''' Sets jog step to a particular angle (in degrees). 
        '''
        position = self.angle_to_pos(angle)
        status = self.set('stepsize', position)
        return status

    # TODO: set_home_offset(self, offset)
    # TODO: clean(self)
    # TODO: clean_and_optimize(self)

    # Helper functions
    def extract_angle_from_status(self, status):
        # If status is telling us current position
        if status:
            if status[0] in ['PO', 'HO', 'GJ']:
                position = int(str(status[1]), 16)
                angle = self.pos_to_angle(position)
                return angle
        
        return None

    def pos_to_angle(self, posval):
        position = posval % self.pulse_per_rev
        angle = position/self.pulse_per_rev * self.range
        angle_rounded = round(angle, 4)
        return angle_rounded
        
    def angle_to_pos(self, angleval):
        angle = angleval % self.range
        position = int(angle/self.range * self.pulse_per_rev)
        return position