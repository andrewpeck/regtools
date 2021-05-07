#!/usr/bin/env python3

CONFIGS = {}

CONFIGS['test'] = {
    'ADDRESS_TABLE_TOP'             : 'test/test.xml',
    'CONSTANTS_FILE'                : 'test/registers.vhd',
    'DOC_FILE'                      : 'test/address_table.tex',
    'PACKAGE_FILE'                  : 'test/ipbus_pkg.vhd',
    'TOP_NODE_NAME'                 : 'FPGA',
    'USE_TMR'                       : True
}

CONFIGS['oh'] = {
    'ADDRESS_TABLE_TOP'             : '../address_table/gem/optohybrid_registers.xml',
    'CONSTANTS_FILE'                : '../gem/hdl/oh_fe/pkg/registers.vhd',
    'DOC_FILE'                      : '', # ../doc/latex/address_table.tex
    'PACKAGE_FILE'                  : '../gem/hdl/oh_fe/pkg/ipbus_pkg.vhd',
    'TOP_NODE_NAME'                 : 'FPGA',
    'USE_TMR'                       : True
}

CONFIGS['gem_amc'] = {
    'ADDRESS_TABLE_TOP'             : '../address_table/gem/gem_amc.xml',
    'CONSTANTS_FILE'                : '../gem/hdl/pkg/registers.vhd',
    'DOC_FILE'                      : '../doc/latex/address_table.tex',
    'PACKAGE_FILE'                  : '',
    'TOP_NODE_NAME'                 : 'GEM_AMC',
    'USE_TMR'                       : False
}

CONFIGS['csc_fed'] = {
    'ADDRESS_TABLE_TOP'             : '../address_table/csc/csc_fed.xml',
    'CONSTANTS_FILE'                : '../csc/hdl/pkg/registers.vhd',
    'DOC_FILE'                      : '../doc/latex/address_table.tex',
    'PACKAGE_FILE'                  : '',
    'TOP_NODE_NAME'                 : 'CSC_FED',
    'USE_TMR'                       : False
}
