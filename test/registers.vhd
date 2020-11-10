library IEEE;
use IEEE.STD_LOGIC_1164.all;

-----> !! This package is auto-generated from an address table file using generate_registers.py !! <-----
package registers is

    --============================================================================
    --       >>> CONTROL Module <<<    base address: 0x00000000
    --
    -- Implements various control and monitoring functions of the Optohybrid
    --============================================================================

    constant REG_CONTROL_NUM_REGS : integer := 35;
    constant REG_CONTROL_ADDRESS_MSB : integer := 5;
    constant REG_CONTROL_ADDRESS_LSB : integer := 0;
    constant REG_CONTROL_LOOPBACK_DATA_ADDR    : std_logic_vector(5 downto 0) := "00" & x"0";
    constant REG_CONTROL_LOOPBACK_DATA_MSB    : integer := 31;
    constant REG_CONTROL_LOOPBACK_DATA_LSB     : integer := 0;
    constant REG_CONTROL_LOOPBACK_DATA_DEFAULT : std_logic_vector(31 downto 0) := x"01234567";

    constant REG_CONTROL_RELEASE_DATE_ADDR    : std_logic_vector(5 downto 0) := "00" & x"1";
    constant REG_CONTROL_RELEASE_DATE_MSB    : integer := 31;
    constant REG_CONTROL_RELEASE_DATE_LSB     : integer := 0;

    constant REG_CONTROL_RELEASE_VERSION_MAJOR_ADDR    : std_logic_vector(5 downto 0) := "00" & x"2";
    constant REG_CONTROL_RELEASE_VERSION_MAJOR_MSB    : integer := 7;
    constant REG_CONTROL_RELEASE_VERSION_MAJOR_LSB     : integer := 0;

    constant REG_CONTROL_RELEASE_VERSION_MINOR_ADDR    : std_logic_vector(5 downto 0) := "00" & x"2";
    constant REG_CONTROL_RELEASE_VERSION_MINOR_MSB    : integer := 15;
    constant REG_CONTROL_RELEASE_VERSION_MINOR_LSB     : integer := 8;

    constant REG_CONTROL_RELEASE_VERSION_BUILD_ADDR    : std_logic_vector(5 downto 0) := "00" & x"2";
    constant REG_CONTROL_RELEASE_VERSION_BUILD_MSB    : integer := 23;
    constant REG_CONTROL_RELEASE_VERSION_BUILD_LSB     : integer := 16;

    constant REG_CONTROL_RELEASE_VERSION_GENERATION_ADDR    : std_logic_vector(5 downto 0) := "00" & x"2";
    constant REG_CONTROL_RELEASE_VERSION_GENERATION_MSB    : integer := 31;
    constant REG_CONTROL_RELEASE_VERSION_GENERATION_LSB     : integer := 24;

    constant REG_CONTROL_SEM_CNT_SEM_CRITICAL_ADDR    : std_logic_vector(5 downto 0) := "00" & x"3";
    constant REG_CONTROL_SEM_CNT_SEM_CRITICAL_MSB    : integer := 15;
    constant REG_CONTROL_SEM_CNT_SEM_CRITICAL_LSB     : integer := 0;

    constant REG_CONTROL_SEM_CNT_SEM_CORRECTION_ADDR    : std_logic_vector(5 downto 0) := "00" & x"4";
    constant REG_CONTROL_SEM_CNT_SEM_CORRECTION_MSB    : integer := 31;
    constant REG_CONTROL_SEM_CNT_SEM_CORRECTION_LSB     : integer := 16;

    constant REG_CONTROL_VFAT_RESET_ADDR    : std_logic_vector(5 downto 0) := "00" & x"5";
    constant REG_CONTROL_VFAT_RESET_MSB    : integer := 11;
    constant REG_CONTROL_VFAT_RESET_LSB     : integer := 0;
    constant REG_CONTROL_VFAT_RESET_DEFAULT : std_logic_vector(11 downto 0) := x"000";

    constant REG_CONTROL_TTC_BX0_CNT_LOCAL_ADDR    : std_logic_vector(5 downto 0) := "00" & x"8";
    constant REG_CONTROL_TTC_BX0_CNT_LOCAL_MSB    : integer := 23;
    constant REG_CONTROL_TTC_BX0_CNT_LOCAL_LSB     : integer := 0;

    constant REG_CONTROL_TTC_BX0_CNT_TTC_ADDR    : std_logic_vector(5 downto 0) := "00" & x"9";
    constant REG_CONTROL_TTC_BX0_CNT_TTC_MSB    : integer := 23;
    constant REG_CONTROL_TTC_BX0_CNT_TTC_LSB     : integer := 0;

    constant REG_CONTROL_TTC_BXN_CNT_LOCAL_ADDR    : std_logic_vector(5 downto 0) := "00" & x"a";
    constant REG_CONTROL_TTC_BXN_CNT_LOCAL_MSB    : integer := 11;
    constant REG_CONTROL_TTC_BXN_CNT_LOCAL_LSB     : integer := 0;

    constant REG_CONTROL_TTC_BXN_SYNC_ERR_ADDR    : std_logic_vector(5 downto 0) := "00" & x"b";
    constant REG_CONTROL_TTC_BXN_SYNC_ERR_BIT    : integer := 12;

    constant REG_CONTROL_TTC_BX0_SYNC_ERR_ADDR    : std_logic_vector(5 downto 0) := "00" & x"c";
    constant REG_CONTROL_TTC_BX0_SYNC_ERR_BIT    : integer := 13;

    constant REG_CONTROL_TTC_BXN_OFFSET_ADDR    : std_logic_vector(5 downto 0) := "00" & x"d";
    constant REG_CONTROL_TTC_BXN_OFFSET_MSB    : integer := 27;
    constant REG_CONTROL_TTC_BXN_OFFSET_LSB     : integer := 16;
    constant REG_CONTROL_TTC_BXN_OFFSET_DEFAULT : std_logic_vector(27 downto 16) := x"000";

    constant REG_CONTROL_TTC_L1A_CNT_ADDR    : std_logic_vector(5 downto 0) := "00" & x"e";
    constant REG_CONTROL_TTC_L1A_CNT_MSB    : integer := 23;
    constant REG_CONTROL_TTC_L1A_CNT_LSB     : integer := 0;

    constant REG_CONTROL_TTC_BXN_SYNC_ERR_CNT_ADDR    : std_logic_vector(5 downto 0) := "00" & x"f";
    constant REG_CONTROL_TTC_BXN_SYNC_ERR_CNT_MSB    : integer := 15;
    constant REG_CONTROL_TTC_BXN_SYNC_ERR_CNT_LSB     : integer := 0;

    constant REG_CONTROL_TTC_BX0_SYNC_ERR_CNT_ADDR    : std_logic_vector(5 downto 0) := "01" & x"0";
    constant REG_CONTROL_TTC_BX0_SYNC_ERR_CNT_MSB    : integer := 31;
    constant REG_CONTROL_TTC_BX0_SYNC_ERR_CNT_LSB     : integer := 16;

    constant REG_CONTROL_SBITS_CLUSTER_RATE_ADDR    : std_logic_vector(5 downto 0) := "01" & x"1";
    constant REG_CONTROL_SBITS_CLUSTER_RATE_MSB    : integer := 31;
    constant REG_CONTROL_SBITS_CLUSTER_RATE_LSB     : integer := 0;

    constant REG_CONTROL_HDMI_SBIT_SEL0_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL0_MSB    : integer := 4;
    constant REG_CONTROL_HDMI_SBIT_SEL0_LSB     : integer := 0;
    constant REG_CONTROL_HDMI_SBIT_SEL0_DEFAULT : std_logic_vector(4 downto 0) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL1_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL1_MSB    : integer := 9;
    constant REG_CONTROL_HDMI_SBIT_SEL1_LSB     : integer := 5;
    constant REG_CONTROL_HDMI_SBIT_SEL1_DEFAULT : std_logic_vector(9 downto 5) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL2_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL2_MSB    : integer := 14;
    constant REG_CONTROL_HDMI_SBIT_SEL2_LSB     : integer := 10;
    constant REG_CONTROL_HDMI_SBIT_SEL2_DEFAULT : std_logic_vector(14 downto 10) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL3_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL3_MSB    : integer := 19;
    constant REG_CONTROL_HDMI_SBIT_SEL3_LSB     : integer := 15;
    constant REG_CONTROL_HDMI_SBIT_SEL3_DEFAULT : std_logic_vector(19 downto 15) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL4_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL4_MSB    : integer := 24;
    constant REG_CONTROL_HDMI_SBIT_SEL4_LSB     : integer := 20;
    constant REG_CONTROL_HDMI_SBIT_SEL4_DEFAULT : std_logic_vector(24 downto 20) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL5_ADDR    : std_logic_vector(5 downto 0) := "01" & x"2";
    constant REG_CONTROL_HDMI_SBIT_SEL5_MSB    : integer := 29;
    constant REG_CONTROL_HDMI_SBIT_SEL5_LSB     : integer := 25;
    constant REG_CONTROL_HDMI_SBIT_SEL5_DEFAULT : std_logic_vector(29 downto 25) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL6_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_SEL6_MSB    : integer := 4;
    constant REG_CONTROL_HDMI_SBIT_SEL6_LSB     : integer := 0;
    constant REG_CONTROL_HDMI_SBIT_SEL6_DEFAULT : std_logic_vector(4 downto 0) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_SEL7_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_SEL7_MSB    : integer := 9;
    constant REG_CONTROL_HDMI_SBIT_SEL7_LSB     : integer := 5;
    constant REG_CONTROL_HDMI_SBIT_SEL7_DEFAULT : std_logic_vector(9 downto 5) := '0' & x"0";

    constant REG_CONTROL_HDMI_SBIT_MODE0_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE0_MSB    : integer := 11;
    constant REG_CONTROL_HDMI_SBIT_MODE0_LSB     : integer := 10;
    constant REG_CONTROL_HDMI_SBIT_MODE0_DEFAULT : std_logic_vector(11 downto 10) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE1_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE1_MSB    : integer := 13;
    constant REG_CONTROL_HDMI_SBIT_MODE1_LSB     : integer := 12;
    constant REG_CONTROL_HDMI_SBIT_MODE1_DEFAULT : std_logic_vector(13 downto 12) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE2_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE2_MSB    : integer := 15;
    constant REG_CONTROL_HDMI_SBIT_MODE2_LSB     : integer := 14;
    constant REG_CONTROL_HDMI_SBIT_MODE2_DEFAULT : std_logic_vector(15 downto 14) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE3_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE3_MSB    : integer := 17;
    constant REG_CONTROL_HDMI_SBIT_MODE3_LSB     : integer := 16;
    constant REG_CONTROL_HDMI_SBIT_MODE3_DEFAULT : std_logic_vector(17 downto 16) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE4_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE4_MSB    : integer := 19;
    constant REG_CONTROL_HDMI_SBIT_MODE4_LSB     : integer := 18;
    constant REG_CONTROL_HDMI_SBIT_MODE4_DEFAULT : std_logic_vector(19 downto 18) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE5_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE5_MSB    : integer := 21;
    constant REG_CONTROL_HDMI_SBIT_MODE5_LSB     : integer := 20;
    constant REG_CONTROL_HDMI_SBIT_MODE5_DEFAULT : std_logic_vector(21 downto 20) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE6_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE6_MSB    : integer := 23;
    constant REG_CONTROL_HDMI_SBIT_MODE6_LSB     : integer := 22;
    constant REG_CONTROL_HDMI_SBIT_MODE6_DEFAULT : std_logic_vector(23 downto 22) := "00";

    constant REG_CONTROL_HDMI_SBIT_MODE7_ADDR    : std_logic_vector(5 downto 0) := "01" & x"3";
    constant REG_CONTROL_HDMI_SBIT_MODE7_MSB    : integer := 25;
    constant REG_CONTROL_HDMI_SBIT_MODE7_LSB     : integer := 24;
    constant REG_CONTROL_HDMI_SBIT_MODE7_DEFAULT : std_logic_vector(25 downto 24) := "00";

    constant REG_CONTROL_CNT_SNAP_PULSE_ADDR    : std_logic_vector(5 downto 0) := "01" & x"4";
    constant REG_CONTROL_CNT_SNAP_PULSE_BIT    : integer := 0;

    constant REG_CONTROL_CNT_SNAP_DISABLE_ADDR    : std_logic_vector(5 downto 0) := "01" & x"5";
    constant REG_CONTROL_CNT_SNAP_DISABLE_BIT    : integer := 1;
    constant REG_CONTROL_CNT_SNAP_DISABLE_DEFAULT : std_logic := '1';

    constant REG_CONTROL_DNA_DNA_LSBS_ADDR    : std_logic_vector(5 downto 0) := "01" & x"7";
    constant REG_CONTROL_DNA_DNA_LSBS_MSB    : integer := 31;
    constant REG_CONTROL_DNA_DNA_LSBS_LSB     : integer := 0;

    constant REG_CONTROL_DNA_DNA_MSBS_ADDR    : std_logic_vector(5 downto 0) := "01" & x"8";
    constant REG_CONTROL_DNA_DNA_MSBS_MSB    : integer := 24;
    constant REG_CONTROL_DNA_DNA_MSBS_LSB     : integer := 0;

    constant REG_CONTROL_UPTIME_ADDR    : std_logic_vector(5 downto 0) := "01" & x"9";
    constant REG_CONTROL_UPTIME_MSB    : integer := 19;
    constant REG_CONTROL_UPTIME_LSB     : integer := 0;

    constant REG_CONTROL_USR_ACCESS_ADDR    : std_logic_vector(5 downto 0) := "10" & x"0";
    constant REG_CONTROL_USR_ACCESS_MSB    : integer := 31;
    constant REG_CONTROL_USR_ACCESS_LSB     : integer := 0;

    constant REG_CONTROL_HOG_GLOBAL_DATE_ADDR    : std_logic_vector(5 downto 0) := "10" & x"1";
    constant REG_CONTROL_HOG_GLOBAL_DATE_MSB    : integer := 31;
    constant REG_CONTROL_HOG_GLOBAL_DATE_LSB     : integer := 0;

    constant REG_CONTROL_HOG_GLOBAL_TIME_ADDR    : std_logic_vector(5 downto 0) := "10" & x"2";
    constant REG_CONTROL_HOG_GLOBAL_TIME_MSB    : integer := 31;
    constant REG_CONTROL_HOG_GLOBAL_TIME_LSB     : integer := 0;

    constant REG_CONTROL_HOG_GLOBAL_VER_ADDR    : std_logic_vector(5 downto 0) := "10" & x"3";
    constant REG_CONTROL_HOG_GLOBAL_VER_MSB    : integer := 31;
    constant REG_CONTROL_HOG_GLOBAL_VER_LSB     : integer := 0;

    constant REG_CONTROL_HOG_GLOBAL_SHA_ADDR    : std_logic_vector(5 downto 0) := "10" & x"4";
    constant REG_CONTROL_HOG_GLOBAL_SHA_MSB    : integer := 31;
    constant REG_CONTROL_HOG_GLOBAL_SHA_LSB     : integer := 0;

    constant REG_CONTROL_HOG_TOP_SHA_ADDR    : std_logic_vector(5 downto 0) := "10" & x"5";
    constant REG_CONTROL_HOG_TOP_SHA_MSB    : integer := 31;
    constant REG_CONTROL_HOG_TOP_SHA_LSB     : integer := 0;

    constant REG_CONTROL_HOG_TOP_VER_ADDR    : std_logic_vector(5 downto 0) := "10" & x"6";
    constant REG_CONTROL_HOG_TOP_VER_MSB    : integer := 31;
    constant REG_CONTROL_HOG_TOP_VER_LSB     : integer := 0;

    constant REG_CONTROL_HOG_HOG_SHA_ADDR    : std_logic_vector(5 downto 0) := "10" & x"7";
    constant REG_CONTROL_HOG_HOG_SHA_MSB    : integer := 31;
    constant REG_CONTROL_HOG_HOG_SHA_LSB     : integer := 0;

    constant REG_CONTROL_HOG_HOG_VER_ADDR    : std_logic_vector(5 downto 0) := "10" & x"8";
    constant REG_CONTROL_HOG_HOG_VER_MSB    : integer := 31;
    constant REG_CONTROL_HOG_HOG_VER_LSB     : integer := 0;

    constant REG_CONTROL_HOG_OH_SHA_ADDR    : std_logic_vector(5 downto 0) := "10" & x"9";
    constant REG_CONTROL_HOG_OH_SHA_MSB    : integer := 31;
    constant REG_CONTROL_HOG_OH_SHA_LSB     : integer := 0;

    constant REG_CONTROL_HOG_OH_VER_ADDR    : std_logic_vector(5 downto 0) := "10" & x"a";
    constant REG_CONTROL_HOG_OH_VER_MSB    : integer := 31;
    constant REG_CONTROL_HOG_OH_VER_LSB     : integer := 0;

    constant REG_CONTROL_HOG_FLAVOUR_ADDR    : std_logic_vector(5 downto 0) := "10" & x"b";
    constant REG_CONTROL_HOG_FLAVOUR_MSB    : integer := 31;
    constant REG_CONTROL_HOG_FLAVOUR_LSB     : integer := 0;


end registers;
