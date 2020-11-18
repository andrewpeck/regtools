#!/usr/bin/env python3

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
