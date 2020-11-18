#!/usr/bin/env python3

from insert_code import insert_code
from utils import *

def write_org_file (modules, filename, SUFFIX):

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
            if permission!="r":
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
                    if key in ("GBT_IDX", "OH_IDX", "VFAT_IDX", "CHANNEL_IDX"):
                        reg_unrolling_is_supressed = 1
                        if reg.genvars[key] > 0:
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
                    if i!=(len(name_split)-2):
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
                    raise ValueError("Somethings wrong... parent not found for node %s" % name)

                # write a header if this is a new parent

                if name_of_parent_node != name_of_last_parent_node:

                    if not reg_is_first_in_parent:
                        write_end_of_table(f)

                    reg_is_first_in_parent = 0

                    variables = { 'GBT_IDX' : '{N}' , 'OH_IDX' : '{X}' , 'VFAT_IDX' : '{Y}', 'CHANNEL_IDX' : '{Z}' }

                    # Write name of parent node
                    write_parent_name (f, substitute_vars(reg_parent.name_raw, variables))

                    # If parent has a description, write it
                    if reg_parent.description!="" and reg_parent.description is not None:
                        write_parent_description (f, substitute_vars(reg_parent.description_raw, variables))

                    # If parent is a generator, record generation properties
                    if len(reg_parent.genvars)>0:
                        write_parent_generators (f, reg_parent)

                    # write the reg table preampble
                    write_start_of_reg_table (f)

                name_of_last_parent_node = name_of_parent_node

                reg_default=""

                if reg.default is not None:
                    if reg.default==-1:
                        reg_default = ""
                    else:
                        reg_default = "0x%X" % reg.default
                if reg.write_pulse_signal is not None:
                    reg_default = "Pulsed"

                description=""
                if reg_unrolling_is_supressed:
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
