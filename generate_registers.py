#!/usr/bin/python2
from __future__ import unicode_literals
from __future__ import print_function

import io
import xml.etree.ElementTree as xml
import textwrap as tw
import argparse
import sys
import shutil
import tempfile
from write_latex import *
from write_orgmode import *
from write_package_file import *
from utils import *
from configs import *
from insert_code import insert_code

VERBOSE                       =  False
PREFIX                        =  ''
SUFFIX                        =  ''
ADDRESS_TABLE_TOP             =  ''
CONSTANTS_FILE                =  ''
DOC_FILE                      =  ''
PACKAGE_FILE                  =  ''
TOP_NODE_NAME                 =  ''
VHDL_REG_GENERATED_DISCLAIMER =  ''

USED_REGISTER_SPACE           =  {}

VHDL_REG_CONSTANT_PREFIX = 'REG_'

VHDL_REG_SIGNAL_MARKER_START = '------ Register signals begin'
VHDL_REG_SIGNAL_MARKER_END   = '------ Register signals end'

VHDL_REG_SLAVE_MARKER_START = '--==== Registers begin'
VHDL_REG_SLAVE_MARKER_END   = '--==== Registers end'

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

    parser.add_argument('-p',
                        '--prefix',
                        dest='prefix',
                        help="Specify an optional prefix to copy the file onto")

    parser.add_argument('-s',
                        '--suffix',
                        dest='suffix',
                        help="Specify an optional suffix to copy the file onto")

    parser.add_argument('config_name',
                        help="Choose a config from the config.py file (e.g. gem_amc, csc_fed, oh)")

    args = parser.parse_args()

    config_name = args.config_name
    global VERBOSE
    VERBOSE = args.verbose

    if not config_name in CONFIGS:
        raise ValueError('Config name "%s" does not exist in config.py' % config_name)

    config = CONFIGS[config_name]

    global ADDRESS_TABLE_TOP
    global CONSTANTS_FILE
    global DOC_FILE
    global PACKAGE_FILE
    global TOP_NODE_NAME
    global VHDL_REG_GENERATED_DISCLAIMER
    global SUFFIX
    global PREFIX

    if args.suffix is not None:
        SUFFIX = args.suffix

    if args.prefix is not None:
        PREFIX = args.prefix

    ADDRESS_TABLE_TOP             = config['ADDRESS_TABLE_TOP']
    CONSTANTS_FILE                = config['CONSTANTS_FILE']
    DOC_FILE                      = config['DOC_FILE']
    PACKAGE_FILE                  = config['PACKAGE_FILE']
    TOP_NODE_NAME                 = config['TOP_NODE_NAME']
    USE_TMR                       = config['USE_TMR']
    VHDL_REG_GENERATED_DISCLAIMER = '(this section is generated by generate_registers.py -- do not edit)'

    ADDRESS_TABLE_TOP = updateFilename(ADDRESS_TABLE_TOP, PREFIX, SUFFIX)
    print('Hi, parsing this top address table file: ' + ADDRESS_TABLE_TOP)

    tree = xml.parse(ADDRESS_TABLE_TOP)
    root = tree.getroot()

    modules = []
    variables = {}

    find_registers(root, '', 0x0, modules, None, variables, False)

    for module in modules:
        module.regs.sort(key=lambda reg: reg.address * 100 + reg.msb)

    if VERBOSE:
        print('Modules:')
        for module in modules:
            print('============================================================================')
            print(module.to_string())
            print('============================================================================')
            for reg in module.regs:
                print(reg.to_string())

    CONSTANTS_FILE = updateFilename(CONSTANTS_FILE, PREFIX, SUFFIX)
    print('Writing constants file to ' + CONSTANTS_FILE)
    write_constants_file(modules, CONSTANTS_FILE)

#    DOC_FILE = updateFilename(DOC_FILE, PREFIX, SUFFIX)
#    print('Writing documentation file to ' + DOC_FILE)
#    write_latex_file (modules, DOC_FILE, "")

#    ORG_FILE = updateFilename(DOC_FILE.replace(".tex",".org"), PREFIX, SUFFIX)
#    print('Writing org file to ' + ORG_FILE)
#    write_org_file (modules, ORG_FILE, SUFFIX)

    if PACKAGE_FILE!='':
        print('Writing package file to ' + PACKAGE_FILE)
        write_package_file (modules, PACKAGE_FILE)

    for module in modules:
        if not module.is_external:
            update_module_file(module, PREFIX, SUFFIX, USE_TMR)

