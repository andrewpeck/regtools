#!/usr/bin/python2
from __future__ import unicode_literals
from __future__ import print_function

__author__ = 'evka'

import io
import xml.etree.ElementTree as xml
import textwrap as tw
import argparse
import sys
import shutil
import tempfile
from insert_code import *

VERBOSE                       =  False
SUFFIX                        =  ''
ADDRESS_TABLE_TOP             =  ''
CONSTANTS_FILE                =  ''
DOC_FILE                      =  ''
PACKAGE_FILE                  =  ''
TOP_NODE_NAME                 =  ''
VHDL_REG_GENERATED_DISCLAIMER =  ''

USED_REGISTER_SPACE           =  {}

CONFIG_TEST = {
    'ADDRESS_TABLE_TOP'             : 'test/test.xml',
    'CONSTANTS_FILE'                : 'test/registers.vhd',
    'DOC_FILE'                      : 'test/address_table.tex',
    'PACKAGE_FILE'                  : 'test/ipbus_pkg.vhd',
    'TOP_NODE_NAME'                 : 'FPGA'
}

CONFIG_OH = {
    'ADDRESS_TABLE_TOP'             : '../optohybrid_registers.xml',
    'CONSTANTS_FILE'                : '../src/pkg/registers.vhd',
    'DOC_FILE'                      : '../doc/latex/address_table.tex',
    'PACKAGE_FILE'                  : '../src/pkg/ipbus_pkg.vhd',
    'TOP_NODE_NAME'                 : 'FPGA'
}

CONFIG_AMC = {
    'ADDRESS_TABLE_TOP'             : './address_table/gem_amc_top.xml',
    'CONSTANTS_FILE'                : '../common/hdl/pkg/registers.vhd',
    'DOC_FILE'                      : '../doc/latex/table2.tex',
    'PACKAGE_FILE'                  : '',
    'TOP_NODE_NAME'                 : 'GEM_AMC'
}

VHDL_REG_CONSTANT_PREFIX = 'REG_'

VHDL_REG_SIGNAL_MARKER_START = '------ Register signals begin'
VHDL_REG_SIGNAL_MARKER_END   = '------ Register signals end'

VHDL_REG_SLAVE_MARKER_START = '--==== Registers begin'
VHDL_REG_SLAVE_MARKER_END   = '--==== Registers end'

class Module:
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

    def __init__(self):
        """"""
        self.regs    = []
        self.parents = []

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
        return self.name.replace(TOP_NODE_NAME + '.', '').replace('.', '_')

class Register:
    """"""

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
        return self.name.replace(TOP_NODE_NAME + '.', '').replace('.', '_')

def main():

    parser = argparse.ArgumentParser()

    #parser.add_argument('-x',
    #                    '--xml',
    #                    dest='verbose',
    #                    help="Verbose print out")

    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        help="Verbose print out")

    parser.add_argument('-s',
                        '--suffix',
                        dest='suffix',
                        help="Specify an optional suffix to copy the file onto")

    parser.add_argument('-n',
                        '--num_ohs',
                        dest='num_ohs',
                        help="Number of optohybrids to build for")

    parser.add_argument('board_type',
                        help="Choose board type (ctp7 or glib or oh)")

    args = parser.parse_args()

    board_type = args.board_type
    global VERBOSE
    VERBOSE = args.verbose

    if board_type in ('glib', 'ctp7'):
        config = CONFIG_AMC
        if args.num_ohs is not None:
            num_of_oh = args.num_ohs
            print('Generating address table with num_of_oh = %d'%(num_of_oh))
        elif board_type == 'ctp7':
            num_of_oh = 4
        elif board_type == 'glib':
            num_of_oh = 2
    elif board_type == 'test':
        num_of_oh = 1
        config = CONFIG_TEST
    elif board_type == 'oh':
        num_of_oh = 0
        config = CONFIG_OH
    else:
        print ()
        sys.exit(1)

    global ADDRESS_TABLE_TOP
    global CONSTANTS_FILE
    global DOC_FILE
    global PACKAGE_FILE
    global TOP_NODE_NAME
    global VHDL_REG_GENERATED_DISCLAIMER
    global SUFFIX

    if args.suffix is not None:
        SUFFIX = args.suffix;

    ADDRESS_TABLE_TOP             = config['ADDRESS_TABLE_TOP']
    CONSTANTS_FILE                = config['CONSTANTS_FILE']
    DOC_FILE                      = config['DOC_FILE']
    PACKAGE_FILE                  = config['PACKAGE_FILE']
    TOP_NODE_NAME                 = config['TOP_NODE_NAME']
    VHDL_REG_GENERATED_DISCLAIMER = '(this section is generated by generate_registers.py -- do not edit)'

    ADDRESS_TABLE_TOP = ADDRESS_TABLE_TOP.replace(".xml",SUFFIX+".xml")
    print('Hi, parsing this top address table file: ' + ADDRESS_TABLE_TOP)

    tree = xml.parse(ADDRESS_TABLE_TOP)
    root = tree.getroot()

    modules = []
    variables = {}

    find_registers(root, '', 0x0, modules, None, variables, False, num_of_oh)

    if VERBOSE:
        print('Modules:')
        for module in modules:
            module.regs.sort(key=lambda reg: reg.address * 100 + reg.msb)
            print('============================================================================')
            print(module.to_string())
            print('============================================================================')
            for reg in module.regs:
                print(reg.to_string())

    print('Writing constants file to ' + CONSTANTS_FILE.replace(".vhd",SUFFIX+".vhd"))
    write_constants_file(modules, CONSTANTS_FILE.replace(".vhd",SUFFIX+".vhd"))

    print('Writing documentation file to ' + DOC_FILE.replace(".tex",SUFFIX+".tex"))
    write_docFile (modules, DOC_FILE)

    print('Writing org file to ' + DOC_FILE.replace(".org",SUFFIX+".org"))
    writeOrgFile (modules, DOC_FILE.replace(".tex",".org"))

    if PACKAGE_FILE!='':
        print('Writing package file to ' + PACKAGE_FILE)
        write_package_file (modules, PACKAGE_FILE)

    for module in modules:
        if not module.is_external:
            update_module_file(module)

