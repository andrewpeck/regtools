#!/usr/bin/env python3
import os.path
from os import mkdir

# returns the number of required 32 bit registers for this module -- basically it counts the number of registers with different addresses
def get_num_required_regs32(module):
    total_regs32 = 0
    if len(module.regs) > 0:
        total_regs32 = 1
        last_address = module.regs[0].address
        for reg in module.regs:
            if reg.address != last_address:
                total_regs32 += 1
                last_address = reg.address
    return total_regs32

def hex(number):
    if number is None:
        return 'None'
    else:
        return "{0:#0x}".format(number)

def hex_padded32(number):
    if number is None:
        return 'None'
    else:
        return "{0:#0{1}x}".format(number, 10)

def binary_padded32(number):
    if number is None:
        return 'None'
    else:
        return "{0:#0{1}b}".format(number, 34)

def vhdl_hex_padded(number, num_bits):
    if number is None:
        return 'None'
    else:
        hex32 = hex_padded32(number)
        binary32 = binary_padded32(number)

        ret = ''

        # if the number is not aligned with hex nibbles, add  some binary in front
        num_single_bits = (num_bits % 4)
        if num_single_bits != 0:
            ret += "'" if num_single_bits == 1 else '"'
            # go back from the MSB down to the boundary of the most significant nibble
            for i in range(num_bits, num_bits // 4 * 4, -1):
                ret += binary32[i *  -1]
            ret += "'" if num_single_bits == 1 else '"'


        # add the right amount of hex characters

        if num_bits // 4 > 0:
            if num_single_bits != 0:
                ret += ' & '
            ret += 'x"'
            for i in range(num_bits // 4, 0, -1):
                ret += hex32[i * -1]
            ret += '"'
        return ret


def parse_int(string):
    if string is None:
        return None
    elif string.startswith('0x'):
        return int(string, 16)
    elif string.startswith('0b'):
        return int(string, 2)
    else:
        return int(string)

def get_low_high_from_bitmask(bitmask):
    binary32 = binary_padded32(bitmask)
    lsb = -1
    msb = -1
    range_done = False
    for i in range(1, 33):
        if binary32[i * -1] == '1':
            if range_done == True:
                raise ValueError('Non-continuous bitmasks are not supported: %s' % hex_padded32(bitmask))
            if lsb == -1:
                lsb = i - 1
            msb = i - 1
        if lsb != -1 and binary32[i * -1] == '0':
            if range_done == False:
                range_done = True
    return msb, lsb
def substitute_vars(string, variables):
    if string is None:
        return string
    ret = string
    for key in variables.keys():
        ret = ret.replace('${' + key + '}', str(variables[key]))
    return ret

def updateFilename(fname, prefix, suffix):
    path_split = fname.split("/")
    fname_split = path_split[-1].split(".")
    path_split[-1] = prefix + fname_split[0] + suffix + "." + fname_split[1]
    
    new_path_split = os.path.join(*path_split).split("/")
    for i in range(len(new_path_split) - 1):
        d = os.path.join(*new_path_split[:i+1])
        try:
            mkdir(d)
        except OSError as err:
            pass        
    
    return os.path.join(*path_split)

class Module:
    top_node_name=""
    name = ''
    description = ''
    base_address = 0x0
    reg_address_msb = None
    reg_address_lsb = None
    file_name = ''
    user_clock = ''
    bus_clock = ''
    bus_reset = ''
    fw_cnt_reset_signal = None
    master_bus = ''
    slave_bus = ''

    # if this is true it means that firmware doesn't have to be modified,
    # only bash scripts will be generated
    is_external = False

    def __init__(self, top_node_name):
        """"""
        self.regs    = []
        self.parents = []
        self.top_node_name = top_node_name

    def add_reg(self, reg):
        """"""
        self.regs.append(reg)

    def add_parent(self, parent):
        """"""
        self.parents.append(parent)

    def is_valid(self):
        """"""
        if self.is_external:
            return self.name is not None

        return self.name is not None \
            and self.file_name is not None \
            and self.user_clock is not None \
            and self.bus_clock is not None \
            and self.bus_reset is not None \
            and self.master_bus is not None \
            and self.slave_bus is not None\
            and self.reg_address_msb is not None \
            and self.reg_address_lsb is not None

    def to_string(self):
        """"""
        return str(self.name) + \
            ' module: ' + str(self.description) + '\n'\
            + '    Base address = ' + hex(self.base_address) + '\n'\
            + '    Register address MSB = ' + hex(self.reg_address_msb) + '\n'\
            + '    Register address LSB = ' + hex(self.reg_address_lsb) + '\n'\
            + '    File = ' + str(self.file_name) + '\n'\
            + '    User clock = ' + str(self.user_clock) + '\n'\
            + '    Bus clock = ' + str(self.bus_clock) + '\n'\
            + '    Bus reset = ' + str(self.bus_reset) + '\n'\
            + '    Master_bus = ' + str(self.master_bus) + '\n'\
            + '    Slave_bus = ' + str(self.slave_bus)

    def get_vhdl_name(self):
        """"""
        return self.name.replace(self.top_node_name + '.', '').replace('.', '_')

class Register:
    """"""
    top_node_name=""
    name               = ''
    name_raw           = ''
    address            = 0x0
    description        = ''
    description_raw    = ''
    permission         = ''
    mask               = 0x0
    signal             = None
    write_pulse_signal = None
    write_done_signal  = None
    read_pulse_signal  = None
    read_ready_signal  = None

    genvars = {}
    gensize = {}
    genstep = {}

    # count signals
    fw_cnt_snap_signal    = '\'1\''
    fw_cnt_allow_rollover = 'false'
    fw_cnt_increment_step = '1'
    fw_cnt_reset_signal   = None
    fw_cnt_en_signal      = None

    fw_rate_clk_frequency = 40079000 # clock frequency in Hz
    fw_rate_reset_signal  = None     # Reset input
    fw_rate_en_signal     = None     # Enable

    default = 0x0
    msb = -1
    lsb = -1

    def __init__(self, top_node_name=""):
        """"""
        self.top_node_name = top_node_name

    def is_valid_reg(self, is_external = False):
        """"""
        if is_external:
            return self.name is not None \
                and self.address is not None \
                and self.permission is not None\
                and self.mask is not None
        else:
            return self.name is not None \
                and self.address is not None \
                and self.permission is not None\
                and self.mask is not None \
                and ((self.signal is not None and 'w' in self.permission) == (self.default is not None)) \
                and (self.signal is not None or self.write_pulse_signal is not None or self.read_pulse_signal is not None)

    def to_string(self):
        ret = 'Register ' + str(self.name) + ': ' + str(self.description) + '\n'\
              '    Address = ' + hex(self.address) + '\n'\
              '    Mask = ' + hex_padded32(self.mask) + '\n'\
              '    Permission = ' + str(self.permission) + '\n'\
              '    Default value = ' + hex_padded32(self.default) + '\n'\

        if self.signal is not None:
            ret += '    Signal = ' + str(self.signal) + '\n'
        if self.write_pulse_signal is not None:
            ret += '    Write pulse signal = ' + str(self.write_pulse_signal) + '\n'
        if self.write_done_signal is not None:
            ret += '    Write done signal = ' + str(self.write_done_signal) + '\n'
        if self.read_pulse_signal is not None:
            ret += '    Read pulse signal = ' + str(self.read_pulse_signal) + '\n'
        if self.read_ready_signal is not None:
            ret += '    Read ready signal = ' + str(self.read_ready_signal) + '\n'

        return ret

    def get_vhdl_name(self):
        """"""
        return self.name.replace(self.top_node_name + '.', '').replace('.', '_')
