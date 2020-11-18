#!/usr/bin/env python3
from insert_code import insert_code
from utils import *

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
            if imodule != 0:
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

            if imodule==0:
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