def find_registers(node, base_name, base_address, modules, current_module, variables, is_generated, num_of_oh):

    if is_generated in (None, False) \
       and node.get('generate') is not None \
       and node.get('generate') == 'true':

        if node.get('generate_idx_var') == 'OH_IDX':
            generate_size = num_of_oh
            variables [node.get('generate_idx_var')+'_LOOP_SIZE'] = generate_size
        else:
            generate_size = parse_int(node.get('generate_size'))
            variables [node.get('generate_idx_var')+'_LOOP_SIZE'] = generate_size

        generate_address_step = parse_int(node.get('generate_address_step'))
        generate_idx_var = node.get('generate_idx_var')

        for i in range(0, generate_size):

            variables[generate_idx_var] = i
            variables[generate_idx_var + "_STEP_SIZE"] = generate_address_step
            #print('generate base_addr = ' + hex(base_address + generate_address_step * i) + ' for node ' + node.get('id'))

            find_registers(node, base_name, base_address + generate_address_step * i, \
                          modules, current_module, variables, True, num_of_oh)
        return

    is_module = node.get('fw_is_module') is not None and node.get('fw_is_module') == 'true'
    name = base_name
    module = current_module
    if base_name != '':
        name += '.'

    if node.get('id') is not None:
        name += node.get('id')

    address = base_address

    if is_module:
        module, modules=process_module (name, node, modules, variables)
    else:
        address, node, module, modules = \
            process_register(name, base_address, node, module, modules, variables)

    for child in node:
        find_registers(child, name, address, modules, module, variables, False, num_of_oh)

def writeOrgFile (modules, filename):

    def convert_newlines(string):
        if string is None:
            string=""
        ret = string.replace('\\n','|\n|            |      |         |     |     |  ')
        return ret

    def write_module_name (f, module):
        module_name = module.name
        f.write ('\n')
        f.write ('* Module %s \t adr = ~0x%x~\n' % (module_name, module.base_address))
        f.write ('\n')
        f.write ('%s\n' % (module.description))
        f.write ('\n')

    def write_end_of_table (f):
        f.write('\n')

    def write_parent_name (f, parent_name):
        f.write('*%s*\n' % parent_name)
        f.write('\n')

    def write_parent_description (f, parent_description):
        f.write('%s\n' % parent_description.replace("\\\\","\n\n"))
        f.write('\n')

    def write_parent_generators (f, parent):

        def idx_to_xyz (idx):
            return idx.replace('GBT_IDX','GBT{N}').replace('OH_IDX','OH{X}').replace('VFAT_IDX','VFAT{Y}').replace('CHANNEL_IDX','CHANNEL{Z}')

        for key in parent.genvars.keys():
            f.write('Generated range of %s is ~[%d:0]~ adr_step = ~0x%X~ (%d)\n' % (idx_to_xyz(key), parent.gensize[key]-1, parent.genstep[key], parent.genstep[key]))

    def write_start_of_reg_table (f):
        f.write('|------------+------+---------+------+-----+----------------------------|\n')
        f.write('| Node       | Adr  | Bits    | Perm | Def | Description                |\n')
        f.write('|------------+------+---------+------+-----+----------------------------|\n')

    def write_reg_entry (f, endpoint_name, address, bithi, bitlo, permission, default, description):

        if default!="Pulsed":
            if (permission!="r"):
                default = ("~%s~" % default)
        else:
            default="Pulse"

        bitstr = ("[%d:%d]" % (bithi, bitlo))
        if bithi==bitlo:
            bitstr = ("%d" % (bithi))

        f.write('|%s | ~0x%x~ | ~%s~ | %s | %s | %s | \n' % (endpoint_name, address, bitstr, permission, default, convert_newlines(description)))
        f.write('|------------+------+---------+-----+-----+----------------------------|\n')

    def write_doc (filename):

        f = filename

        for module in modules:

            print ("    > writing documentation for " + module.name)
            ################################################################################
            # Nodes to skip from documentation
            ################################################################################

            if module.name=="GEM_AMC.GLIB_SYSTEM":
                continue

            ################################################################################
            # Write module name
            ################################################################################

            write_module_name (f, module)

            ################################################################################

            # only want to write the table header and parent name once
            name_of_last_parent_node = ""

            ################################################################################
            # Loop over registers
            ################################################################################

            reg_is_first_in_parent = 1

            for reg in module.regs:

                # Only want to document the first instance in a loop of OH, VFAT, or Channel
                # allow other loops to unroll...

                is_first_in_loop = 1
                reg_unrolling_is_supressed = 0
                for key in reg.genvars.keys():
                    if (key == "GBT_IDX" or key == "OH_IDX" or key == "VFAT_IDX" or key == "CHANNEL_IDX"):
                        reg_unrolling_is_supressed = 1
                        if (reg.genvars[key] > 0):
                            is_first_in_loop = 0

                if is_first_in_loop == 0:
                    continue

                name          = reg.name
                name_split    = reg.name_raw.split('.')
                address       = reg.address + module.base_address


                endpoint_name = reg.name.split('.')[-1]

                name_of_parent_node = ""

                # find the name of the current node's parent

                for i in range (len(name_split)-1):
                    name_of_parent_node = name_of_parent_node + name_split[i]
                    if (i!=(len(name_split)-2)):
                        name_of_parent_node = name_of_parent_node + "."

                # find the parent module
                reg_parent = Register()
                parent_found = 0
                for parent in module.parents:
                    if name_of_parent_node==parent.name_raw:
                        reg_parent=parent
                        parent_found = 1

                # error if we can't find the parent

                if not parent_found:
                    raise ValueError("Somethings wrong... parent not found for node %s" % name);

                # write a header if this is a new parent

                if (name_of_parent_node != name_of_last_parent_node):

                    if (not reg_is_first_in_parent):
                        write_end_of_table(f)

                    reg_is_first_in_parent = 0

                    variables = { 'GBT_IDX' : '{N}' , 'OH_IDX' : '{X}' , 'VFAT_IDX' : '{Y}', 'CHANNEL_IDX' : '{Z}' }

                    # Write name of parent node
                    write_parent_name (f, substitute_vars(reg_parent.name_raw, variables))

                    # If parent has a description, write it
                    if (reg_parent.description!="" and reg_parent.description!=None):
                        write_parent_description (f, substitute_vars(reg_parent.description_raw, variables))

                    # If parent is a generator, record generation properties
                    if (len(reg_parent.genvars)>0):
                        write_parent_generators (f, reg_parent)

                    # write the reg table preampble
                    write_start_of_reg_table (f)

                name_of_last_parent_node = name_of_parent_node

                reg_default=""

                if (reg.default!=None):
                    if (reg.default==-1):
                        reg_default = ""
                    else:
                        reg_default = "0x%X" % reg.default
                if reg.write_pulse_signal!=None:
                    reg_default = "Pulsed"

                description=""
                if (reg_unrolling_is_supressed ):
                    description=substitute_vars(reg.description_raw,variables)
                else:
                    description=reg.description

                # write register entry
                write_reg_entry (f, endpoint_name, address, reg.msb, reg.lsb, reg.permission, reg_default, description)

            # end of table

            write_end_of_table (f)

        print ("    > finished writing all documentation...")

    MARKER_START = "# START: ADDRESS_TABLE :: DO NOT EDIT"
    MARKER_END   = "# END: ADDRESS_TABLE :: DO NOT EDIT"

    outfile = filename.replace(".org",SUFFIX+".org")
    insert_code (filename, outfile, MARKER_START, MARKER_END, write_doc)

