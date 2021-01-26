#!/usr/bin/env python3
from __future__ import unicode_literals
from __future__ import print_function

from insert_code import insert_code
from utils import *

def write_latex_file (modules, filename, SUFFIX):

    def latexify(string):

        if string is None:
            string=""

        return string.replace('\\\\','\\\\\\\\')\
                     .replace('&','\\&')\
                     .replace('%','\\%')\
                     .replace('$','\\$')\
                     .replace('#','\\#')\
                     .replace('_','\\_')\
                     .replace('{','\\{')\
                     .replace('}','\\}')\
                     .replace('~','\\~')\
                     .replace('^','\\^')

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
        if default!="Pulsed":
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
                    if key == "GBT_IDX" or key == "OH_IDX" or key == "VFAT_IDX" or key == "CHANNEL_IDX":
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
                    raise ValueError("Somethings wrong... parent not found for node %s" % name);

                # write a header if this is a new parent

                if name_of_parent_node != name_of_last_parent_node:

                    if not reg_is_first_in_parent:
                        write_end_of_table_latex(f)

                    reg_is_first_in_parent = 0

                    variables = { 'GBT_IDX' : '{N}' , 'OH_IDX' : '{X}' , 'VFAT_IDX' : '{Y}', 'CHANNEL_IDX' : '{Z}' }

                    # Write name of parent node
                    write_parent_name_latex (f, substitute_vars(reg_parent.name_raw, variables))

                    # If parent has a description, write it
                    if reg_parent.description!="" and reg_parent.description is not None:
                        write_parent_description_latex (f, substitute_vars(reg_parent.description_raw, variables))

                    # If parent is a generator, record generation properties
                    if len(reg_parent.genvars)>0:
                        write_parent_generators_latex (f, reg_parent)

                    # write the reg table preampble
                    write_start_of_reg_table_latex (f)

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
                write_reg_entry_latex (f, endpoint_name, address, reg.msb, reg.lsb, reg.permission, reg_default, description)

            # end of table

            write_end_of_table_latex (f)

        print ("    > finished writing all documentation...")

    MARKER_START = "% START: ADDRESS_TABLE :: DO NOT EDIT"
    MARKER_END   = "% END: ADDRESS_TABLE :: DO NOT EDIT"

    outfile = filename.replace(".tex",SUFFIX+".tex")
    insert_code (filename, outfile, MARKER_START, MARKER_END, write_doc)