def find_registers(node, base_name, base_address, modules, current_module, variables, is_generated):

    if node.get('ignore') is not None and eval(node.get('ignore')) == True:
        return

    if is_generated in (None, False) \
       and node.get('generate') is not None \
       and node.get('generate') == 'true':

        generate_size = parse_int(node.get('generate_size'))
        variables [node.get('generate_idx_var')+'_LOOP_SIZE'] = generate_size

        generate_address_step = parse_int(node.get('generate_address_step'))
        generate_idx_var = node.get('generate_idx_var')

        for i in range(0, generate_size):
            variables[generate_idx_var] = i
            variables[generate_idx_var + "_STEP_SIZE"] = generate_address_step
            find_registers(node, base_name, base_address + generate_address_step * i, \
                          modules, current_module, variables, True)
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
        find_registers(child, name, address, modules, module, variables, False)



def write_constants_file(modules, filename):
    """"""
    f = io.open (filename, "w", newline='')
    f.write('library IEEE;\n'\
            'use IEEE.STD_LOGIC_1164.all;\n\n')
    f.write('-----> !! This package is auto-generated from an address table file using generate_registers.py !! <-----\n')
    f.write('package registers is\n')

    for module in modules:
        if module.is_external:
            continue

        total_regs32 = get_num_required_regs32(module)

        # check if we have enough address bits for the max reg address
        # (recall that the reg list is sorted by address)
        top_address_binary = "{0:#0b}".format(module.regs[-1].address)
        num_address_bits_needed = len(top_address_binary) - 2
        if VERBOSE:
            print('    > Top address of the module ' + module.get_vhdl_name() + ' is ' +
                  hex(module.regs[-1].address) + ' (' + top_address_binary + '), need ' +
                  str(num_address_bits_needed) + ' bits and have ' +
                  str(module.reg_address_msb - module.reg_address_lsb + 1) + ' bits available')

        if num_address_bits_needed > module.reg_address_msb - module.reg_address_lsb + 1:
            raise ValueError('There is not enough bits in the module address space to accomodate \
            all registers (see above for details). Please modify fw_reg_addr_msb and/or fw_reg_addr_lsb attributes in the xml file')


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

        for reg in module.regs:

            if (VERBOSE):
                print('Writing register constants for ' + reg.name)
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
            if reg.default==-1:
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