def write_docFile (modules, filename):

    def latexify(string):
        if string is None:
            string=""
        return string.replace('\\\\','\\\\\\\\').replace('&','\&').replace('%','\%').replace('$','\$').replace('#','\#').replace('_','\_').replace('{','\{').replace('}','\}').replace('~','\~').replace('^','\^')

    def convert_newlines(string):
        if string is None:
            string=""
        return string.replace('\\n','\\\\ & & & & &')

    def write_module_name_latex (f, module):
        padding = "    "
        module_name = module.name
        f.write ('\n')
        f.write ('%s\pagebreak\n' % (padding))
        f.write ('%s\\section{Module: %s \\hfill \\texttt{0x%x}}\n' % (padding, latexify(module_name), module.base_address))
        f.write ('\n')
        f.write ('%s%s\\\\\n' % (padding, latexify(module.description)))
        f.write ('\n')
        f.write ('%s\\renewcommand{\\arraystretch}{1.3}\n' % (padding))

    def write_end_of_table_latex (f):
        padding = "    "
        f.write('%s\\end{tabularx}\n' % (padding))
        f.write('%s\\vspace{5mm}\n' % (padding))
        f.write('\n\n')

    def write_parent_name_latex (f, parent_name):
        padding = "    "
        f.write('%s\\noindent\n' % (padding))
        f.write('%s\\subsection*{\\textcolor{parentcolor}{\\textbf{%s}}}\n' % (padding, latexify(parent_name)))
        f.write ('\n')

    def write_parent_description_latex (f, parent_description):
        padding = "    "
        f.write('%s\\vspace{4mm}\n' % (padding))
        f.write('%s\\noindent\n' % (padding))
        f.write('%s%s\n' % (padding, latexify(parent_description)))
        f.write('%s\\noindent\n' % (padding))
        f.write('\n')

    def write_parent_generators_latex (f, parent):

        def idx_to_xyz (idx):
            return idx.replace('GBT_IDX','GBT{N}').replace('OH_IDX','OH{X}').replace('VFAT_IDX','VFAT{Y}').replace('CHANNEL_IDX','CHANNEL{Z}')

        padding = "    "
        f.write ('%s\\noindent\n' % (padding) )
        f.write ('%s\\keepXColumns\n' % (padding))
        f.write ('%s\\begin{tabularx}{\\linewidth}{  l  l  l  r   X }\n' % (padding))
        for key in parent.genvars.keys():
            f.write('%sGenerated range of & %s & is & \\texttt{[%d:0]} & adr\_step=0x%X (%d) \\\\ \n' % (padding,  latexify(idx_to_xyz(key)), parent.gensize[key]-1, parent.genstep[key], parent.genstep[key]))
        f.write('%s\\end{tabularx}\n' % (padding))

    def write_start_of_reg_table_latex (f):
        padding = "    "
        f.write ('%s\\keepXColumns\n' % (padding))
        f.write ('%s\\begin{tabularx}{\\linewidth}{ | l | l | r | c | l | X | }\n' % (padding))
        f.write('%s\\hline\n' % (padding))
        f.write('%s\\textbf{Node} & \\textbf{Adr} & \\textbf{Bits} & \\textbf{Perm} & \\textbf{Def} & \\textbf{Description} \\\\\\hline\n' % (padding))
        f.write('%s\\nopagebreak\n' % (padding))

    def write_reg_entry_latex (f, endpoint_name, address, bithi, bitlo, permission, default, description):

        padding = "    "
        if (default!="Pulsed"):
            default = "\\texttt{%s}" % default
        else:
            default="Pulse"

        f.write('%s%s & \\texttt{0x%x} & \\texttt{[%d:%d]} & %s & %s & %s \\\\\hline\n' % (padding,latexify(endpoint_name), address, bithi, bitlo, permission, default, convert_newlines(latexify(description))))

    def write_doc (filename):

        f = filename

        padding = "    "


        for module in modules:

            print ("    > writing documentation for " + module.name)
            ################################################################################
            # Nodes to skip from documentation
            ################################################################################

            if module.name=="GEM_AMC.GLIB_SYSTEM":
                continue

            ################################################################################
            # Write module name
            ################################################################################

            write_module_name_latex (f, module)

            ################################################################################

            # only want to write the table header and parent name once
            name_of_last_parent_node = ""

            ################################################################################
            # Loop over registers
            ################################################################################

            reg_is_first_in_parent = 1

            for reg in module.regs:

                # Only want to document the first instance in a loop of OH, VFAT, or Channel
                # allow other loops to unroll...

                is_first_in_loop = 1
                reg_unrolling_is_supressed = 0
                for key in reg.genvars.keys():
                    if (key == "GBT_IDX" or key == "OH_IDX" or key == "VFAT_IDX" or key == "CHANNEL_IDX"):
                        reg_unrolling_is_supressed = 1
                        if (reg.genvars[key] > 0):
                            is_first_in_loop = 0

                if (is_first_in_loop == 0):
                    continue

                name          = reg.name
                name_split    = reg.name_raw.split('.')
                address       = reg.address + module.base_address


                endpoint_name = reg.name.split('.')[-1]

                name_of_parent_node = ""

                # find the name of the current node's parent

                for i in range (len(name_split)-1):
                    name_of_parent_node = name_of_parent_node + name_split[i]
                    if (i!=(len(name_split)-2)):
                        name_of_parent_node = name_of_parent_node + "."

                # find the parent module
                reg_parent = Register()
                parent_found = 0
                for parent in module.parents:
                    if name_of_parent_node==parent.name_raw:
                        reg_parent=parent
                        parent_found = 1

                # error if we can't find the parent

                if (not parent_found):
                    raise ValueError("Somethings wrong... parent not found for node %s" % name);

                # write a header if this is a new parent

                if (name_of_parent_node != name_of_last_parent_node):

                    if (not reg_is_first_in_parent):
                        write_end_of_table_latex(f)

                    reg_is_first_in_parent = 0

                    variables = { 'GBT_IDX' : '{N}' , 'OH_IDX' : '{X}' , 'VFAT_IDX' : '{Y}', 'CHANNEL_IDX' : '{Z}' }

                    # Write name of parent node
                    write_parent_name_latex (f, substitute_vars(reg_parent.name_raw, variables))

                    # If parent has a description, write it
                    if (reg_parent.description!="" and reg_parent.description!=None):
                        write_parent_description_latex (f, substitute_vars(reg_parent.description_raw, variables))

                    # If parent is a generator, record generation properties
                    if (len(reg_parent.genvars)>0):
                        write_parent_generators_latex (f, reg_parent)

                    # write the reg table preampble
                    write_start_of_reg_table_latex (f)

                name_of_last_parent_node = name_of_parent_node

                reg_default=""

                if (reg.default!=None):
                    if (reg.default==-1):
                        reg_default = ""
                    else:
                        reg_default = "0x%X" % reg.default
                if (reg.write_pulse_signal!=None):
                    reg_default = "Pulsed"

                description=""
                if (reg_unrolling_is_supressed ):
                    description=substitute_vars(reg.description_raw,variables)
                else:
                    description=reg.description

                # write register entry
                write_reg_entry_latex (f, endpoint_name, address, reg.msb, reg.lsb, reg.permission, reg_default, description)

            # end of table

            write_end_of_table_latex (f)

        print ("    > finished writing all documentation...")

    MARKER_START = "% START: ADDRESS_TABLE :: DO NOT EDIT"
    MARKER_END   = "% END: ADDRESS_TABLE :: DO NOT EDIT"

    outfile = filename.replace(".tex",SUFFIX+".tex")
    insert_code (filename, outfile, MARKER_START, MARKER_END, write_doc)

def write_package_file (modules, filename):

    def write_ipbus_slaves (filename):

        f = filename

        padding = "    "

        imodule=0
        f.write('%stype t_ipb_slv is record\n'             % (padding))
        for module in modules:
            if module.is_external:
                continue
            f.write('%s    %15s   : integer;\n'            % (padding, module.get_vhdl_name()))
            imodule = imodule + 1
        f.write('%send record;\n'                          % (padding))

        imodule=0
        f.write('%s-- IPbus slave index definition\n'      % (padding))
        f.write('%sconstant IPB_SLAVE : t_ipb_slv := (\n'  % (padding))
        for module in modules:
            if module.is_external:
                continue
            if (imodule != 0):
                f.write(',\n')
            f.write('%s    %15s  => %d'                 % (padding, module.get_vhdl_name(), imodule))
            imodule = imodule + 1
        f.write('%s);\n'                                   % (padding))

    def write_ipbus_addr_sel (filename):

        f = filename

        padding = "        "
        modulebits = 4

        imodule = 0

        for module in modules:

            if (imodule==0):
                start = "if   "
            else:
                start = "elsif"

            if module.is_external:
                continue
            f.write('%s%s(std_match(addr, std_logic_vector(to_unsigned(IPB_SLAVE.%15s,     %d))  & "------------")) then sel := IPB_SLAVE.%s;\n' % (padding, start, module.get_vhdl_name(), modulebits, module.get_vhdl_name()))

            imodule = imodule + 1

    MARKER_START = "-- START: IPBUS_SLAVES :: DO NOT EDIT"
    MARKER_END   = "-- END: IPBUS_SLAVES :: DO NOT EDIT"
    insert_code (filename, filename, MARKER_START, MARKER_END, write_ipbus_slaves)

    MARKER_START = "-- START: IPBUS_ADDR_SEL :: DO NOT EDIT"
    MARKER_END   = "-- END: IPBUS_ADDR_SEL :: DO NOT EDIT"
    insert_code (filename, filename, MARKER_START, MARKER_END, write_ipbus_addr_sel)


def write_constants_file(modules, filename):
    f = io.open (filename, "w", newline='')
    f.write('library IEEE;\n'\
            'use IEEE.STD_LOGIC_1164.all;\n\n')
    f.write('-----> !! This package is auto-generated from an address table file using generate_registers.py !! <-----\n')
    f.write('package registers is\n')

    for module in modules:
        if module.is_external:
            continue

        total_regs32 = get_num_required_regs32(module)

        # check if we have enough address bits for the max reg address (recall that the reg list is sorted by address)
        topAddressBinary = "{0:#0b}".format(module.regs[-1].address)
        numAddressBitsNeeded = len(topAddressBinary) - 2
        if (VERBOSE):
            print('    > Top address of the module ' + module.get_vhdl_name() + ' is ' + hex(module.regs[-1].address) + ' (' + topAddressBinary + '), need ' + str(numAddressBitsNeeded) + ' bits and have ' + str(module.reg_address_msb - module.reg_address_lsb + 1) + ' bits available')
        if numAddressBitsNeeded > module.reg_address_msb - module.reg_address_lsb + 1:
            raise ValueError('There is not enough bits in the module address space to accomodate all registers (see above for details). Please modify fw_reg_addr_msb and/or fw_reg_addr_lsb attributes in the xml file')


        f.write('\n')
        f.write('    --============================================================================\n')
        f.write('    --       >>> ' + module.get_vhdl_name() + ' Module <<<    base address: ' + hex_padded32(module.base_address) + '\n')
        f.write('    --\n')
        for line in tw.wrap(module.description, 75):
            f.write('    -- ' + line + '\n')
        f.write('    --============================================================================\n\n')

        f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_NUM_REGS : integer := ' + str(total_regs32) + ';\n')
        f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_MSB : integer := ' + str(module.reg_address_msb) + ';\n')
        f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_LSB : integer := ' + str(module.reg_address_lsb) + ';\n')
        #f.write('    type T_' + VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_ARR is array(integer range <>) of std_logic_vector(%s downto %s);\n\n' % (VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_MSB', VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_LSB')) # cannot use that because we need to be able to pass it as a generic type to the generic IPBus slave module

        for reg in module.regs:
            #print('Writing register constants for ' + reg.name)
            f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_ADDR    : '\
                        'std_logic_vector(' + str(module.reg_address_msb) + ' downto ' + str(module.reg_address_lsb) + ') := ' + \
                        vhdl_hex_padded(reg.address, module.reg_address_msb - module.reg_address_lsb + 1)  + ';\n')
            if reg.msb == reg.lsb:
                f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_BIT    : '\
                            'integer := ' + str(reg.msb) + ';\n')
            else:
                f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_MSB    : '\
                            'integer := ' + str(reg.msb) + ';\n')
                f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_LSB     : '\
                            'integer := ' + str(reg.lsb) + ';\n')
            if (reg.default==-1):
                f.write('  --constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_DEFAULT should be supplied externally\n')
            elif reg.default is not None and reg.msb - reg.lsb > 0:
                f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_DEFAULT : '\
                            'std_logic_vector(' + str(reg.msb) + ' downto ' + str(reg.lsb) + ') := ' + \
                            vhdl_hex_padded(reg.default, reg.msb - reg.lsb + 1)  + ';\n')
            elif reg.default is not None and reg.msb - reg.lsb == 0:
                f.write('    constant ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_DEFAULT : '\
                            'std_logic := ' + \
                            vhdl_hex_padded(reg.default, reg.msb - reg.lsb + 1)  + ';\n')
            f.write('\n')

    f.write('\n')
    f.write('end registers;\n')
    f.close()
    print("    > DONE" )