def update_module_file(module, prefix, suffix, use_tmr):

    if module.is_external:
        return

    total_regs32 = get_num_required_regs32(module)
    print('Updating ' + module.name + ' module in file = ' + module.file_name)

    def check_for_library_declaration (filename):
        search = open(filename)
        for line in search:
            if line.startswith('use work.registers.all;'):
                return True
        raise ValueError('Registers library not included in %s -- \
            please add "use work.registers.all;"' % module.file_name)

    def write_signals (filename):
        signal_declaration        = "    signal regs_read_arr        : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
            "    signal regs_write_arr       : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
            "    signal regs_addresses       : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
            "    signal regs_defaults        : t_std32_array(<num_regs> - 1 downto 0) := (others => (others => '0'));\n"\
            "    signal regs_read_pulse_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"\
            "    signal regs_write_pulse_arr : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"\
            "    signal regs_read_ready_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '1');\n" \
            "    signal regs_write_done_arr  : std_logic_vector(<num_regs> - 1 downto 0) := (others => '1');\n" \
            "    signal regs_writable_arr    : std_logic_vector(<num_regs> - 1 downto 0) := (others => '0');\n"
        signal_declaration = signal_declaration.replace('<num_regs>', VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + '_NUM_REGS')
        filename.write(signal_declaration)
        header_written = False;
        for reg in module.regs:
            if reg.fw_cnt_en_signal is not None and reg.signal is not None:
                if not header_written:
                    filename.write('    -- Connect counter signal declarations\n')
                    header_written = True;
                filename.write ('    signal %s : std_logic_vector (%s downto 0) := (others => \'0\');\n' % (reg.signal,  reg.msb-reg.lsb))

        header_written = False;
        for reg in module.regs:
            if reg.fw_rate_en_signal is not None and reg.signal is not None:
                if not header_written:
                    filename.write('    -- Connect rate signal declarations\n')
                    header_written = True;
                filename.write ('    signal %s : std_logic_vector (%s downto 0) := (others => \'0\');\n' % (reg.signal,  reg.msb-reg.lsb))

    def write_slaves (filename):
        f=filename
        slave_entity = "ipbus_slave_tmr" if use_tmr else "ipbus_slave"
        slave_declaration = '    ipbus_slave_inst : entity work.%s\n' % slave_entity + \
                            '        generic map(\n' + \
                           ('           g_ENABLE_TMR           => %s,\n' % ('EN_TMR_IPB_SLAVE_'     + module.get_vhdl_name()) if use_tmr else "") + \
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
                            '           writable_regs_i        => regs_writable_arr,\n'\
                            '           tmr_err_o              => ipb_slave_tmr_err\n'\
                            '      );\n'

        f.write('\n')
        f.write('    -- IPbus slave instanciation\n')
        f.write(slave_declaration)
        f.write('\n')

        # assign addresses
        unique_addresses = []
        for reg in module.regs:
            if not reg.address in unique_addresses:
                unique_addresses.append(reg.address)
        if len(unique_addresses) != total_regs32:
            raise ValueError("Something's wrong.. Got a list of unique addresses which \
            is of different length than the total number of 32bit addresses previously calculated..\
            num unique addresses = %d, total calculated addresses = %d" % (len(unique_addresses), total_regs32));

        f.write('    -- Addresses\n')
        for i in range(0, total_regs32):
            # TODO: this is a hack using literal values - you should sort it out in the future and
            # use constants (the thing is that the register address constants are not good for this
            # since there are more of them than there are 32bit registers, so you need a constant
            # for each group of regs that go to the same 32bit reg)
            bit_high = VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + "_ADDRESS_MSB"
            bit_lo = VHDL_REG_CONSTANT_PREFIX + module.get_vhdl_name() + "_ADDRESS_LSB"
            vhdl_adr = vhdl_hex_padded(unique_addresses[i], module.reg_address_msb - module.reg_address_lsb + 1)
            f.write('    regs_addresses(%d)(%s downto %s) <= %s;\n' % (i, bit_high, bit_lo, vhdl_adr))
        f.write('\n')

        # connect read signals
        f.write('    -- Connect read signals\n')
        for reg in module.regs:
            is_single_bit = reg.msb == reg.lsb
            if 'r' in reg.permission:
                adr = unique_addresses.index(reg.address)
                if is_single_bit:
                    bitrange = VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_BIT"
                else:
                    bitrange = VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_MSB" + \
                        " downto " +VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_LSB"
                f.write('    regs_read_arr(%d)(%s) <= %s;\n' % (adr, bitrange, reg.signal))
        f.write('\n')

        # connect write signals
        f.write('    -- Connect write signals\n')
        for reg in module.regs:
            is_single_bit = reg.msb == reg.lsb
            if 'w' in reg.permission and reg.signal is not None:
                adr = unique_addresses.index(reg.address)
                if is_single_bit:
                    bitrange = VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_BIT"
                else:
                    bitrange = VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_MSB" + \
                        " downto " + VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + "_LSB"
                f.write('    %s <= regs_write_arr(%d)(%s);\n' % (reg.signal, adr, bitrange))
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
                if unique_addresses.index(reg.address) in write_pulse_addresses:
                    duplicate_write_pulse_error = True
                    write_pulse_error(f, "write pulse", str(unique_addresses.index(reg.address)), module.name)
                write_pulse_addresses.append(unique_addresses.index(reg.address))
                f.write('    %s <= regs_write_pulse_arr(%d);\n' % (reg.write_pulse_signal,
                                                                   unique_addresses.index(reg.address)))
        f.write('\n')

        # connect write done signals
        write_done_addresses = []
        duplicate_write_done_error = False
        f.write('    -- Connect write done signals\n')
        for reg in module.regs:
            if 'w' in reg.permission and reg.write_done_signal is not None:
                if unique_addresses.index(reg.address) in write_done_addresses:
                    duplicate_write_done_error = True
                    write_pulse_error(f, "write done", str(unique_addresses.index(reg.address)), module.name)
                write_done_addresses.append(unique_addresses.index(reg.address))
                f.write('    regs_write_done_arr(%d) <= %s;\n' % (unique_addresses.index(reg.address),
                                                                  reg.write_done_signal))
        f.write('\n')

        # connect read pulse signals
        read_pulse_addresses = []
        duplicate_read_pulse_error = False
        f.write('    -- Connect read pulse signals\n')
        for reg in module.regs:
            if 'r' in reg.permission and reg.read_pulse_signal is not None:
                if unique_addresses.index(reg.address) in read_pulse_addresses:
                    duplicate_read_pulse_error = True
                    write_pulse_error(f, "read pulse", str(unique_addresses.index(reg.address)), module.name)
                read_pulse_addresses.append(unique_addresses.index(reg.address))
                f.write('    %s <= regs_read_pulse_arr(%d);\n' % (reg.read_pulse_signal,
                                                                  unique_addresses.index(reg.address)))
        f.write('\n')

        # connect counter signals
        f.write('    -- Connect counter instances\n')
        for reg in module.regs:

            # COUNTER WITH SNAP
            if reg.fw_cnt_en_signal is not None and reg.fw_cnt_snap_signal != '\'1\'':
                if (reg.fw_cnt_use_tmr):
                    tmr = "_tmr"
                else:
                    tmr = ""
                f.write ("\n")
                f.write ('    COUNTER_%s : entity work.counter_snap%s\n' % (reg.get_vhdl_name(), tmr))
                f.write ('    generic map (\n')
                if reg.fw_cnt_increment_step!='1':
                    f.write ('        g_INCREMENT_STEP => %s,\n' % (reg.fw_cnt_increment_step))
                if reg.fw_cnt_allow_rollover!='false':
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
                if reg.fw_cnt_increment_step!='1':
                    f.write ('        g_INCREMENT_STEP => %s,\n' % (reg.fw_cnt_increment_step))
                if reg.fw_cnt_allow_rollover!='false':
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
        read_ready_addresses = []
        duplicate_read_ready_error = False
        f.write('    -- Connect read ready signals\n')
        for reg in module.regs:
            if 'r' in reg.permission and reg.read_ready_signal is not None:
                if unique_addresses.index(reg.address) in read_ready_addresses:
                    duplicate_read_ready_error = True
                    f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
                    f.write(" !!! ERROR: register #" + str(unique_addresses.index(reg.address))
                            + " in module " + module.name +
                            " is used for multiple read ready signals \
                            (there can only be one read ready signal per register address)\n")
                    f.write(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n")
                read_ready_addresses.append(unique_addresses.index(reg.address))
                f.write('    regs_read_ready_arr(%d) <= %s;\n' % \
                        (unique_addresses.index(reg.address), reg.read_ready_signal))

        f.write('\n')

        # Defaults
        f.write('    -- Defaults\n')
        writable_reg_addresses = []

        for reg in module.regs:

            is_single_bit = reg.msb == reg.lsb

            if reg.default is not None:

                if not unique_addresses.index(reg.address) in writable_reg_addresses:
                    writable_reg_addresses.append(unique_addresses.index(reg.address))

                if is_single_bit:
                    bit_suffix = '_BIT'
                else:
                    bit_suffix = '_MSB' + ' downto ' + VHDL_REG_CONSTANT_PREFIX \
                        + reg.get_vhdl_name() + '_LSB'

                f.write('    regs_defaults(%d)(%s) <= %s;\n' % \
                        (unique_addresses.index(reg.address), \
                            VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + bit_suffix,
                            VHDL_REG_CONSTANT_PREFIX + reg.get_vhdl_name() + '_DEFAULT'))

        f.write('\n')

        # Writable regs
        # connect read ready signals
        f.write('    -- Define writable regs\n')
        for reg_addr in writable_reg_addresses:
                f.write("    regs_writable_arr(%d) <= '1';\n" % (reg_addr))

        f.write('\n')

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


    check_for_library_declaration(module.file_name)

    out_fname = updateFilename(module.file_name, prefix, suffix)
    insert_code (module.file_name, out_fname, VHDL_REG_SIGNAL_MARKER_START, \
                 VHDL_REG_SIGNAL_MARKER_END, write_signals)
    insert_code (out_fname, out_fname, VHDL_REG_SLAVE_MARKER_START, \
                 VHDL_REG_SLAVE_MARKER_END, write_slaves)

def process_module (name, node, modules, variables):
    module = Module(TOP_NODE_NAME)
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
    parent                 = Register(TOP_NODE_NAME)
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
    if  (node.get('fw_signal')              is not None or
        ((node.get('permission')             is not None
        or node.get('mask')                   is not None
        or node.get ('fw_write_pulse_signal') is not None)
        and node.get('generate_size')         is     None
        and node.get('generate')              is     None
        and node.get('address')               is not None)):
        reg = Register(TOP_NODE_NAME)
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
        if node.get('fw_cnt_use_tmr') is not None:
            reg.fw_cnt_use_tmr = node.get('fw_cnt_use_tmr')
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

        parent                 = Register(TOP_NODE_NAME)
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