def update_module_file(module):

    if module.is_external:
        return

    total_regs32 = get_num_required_regs32(module)
    print('Updating ' + module.name + ' module in file = ' + module.file_name)

    # copy lines out of source file
    f = open(module.file_name, 'r+')
    lines = f.readlines()
    f.close()

    # create temp file for writing to
    tempname = tempfile.mktemp()
    shutil.copy (module.file_name, tempname)
    f = io.open (tempname, "w", newline='')

    signal_section_found = False
    signal_section_done = False
    slave_section_found = False
    slave_section_done = False
    registersLibraryFound = False
    for line in lines:
        if sys.version_info[0] < 3:
            line = unicode(line)
        if line.startswith('use work.registers.all;'):
            registersLibraryFound = True

        # if we're outside of business of writing the special sections, then just repeat the lines we read from the original file
        if (not signal_section_found or signal_section_done) and (not slave_section_found or slave_section_done):
            f.write(line)
        elif (signal_section_found and not signal_section_done and VHDL_REG_SIGNAL_MARKER_END in line):
            signal_section_done = True
            f.write(line)
        elif (slave_section_found and not slave_section_done and VHDL_REG_SLAVE_MARKER_END in line):
            slave_section_done = True
            f.write(line)

        # signal section
        if VHDL_REG_SIGNAL_MARKER_START in line:
            signal_section_found = True
            signalDeclaration         = "    signal regs_read_arr        : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
                                        "    signal regs_write_arr       : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
                                        "    signal regs_addresses       : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
                                        "    signal regs_defaults        : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
                                        "    signal regs_read_pulse_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"\
                                        "    signal regs_write_pulse_arr : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"\
                                        "    signal regs_read_ready_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '1');\n" \
                                        "    signal regs_write_done_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '1');\n" \
                                        "    signal regs_writable_arr    : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"
            signalDeclaration = signalDeclaration.replace('<num_regs>', VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_NUM_REGS')
            f.write(signalDeclaration)

            # connect counter en signal declarations
            header_written = False;
            for reg in module.regs:
                if reg.fw_cnt_en_signal is not None and reg.signal is not None:
                    if (not header_written):
                        f.write('    -- Connect counter signal declarations\n')
                        header_written = True;
                    f.write ('    signal %s : std_logic_vector (%s downto 0) := (others => \'0\');\n' % (reg.signal,  reg.msb-reg.lsb))

            header_written = False;
            for reg in module.regs:
                if reg.fw_rate_en_signal is not None and reg.signal is not None:
                    if (not header_written):
                        f.write('    -- Connect rate signal declarations\n')
                        header_written = True;
                    f.write ('    signal %s : std_logic_vector (%s downto 0) := (others => \'0\');\n' % (reg.signal,  reg.msb-reg.lsb))

        # slave section
        if VHDL_REG_SLAVE_MARKER_START in line:
            slave_section_found = True
            slaveDeclaration =  '    ipbus_slave_inst : entity work.ipbus_slave_tmr\n'\
                                '        generic map(\n'\
                                '           g_ENABLE_TMR           => %s,\n' % ('EN_TMR_IPB_SLAVE_'     + module.get_vhdl_name()) + \
                                '           g_NUM_REGS             => %s,\n' % (VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_NUM_REGS') + \
                                '           g_ADDR_HIGH_BIT        => %s,\n' % (VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_MSB') + \
                                '           g_ADDR_LOW_BIT         => %s,\n' % (VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_LSB') + \
                                '           g_USE_INDIVIDUAL_ADDRS => true\n'\
                                '       )\n'\
                                '       port map(\n'\
                                '           ipb_reset_i            => %s,\n' % (module.bus_reset) + \
                                '           ipb_clk_i              => %s,\n' % (module.bus_clock) + \
                                '           ipb_mosi_i             => %s,\n' % (module.master_bus) + \
                                '           ipb_miso_o             => %s,\n' % (module.slave_bus) + \
                                '           usr_clk_i              => %s,\n' % (module.user_clock) + \
                                '           regs_read_arr_i        => regs_read_arr,\n'\
                                '           regs_write_arr_o       => regs_write_arr,\n'\
                                '           read_pulse_arr_o       => regs_read_pulse_arr,\n'\
                                '           write_pulse_arr_o      => regs_write_pulse_arr,\n'\
                                '           regs_read_ready_arr_i  => regs_read_ready_arr,\n'\
                                '           regs_write_done_arr_i  => regs_write_done_arr,\n'\
                                '           individual_addrs_arr_i => regs_addresses,\n'\
                                '           regs_defaults_arr_i    => regs_defaults,\n'\
                                '           writable_regs_i        => regs_writable_arr\n'\
                                '      );\n'

            f.write('\n')
            f.write('    -- IPbus slave instanciation\n')
            f.write(slaveDeclaration)
            f.write('\n')

            # assign addresses
            uniqueAddresses = []
            for reg in module.regs:
                if not reg.address in uniqueAddresses:
                    uniqueAddresses.append(reg.address)
            if len(uniqueAddresses) != total_regs32:
                raise ValueError("Something's wrong.. Got a list of unique addresses which is of different length than the total number of 32bit addresses previously calculated..");

            f.write('    -- Addresses\n')
            for i in range(0, total_regs32):
                f.write('    regs_addresses(%d)(%s downto %s) <= %s;\n' % (i, VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_MSB', VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_ADDRESS_LSB', vhdl_hex_padded(uniqueAddresses[i], module.reg_address_msb - module.reg_address_lsb + 1))) # TODO: this is a hack using literal values - you should sort it out in the future and use constants (the thing is that the register address constants are not good for this since there are more of them than there are 32bit registers, so you need a constant for each group of regs that go to the same 32bit reg)
            f.write('\n')

            # connect read signals
            f.write('    -- Connect read signals\n')
            for reg in module.regs:
                is_single_bit = reg.msb == reg.lsb
                if 'r' in reg.permission:
                    f.write('    regs_read_arr(%d)(%s) <= %s;\n' % (uniqueAddresses.index(reg.address), VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_BIT' if is_single_bit else VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_MSB' + ' downto ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_LSB', reg.signal))

            f.write('\n')

            # connect write signals
            f.write('    -- Connect write signals\n')
            for reg in module.regs:
                is_single_bit = reg.msb == reg.lsb
                if 'w' in reg.permission and reg.signal is not None:
                    f.write('    %s <= regs_write_arr(%d)(%s);\n' % (reg.signal, uniqueAddresses.index(reg.address), VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_BIT' if is_single_bit else VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_MSB' + ' downto ' + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_LSB'))

            f.write('\n')

            def write_pulse_error (f, reg_type, address, name):
                f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
                f.write(" !!! ERROR: register #" + address + " in module "
                        + name + " is used for multiple + " + reg_type +
                        " pulses (there can only be one " + reg_type +
                        " per register address)\n")
                f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")

            # connect write pulse signals
            write_pulse_addresses = []
            duplicate_write_pulse_error = False
            f.write('    -- Connect write pulse signals\n')
            for reg in module.regs:
                if 'w' in reg.permission and reg.write_pulse_signal is not None:
                    if uniqueAddresses.index(reg.address) in write_pulse_addresses:
                        duplicate_write_pulse_error = True
                        write_pulse_error(f, "write pulse", str(uniqueAddresses.index(reg.address)), module.name)
                    write_pulse_addresses.append(uniqueAddresses.index(reg.address))
                    f.write('    %s <= regs_write_pulse_arr(%d);\n' % (reg.write_pulse_signal, uniqueAddresses.index(reg.address)))

            f.write('\n')

            # connect write done signals
            write_done_addresses = []
            duplicate_write_done_error = False
            f.write('    -- Connect write done signals\n')
            for reg in module.regs:
                if 'w' in reg.permission and reg.write_done_signal is not None:
                    if uniqueAddresses.index(reg.address) in write_done_addresses:
                        duplicate_write_done_error = True
                        write_pulse_error(f, "write done", str(uniqueAddresses.index(reg.address)), module.name)
                    write_done_addresses.append(uniqueAddresses.index(reg.address))
                    f.write('    regs_write_done_arr(%d) <= %s;\n' % (uniqueAddresses.index(reg.address), reg.write_done_signal))

            f.write('\n')

            # connect read pulse signals
            read_pulse_addresses = []
            duplicate_read_pulse_error = False
            f.write('    -- Connect read pulse signals\n')
            for reg in module.regs:
                if 'r' in reg.permission and reg.read_pulse_signal is not None:
                    if uniqueAddresses.index(reg.address) in read_pulse_addresses:
                        duplicate_read_pulse_error = True
                        write_pulse_error(f, "read pulse", str(uniqueAddresses.index(reg.address)), module.name)
                    read_pulse_addresses.append(uniqueAddresses.index(reg.address))
                    f.write('    %s <= regs_read_pulse_arr(%d);\n' % (reg.read_pulse_signal, uniqueAddresses.index(reg.address)))

            f.write('\n')

           # connect counter signals
            f.write('    -- Connect counter instances\n')
            for reg in module.regs:

                # COUNTER WITH SNAP
                if reg.fw_cnt_en_signal is not None and reg.fw_cnt_snap_signal != '\'1\'':
                    f.write ("\n")
                    f.write ('    COUNTER_%s : entity work.counter_snap\n' % (reg.get_vhdl_name()))
                    f.write ('    generic map (\n')
                    if (reg.fw_cnt_increment_step!='1'):
                        f.write ('        g_INCREMENT_STEP => %s,\n' % (reg.fw_cnt_increment_step))
                    if (reg.fw_cnt_allow_rollover!='false'):
                        f.write ('        g_ALLOW_ROLLOVER => %s,\n' % (reg.fw_cnt_allow_rollover))
                    f.write ('        g_COUNTER_WIDTH  => %s\n' % (reg.msb - reg.lsb + 1))
                    f.write ('    )\n')
                    f.write ('    port map (\n')
                    f.write ('        ref_clk_i => %s,\n' % (module.user_clock))
                    f.write ('        reset_i   => %s,\n' % (reg.fw_cnt_reset_signal))
                    f.write ('        en_i      => %s,\n' % (reg.fw_cnt_en_signal))
                    f.write ('        snap_i    => %s,\n' % (reg.fw_cnt_snap_signal))
                    f.write ('        count_o   => %s\n'  % (reg.signal))
                    f.write ('    );\n')
                    f.write ('\n')

                # COUNTER WITHOUT SNAP
                elif reg.fw_cnt_en_signal is not None:
                    f.write ("\n")
                    f.write ('    COUNTER_%s : entity work.counter\n' % (reg.get_vhdl_name()))
                    f.write ('    generic map (\n')
                    if (reg.fw_cnt_increment_step!='1'):
                        f.write ('        g_INCREMENT_STEP => %s,\n' % (reg.fw_cnt_increment_step))
                    if (reg.fw_cnt_allow_rollover!='false'):
                        f.write ('        g_ALLOW_ROLLOVER => %s,\n' % (reg.fw_cnt_allow_rollover))
                    f.write ('        g_COUNTER_WIDTH  => %s\n' % (reg.msb - reg.lsb + 1))
                    f.write ('    )\n')
                    f.write ('    port map (\n')
                    f.write ('        ref_clk_i => %s,\n' % (module.user_clock))
                    f.write ('        reset_i   => %s,\n' % (reg.fw_cnt_reset_signal))
                    f.write ('        en_i      => %s,\n' % (reg.fw_cnt_en_signal))
                    f.write ('        count_o   => %s\n'  % (reg.signal))
                    f.write ('    );\n')
                    f.write ('\n')

            f.write('\n')

           # connect rate signals
            f.write('    -- Connect rate instances\n')
            for reg in module.regs:

                if reg.fw_rate_en_signal is not None:
                    f.write ("\n")
                    f.write ('    RATE_CNT_%s : entity work.rate_counter\n' % (reg.get_vhdl_name()))
                    f.write ('    generic map (\n')
                    f.write ('        g_COUNTER_WIDTH      => %s,\n' % (reg.msb - reg.lsb + 1))
                    f.write ('        g_CLK_FREQUENCY      => %s,\n' % (reg.fw_rate_clk_frequency))
                    f.write ('    )\n')
                    f.write ('    port map (\n')
                    f.write ('        clk_i                => %s,\n' % (module.user_clock))
                    f.write ('        reset_i              => %s,\n' % (reg.fw_rate_reset_signal))
                    f.write ('        en_i                 => %s,\n' % (reg.fw_rate_en_signal))
                    f.write ('        rate_o               => %s\n'  % (reg.signal))
                    f.write ('    );\n')
                    f.write ('\n')

            f.write('\n')

            # connect read ready signals
            readReadyAddresses = []
            duplicate_read_ready_error = False
            f.write('    -- Connect read ready signals\n')
            for reg in module.regs:
                if 'r' in reg.permission and reg.read_ready_signal is not None:
                    if uniqueAddresses.index(reg.address) in readReadyAddresses:
                        duplicate_read_ready_error = True
                        f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
                        f.write(" !!! ERROR: register #" + str(uniqueAddresses.index(reg.address))
                                + " in module " + module.name +
                                " is used for multiple read ready signals \
                                (there can only be one read ready signal per register address)\n")
                        f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
                    readReadyAddresses.append(uniqueAddresses.index(reg.address))
                    f.write('    regs_read_ready_arr(%d) <= %s;\n' % \
                            (uniqueAddresses.index(reg.address), reg.read_ready_signal))

            f.write('\n')

            # Defaults
            f.write('    -- Defaults\n')
            writable_reg_addresses = []

            for reg in module.regs:

                is_single_bit = reg.msb == reg.lsb

                if reg.default is not None:

                    if not uniqueAddresses.index(reg.address) in writable_reg_addresses:
                        writable_reg_addresses.append(uniqueAddresses.index(reg.address))

                    if (is_single_bit):
                        bit_suffix = '_BIT'
                    else:
                        bit_suffix = '_MSB' + ' downto ' + VHDL_REG_CONSTANT_PREFIX \
                            + reg.get_vhdl_name() + '_LSB'

                    f.write('    regs_defaults(%d)(%s) <= %s;\n' % \
                            (uniqueAddresses.index(reg.address), \
                             VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + bit_suffix,
                             VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_DEFAULT'))

            f.write('\n')

            # Writable regs
            # connect read ready signals
            f.write('    -- Define writable regs\n')
            for reg_addr in writable_reg_addresses:
                    f.write("    regs_writable_arr(%d) <= '1';\n" % (reg_addr))

            f.write('\n')

    f.close()
    print((module.file_name).replace(".vhd",SUFFIX+".vhd"))
    shutil.copy (tempname, (module.file_name).replace(".vhd",SUFFIX+".vhd"))

    if not signal_section_found or not signal_section_done:
        print('--> ERROR <-- Could not find a signal section in the file.. Please include "' \
              + VHDL_REG_SIGNAL_MARKER_START + '" and "' + VHDL_REG_SIGNAL_MARKER_END \
              + '" comments denoting the area where the generated code will be inserted')
        print('        e.g. someting like that would work and look nice:')
        print('        ' + VHDL_REG_SIGNAL_MARKER_START + ' ' + VHDL_REG_GENERATED_DISCLAIMER)
        print('        ' + VHDL_REG_SIGNAL_MARKER_END + ' ----------------------------------------------')
        raise ValueError('No signal declaration markers found in %s -- see above' % module.file_name)

    if not slave_section_found or not slave_section_done:
        print('--> ERROR <-- Could not find a slave section in the file.. Please include "' \
              + VHDL_REG_SLAVE_MARKER_START + '" and "' + VHDL_REG_SLAVE_MARKER_END \
              + '" comments denoting the area where the generated code will be inserted')
        print('        e.g. someting like that would work and look nice:')
        print('        --===============================================================================================')
        print('        -- ' + VHDL_REG_GENERATED_DISCLAIMER)
        print('        ' + VHDL_REG_SLAVE_MARKER_START + ' ' + '==========================================================================')
        print('        ' + VHDL_REG_SLAVE_MARKER_END + ' ============================================================================')
        raise ValueError('No slave markers found in %s -- see above' % module.file_name)

    if not registersLibraryFound:
        raise ValueError('Registers library not included in %s -- \
        please add "use work.registers.all;"' % module.file_name)
    if duplicate_write_pulse_error:
        raise ValueError("Two or more write pulse signals in module %s \
        are associated with the same register address \
        (only one write pulse per reg address is allowed), \
        more details are printed to the module file" % module.file_name)
    if duplicate_write_done_error:
        raise ValueError("Two or more write done signals in module %s \
        are associated with the same register address \
        (only one write done signal per reg address is allowed), \
        more details are printed to the module file" % module.file_name)
    if duplicate_read_pulse_error:
        raise ValueError("Two or more read pulse signals in module %s \
        are associated with the same register address \
        (only one read pulse per reg address is allowed), \
        more details are printed to the module file" % module.file_name)
    if duplicate_read_ready_error:
        raise ValueError("Two or more read ready signals in module %s \
        are associated with the same register address \
        (only one read ready signal per reg address is allowed), \
        more details are printed to the module file" % module.file_name)

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
        if (num_single_bits != 0):
            ret += "'" if num_single_bits == 1 else '"'
            # go back from the MSB down to the boundary of the most significant nibble
            for i in range(num_bits, num_bits // 4 * 4, -1):
                ret += binary32[i *  -1]
            ret += "'" if num_single_bits == 1 else '"'


        # add the right amount of hex characters

        if num_bits // 4 > 0:
            if (num_single_bits != 0):
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

def process_module (name, node, modules, variables):
    module = Module()
    module.name = substitute_vars(name, variables)
    module.description = substitute_vars(node.get('description'), variables)
    module.base_address = parse_int(node.get('address'))
    if node.get('fw_is_module_external') is not None \
       and node.get('fw_is_module_external') == 'true':
        module.is_external = True
    else:
        module.reg_address_msb = parse_int(node.get('fw_reg_addr_msb'))
        module.reg_address_lsb = parse_int(node.get('fw_reg_addr_lsb'))
        module.file_name = node.get('fw_module_file')
        module.user_clock = node.get('fw_user_clock_signal')
        module.bus_clock = node.get('fw_bus_clock_signal')
        module.bus_reset = node.get('fw_bus_reset_signal')
        module.master_bus = node.get('fw_master_bus_signal')
        module.slave_bus = node.get('fw_slave_bus_signal')
    if not module.is_valid():
        error = 'One or more parameters for module ' + \
            module.name + ' is missing... ' + module.to_string()
        raise ValueError(error)

    # add a clone of the module as a parent node of that module
    parent                 = Register()
    parent.name            = substitute_vars(name, variables)
    parent.name_raw        = name
    parent.description_raw = module.description
    parent.address         = 0
    parent.description     = module.description
    parent.description     = module.description
    parent.gensize         = {}
    parent.genvars         = {}
    parent.genstep         = {}

    module.add_parent(parent)

    modules.append(module)

    return module,modules


def process_register(name, base_address, node, module, modules, variables):
    address = base_address
    if node.get('address') is not None:
        address = base_address + parse_int(node.get('address'))

    # need some way to discriminate parent nodes from endpoints
    if ( node.get('fw_signal')              is not None or
        ((node.get('permission')             is not None
        or node.get('mask')                   is not None
        or node.get ('fw_write_pulse_signal') is not None)
        and node.get('generate_size')         is     None
        and node.get('generate')              is     None
        and node.get('address')               is not None)
    ):
        reg = Register()
        reg.name = substitute_vars(name, variables)
        reg.name_raw = name
        reg.address = address
        reg.description_raw = node.get('description')
        reg.description = substitute_vars(node.get('description'), variables)
        reg.permission = node.get('permission')
        if node.get('mask') is None:
            reg.mask = 0xffffffff; # default to full 32bit mask if not specified
        else:
            reg.mask = parse_int(node.get('mask'))
        msb, lsb = get_low_high_from_bitmask(reg.mask)
        reg.msb = msb
        reg.lsb = lsb

        global USED_REGISTER_SPACE

        global_address = address + module.base_address
        if (global_address in USED_REGISTER_SPACE):
            if reg.permission == "rw" and (USED_REGISTER_SPACE[global_address] & reg.mask) != 0:
                error = 'Register write conflict on %s at address 0x%X' % (reg.name, global_address)
                raise ValueError(error)
            else:
                USED_REGISTER_SPACE[global_address] |= reg.mask
        else:
            USED_REGISTER_SPACE[global_address] = reg.mask

        reg.default = parse_int(node.get('fw_default'))
        if node.get('fw_signal') is not None:
            reg.signal = substitute_vars(node.get('fw_signal'), variables)
        if node.get('fw_write_pulse_signal') is not None:
            reg.write_pulse_signal = substitute_vars(node.get('fw_write_pulse_signal'), variables)
        if node.get('fw_write_done_signal') is not None:
            reg.write_done_signal = substitute_vars(node.get('fw_write_done_signal'), variables)
        if node.get('fw_read_pulse_signal') is not None:
            reg.read_pulse_signal = substitute_vars(node.get('fw_read_pulse_signal'), variables)
        if node.get('fw_read_ready_signal') is not None:
            reg.read_ready_signal = substitute_vars(node.get('fw_read_ready_signal'), variables)


        ################################################################################
        # Counters
        ################################################################################

        if node.get('fw_cnt_en_signal') is not None:
            reg.fw_cnt_en_signal = substitute_vars (node.get('fw_cnt_en_signal'),variables)
        if node.get('fw_cnt_reset_signal') is not None:
            reg.fw_cnt_reset_signal = substitute_vars (node.get('fw_cnt_reset_signal'),variables)
        else:
            reg.fw_cnt_reset_signal = module.bus_reset
        if node.get('fw_cnt_snap_signal') is not None:
            reg.fw_cnt_snap_signal = substitute_vars (node.get('fw_cnt_snap_signal'),variables)
        if node.get('fw_cnt_allow_rollover_signal') is not None:
            reg.fw_cnt_allow_rollover_signal = substitute_vars (node.get('fw_cnt_allow_rollover_signal'),variables)
        if node.get('fw_cnt_increment_step_signal') is not None:
            reg.fw_cnt_increment_step_signal = substitute_vars (node.get('fw_cnt_increment_step_signal'),variables)

        ################################################################################
        # Rate Counter
        ################################################################################

        if node.get('fw_rate_reset_signal') is not None:
            reg.fw_rate_reset_signal = substitute_vars (node.get('fw_rate_reset_signal'),variables)
        else:
            reg.fw_rate_reset_signal = module.bus_reset

        if node.get('fw_rate_log') is not None:
            reg.fw_rate_log = substitute_vars (node.get('fw_rate_log'),variables)
        if node.get('fw_rate_en_signal') is not None:
            reg.fw_rate_en_signal = substitute_vars (node.get('fw_rate_en_signal'),variables)
        if node.get('fw_rate_clk_frequency') is not None:
            reg.fw_rate_clk_frequency = substitute_vars (node.get('fw_rate_clk_frequency'),variables)
        if node.get('fw_rate_inc_width') is not None:
            reg.fw_rate_inc_width = substitute_vars (node.get('fw_rate_inc_width'),variables)
        if node.get('fw_rate_progress_bar_width') is not None:
            reg.fw_rate_progress_bar_width = substitute_vars (node.get('fw_rate_progress_bar_width'),variables)
        if node.get('fw_rate_progress_bar_step') is not None:
            reg.fw_rate_progress_bar_step = substitute_vars (node.get('fw_rate_progress_bar_step'),variables)
        if node.get('fw_rate_speedup') is not None:
            reg.fw_rate_speedup = substitute_vars (node.get('fw_rate_speedup'),variables)
        if node.get('fw_rate_progress_bar_signal') is not None:
            reg.fw_rate_progress_bar_signal = substitute_vars (node.get('fw_rate_progress_bar_signal'),variables)

        ################################################################################
        # Error
        ################################################################################

        reg.gensize={}
        reg.genvars={}
        for key in variables.keys():
            if reg.name_raw.find("${" + key + "}") > 0:
                reg.genvars [key] = variables[key]
                reg.gensize [key] = variables[key + "_LOOP_SIZE"]
                reg.genstep [key] = variables[key + "_STEP_SIZE"]

        if module is None:
            error = 'Module is not set, cannot add register ' + reg.name
            raise ValueError(error)
        if not reg.is_valid_reg(module.is_external):
            raise ValueError('One or more attributes for register %s are missing.. %s' % (reg.name, reg.to_string()))

        module.add_reg(reg)

    elif (node.get('id') is not None):

        parent                 = Register()
        parent.name            = substitute_vars(name, variables)
        parent.name_raw        = name
        parent.description_raw = node.get('description')
        parent.description     = substitute_vars(node.get('description'), variables)

        parent.gensize={}
        parent.genvars={}
        parent.genstep={}

        for key in variables.keys():
            if parent.name_raw.find("${" + key + "}") > 0:

                parent.genvars [key] = variables[key]
                parent.gensize [key] = variables[key + "_LOOP_SIZE"]
                parent.genstep [key] = variables[key + "_STEP_SIZE"]

        if (module is not None):
            module.add_parent(parent)
    return address, node, module, modules

if __name__ == '__main__':
    #if sys.version_info[0] >= 3:
    #    raise Exception("Python 2 required.")
    main()
