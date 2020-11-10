library IEEE;
use IEEE.STD_LOGIC_1164.all;

-----> !! This package is auto-generated from an address table file using <repo_root>/scripts/generate_registers.py !! <-----
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


    --============================================================================
    --       >>> ADC Module <<<    base address: 0x00001000
    --
    -- Connects to the Virtex-6 XADC and allows for reading of temperature,
    -- VCCINT, and VCCAUX voltages
    --============================================================================

    constant REG_ADC_NUM_REGS : integer := 4;
    constant REG_ADC_ADDRESS_MSB : integer := 3;
    constant REG_ADC_ADDRESS_LSB : integer := 0;
    constant REG_ADC_CTRL_OVERTEMP_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_OVERTEMP_BIT    : integer := 0;

    constant REG_ADC_CTRL_VCCAUX_ALARM_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_VCCAUX_ALARM_BIT    : integer := 1;

    constant REG_ADC_CTRL_VCCINT_ALARM_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_VCCINT_ALARM_BIT    : integer := 2;

    constant REG_ADC_CTRL_ADR_IN_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_ADR_IN_MSB    : integer := 9;
    constant REG_ADC_CTRL_ADR_IN_LSB     : integer := 3;
    constant REG_ADC_CTRL_ADR_IN_DEFAULT : std_logic_vector(9 downto 3) := "000" & x"0";

    constant REG_ADC_CTRL_ENABLE_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_ENABLE_BIT    : integer := 10;
    constant REG_ADC_CTRL_ENABLE_DEFAULT : std_logic := '1';

    constant REG_ADC_CTRL_CNT_OVERTEMP_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_CNT_OVERTEMP_MSB    : integer := 17;
    constant REG_ADC_CTRL_CNT_OVERTEMP_LSB     : integer := 11;

    constant REG_ADC_CTRL_CNT_VCCAUX_ALARM_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_CNT_VCCAUX_ALARM_MSB    : integer := 24;
    constant REG_ADC_CTRL_CNT_VCCAUX_ALARM_LSB     : integer := 18;

    constant REG_ADC_CTRL_CNT_VCCINT_ALARM_ADDR    : std_logic_vector(3 downto 0) := x"0";
    constant REG_ADC_CTRL_CNT_VCCINT_ALARM_MSB    : integer := 31;
    constant REG_ADC_CTRL_CNT_VCCINT_ALARM_LSB     : integer := 25;

    constant REG_ADC_CTRL_DATA_IN_ADDR    : std_logic_vector(3 downto 0) := x"1";
    constant REG_ADC_CTRL_DATA_IN_MSB    : integer := 15;
    constant REG_ADC_CTRL_DATA_IN_LSB     : integer := 0;
    constant REG_ADC_CTRL_DATA_IN_DEFAULT : std_logic_vector(15 downto 0) := x"0000";

    constant REG_ADC_CTRL_DATA_OUT_ADDR    : std_logic_vector(3 downto 0) := x"1";
    constant REG_ADC_CTRL_DATA_OUT_MSB    : integer := 31;
    constant REG_ADC_CTRL_DATA_OUT_LSB     : integer := 16;

    constant REG_ADC_CTRL_RESET_ADDR    : std_logic_vector(3 downto 0) := x"2";
    constant REG_ADC_CTRL_RESET_BIT    : integer := 0;

    constant REG_ADC_CTRL_WR_EN_ADDR    : std_logic_vector(3 downto 0) := x"3";
    constant REG_ADC_CTRL_WR_EN_BIT    : integer := 0;


    --============================================================================
    --       >>> TRIG Module <<<    base address: 0x00002000
    --
    -- Connects to the trigger control module
    --============================================================================

    constant REG_TRIG_NUM_REGS : integer := 73;
    constant REG_TRIG_ADDRESS_MSB : integer := 7;
    constant REG_TRIG_ADDRESS_LSB : integer := 0;
    constant REG_TRIG_CTRL_VFAT_MASK_ADDR    : std_logic_vector(7 downto 0) := x"00";
    constant REG_TRIG_CTRL_VFAT_MASK_MSB    : integer := 11;
    constant REG_TRIG_CTRL_VFAT_MASK_LSB     : integer := 0;
    constant REG_TRIG_CTRL_VFAT_MASK_DEFAULT : std_logic_vector(11 downto 0) := x"000";

    constant REG_TRIG_CTRL_SBIT_DEADTIME_ADDR    : std_logic_vector(7 downto 0) := x"00";
    constant REG_TRIG_CTRL_SBIT_DEADTIME_MSB    : integer := 27;
    constant REG_TRIG_CTRL_SBIT_DEADTIME_LSB     : integer := 24;
    constant REG_TRIG_CTRL_SBIT_DEADTIME_DEFAULT : std_logic_vector(27 downto 24) := x"7";

    constant REG_TRIG_CTRL_ACTIVE_VFATS_ADDR    : std_logic_vector(7 downto 0) := x"01";
    constant REG_TRIG_CTRL_ACTIVE_VFATS_MSB    : integer := 11;
    constant REG_TRIG_CTRL_ACTIVE_VFATS_LSB     : integer := 0;

    constant REG_TRIG_CTRL_CNT_OVERFLOW_ADDR    : std_logic_vector(7 downto 0) := x"02";
    constant REG_TRIG_CTRL_CNT_OVERFLOW_MSB    : integer := 15;
    constant REG_TRIG_CTRL_CNT_OVERFLOW_LSB     : integer := 0;

    constant REG_TRIG_CTRL_ALIGNED_COUNT_TO_READY_ADDR    : std_logic_vector(7 downto 0) := x"02";
    constant REG_TRIG_CTRL_ALIGNED_COUNT_TO_READY_MSB    : integer := 27;
    constant REG_TRIG_CTRL_ALIGNED_COUNT_TO_READY_LSB     : integer := 16;
    constant REG_TRIG_CTRL_ALIGNED_COUNT_TO_READY_DEFAULT : std_logic_vector(27 downto 16) := x"1ff";

    constant REG_TRIG_CTRL_SBIT_SOT_READY_ADDR    : std_logic_vector(7 downto 0) := x"03";
    constant REG_TRIG_CTRL_SBIT_SOT_READY_MSB    : integer := 11;
    constant REG_TRIG_CTRL_SBIT_SOT_READY_LSB     : integer := 0;

    constant REG_TRIG_CTRL_SBIT_SOT_UNSTABLE_ADDR    : std_logic_vector(7 downto 0) := x"04";
    constant REG_TRIG_CTRL_SBIT_SOT_UNSTABLE_MSB    : integer := 11;
    constant REG_TRIG_CTRL_SBIT_SOT_UNSTABLE_LSB     : integer := 0;

    constant REG_TRIG_CTRL_SBITS_MUX_SBIT_MUX_SEL_ADDR    : std_logic_vector(7 downto 0) := x"0e";
    constant REG_TRIG_CTRL_SBITS_MUX_SBIT_MUX_SEL_MSB    : integer := 8;
    constant REG_TRIG_CTRL_SBITS_MUX_SBIT_MUX_SEL_LSB     : integer := 4;
    constant REG_TRIG_CTRL_SBITS_MUX_SBIT_MUX_SEL_DEFAULT : std_logic_vector(8 downto 4) := '1' & x"0";

    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_LSB_ADDR    : std_logic_vector(7 downto 0) := x"0f";
    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_LSB_MSB    : integer := 31;
    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_LSB_LSB     : integer := 0;

    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_MSB_ADDR    : std_logic_vector(7 downto 0) := x"10";
    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_MSB_MSB    : integer := 31;
    constant REG_TRIG_CTRL_SBITS_MUX_SBITS_MUX_MSB_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT0_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"17";
    constant REG_TRIG_CNT_VFAT0_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT0_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT1_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"18";
    constant REG_TRIG_CNT_VFAT1_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT1_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT2_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"19";
    constant REG_TRIG_CNT_VFAT2_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT2_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT3_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1a";
    constant REG_TRIG_CNT_VFAT3_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT3_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT4_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1b";
    constant REG_TRIG_CNT_VFAT4_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT4_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT5_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1c";
    constant REG_TRIG_CNT_VFAT5_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT5_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT6_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1d";
    constant REG_TRIG_CNT_VFAT6_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT6_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT7_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1e";
    constant REG_TRIG_CNT_VFAT7_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT7_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT8_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"1f";
    constant REG_TRIG_CNT_VFAT8_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT8_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT9_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"20";
    constant REG_TRIG_CNT_VFAT9_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT9_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT10_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"21";
    constant REG_TRIG_CNT_VFAT10_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT10_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_VFAT11_SBITS_ADDR    : std_logic_vector(7 downto 0) := x"22";
    constant REG_TRIG_CNT_VFAT11_SBITS_MSB    : integer := 31;
    constant REG_TRIG_CNT_VFAT11_SBITS_LSB     : integer := 0;

    constant REG_TRIG_CNT_RESET_ADDR    : std_logic_vector(7 downto 0) := x"2f";
    constant REG_TRIG_CNT_RESET_BIT    : integer := 0;

    constant REG_TRIG_CNT_SBIT_CNT_PERSIST_ADDR    : std_logic_vector(7 downto 0) := x"30";
    constant REG_TRIG_CNT_SBIT_CNT_PERSIST_BIT    : integer := 0;
    constant REG_TRIG_CNT_SBIT_CNT_PERSIST_DEFAULT : std_logic := '0';

    constant REG_TRIG_CNT_SBIT_CNT_TIME_MAX_ADDR    : std_logic_vector(7 downto 0) := x"31";
    constant REG_TRIG_CNT_SBIT_CNT_TIME_MAX_MSB    : integer := 31;
    constant REG_TRIG_CNT_SBIT_CNT_TIME_MAX_LSB     : integer := 0;
    constant REG_TRIG_CNT_SBIT_CNT_TIME_MAX_DEFAULT : std_logic_vector(31 downto 0) := x"02638e98";

    constant REG_TRIG_CNT_CLUSTER_COUNT_ADDR    : std_logic_vector(7 downto 0) := x"32";
    constant REG_TRIG_CNT_CLUSTER_COUNT_MSB    : integer := 31;
    constant REG_TRIG_CNT_CLUSTER_COUNT_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x0_ADDR    : std_logic_vector(7 downto 0) := x"36";
    constant REG_TRIG_CNT_SBITS_OVER_64x0_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x0_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x1_ADDR    : std_logic_vector(7 downto 0) := x"37";
    constant REG_TRIG_CNT_SBITS_OVER_64x1_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x1_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x2_ADDR    : std_logic_vector(7 downto 0) := x"38";
    constant REG_TRIG_CNT_SBITS_OVER_64x2_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x2_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x3_ADDR    : std_logic_vector(7 downto 0) := x"39";
    constant REG_TRIG_CNT_SBITS_OVER_64x3_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x3_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x4_ADDR    : std_logic_vector(7 downto 0) := x"3a";
    constant REG_TRIG_CNT_SBITS_OVER_64x4_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x4_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x5_ADDR    : std_logic_vector(7 downto 0) := x"3b";
    constant REG_TRIG_CNT_SBITS_OVER_64x5_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x5_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x6_ADDR    : std_logic_vector(7 downto 0) := x"3c";
    constant REG_TRIG_CNT_SBITS_OVER_64x6_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x6_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x7_ADDR    : std_logic_vector(7 downto 0) := x"3d";
    constant REG_TRIG_CNT_SBITS_OVER_64x7_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x7_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x8_ADDR    : std_logic_vector(7 downto 0) := x"3e";
    constant REG_TRIG_CNT_SBITS_OVER_64x8_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x8_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x9_ADDR    : std_logic_vector(7 downto 0) := x"3f";
    constant REG_TRIG_CNT_SBITS_OVER_64x9_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x9_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x10_ADDR    : std_logic_vector(7 downto 0) := x"40";
    constant REG_TRIG_CNT_SBITS_OVER_64x10_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x10_LSB     : integer := 0;

    constant REG_TRIG_CNT_SBITS_OVER_64x11_ADDR    : std_logic_vector(7 downto 0) := x"41";
    constant REG_TRIG_CNT_SBITS_OVER_64x11_MSB    : integer := 15;
    constant REG_TRIG_CNT_SBITS_OVER_64x11_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_RESET_ADDR    : std_logic_vector(7 downto 0) := x"90";
    constant REG_TRIG_SBIT_MONITOR_RESET_MSB    : integer := 31;
    constant REG_TRIG_SBIT_MONITOR_RESET_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER0_ADDR    : std_logic_vector(7 downto 0) := x"91";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER0_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER0_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER1_ADDR    : std_logic_vector(7 downto 0) := x"92";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER1_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER1_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER2_ADDR    : std_logic_vector(7 downto 0) := x"93";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER2_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER2_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER3_ADDR    : std_logic_vector(7 downto 0) := x"94";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER3_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER3_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER4_ADDR    : std_logic_vector(7 downto 0) := x"95";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER4_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER4_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER5_ADDR    : std_logic_vector(7 downto 0) := x"96";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER5_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER5_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER6_ADDR    : std_logic_vector(7 downto 0) := x"97";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER6_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER6_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_CLUSTER7_ADDR    : std_logic_vector(7 downto 0) := x"98";
    constant REG_TRIG_SBIT_MONITOR_CLUSTER7_MSB    : integer := 15;
    constant REG_TRIG_SBIT_MONITOR_CLUSTER7_LSB     : integer := 0;

    constant REG_TRIG_SBIT_MONITOR_L1A_DELAY_ADDR    : std_logic_vector(7 downto 0) := x"a0";
    constant REG_TRIG_SBIT_MONITOR_L1A_DELAY_MSB    : integer := 31;
    constant REG_TRIG_SBIT_MONITOR_L1A_DELAY_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_RESET_ADDR    : std_logic_vector(7 downto 0) := x"b0";
    constant REG_TRIG_SBIT_HITMAP_RESET_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_RESET_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_ACQUIRE_ADDR    : std_logic_vector(7 downto 0) := x"b1";
    constant REG_TRIG_SBIT_HITMAP_ACQUIRE_BIT    : integer := 0;
    constant REG_TRIG_SBIT_HITMAP_ACQUIRE_DEFAULT : std_logic := '0';

    constant REG_TRIG_SBIT_HITMAP_VFAT0_MSB_ADDR    : std_logic_vector(7 downto 0) := x"b2";
    constant REG_TRIG_SBIT_HITMAP_VFAT0_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT0_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT0_LSB_ADDR    : std_logic_vector(7 downto 0) := x"b3";
    constant REG_TRIG_SBIT_HITMAP_VFAT0_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT0_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT1_MSB_ADDR    : std_logic_vector(7 downto 0) := x"b4";
    constant REG_TRIG_SBIT_HITMAP_VFAT1_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT1_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT1_LSB_ADDR    : std_logic_vector(7 downto 0) := x"b5";
    constant REG_TRIG_SBIT_HITMAP_VFAT1_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT1_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT2_MSB_ADDR    : std_logic_vector(7 downto 0) := x"b6";
    constant REG_TRIG_SBIT_HITMAP_VFAT2_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT2_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT2_LSB_ADDR    : std_logic_vector(7 downto 0) := x"b7";
    constant REG_TRIG_SBIT_HITMAP_VFAT2_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT2_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT3_MSB_ADDR    : std_logic_vector(7 downto 0) := x"b8";
    constant REG_TRIG_SBIT_HITMAP_VFAT3_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT3_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT3_LSB_ADDR    : std_logic_vector(7 downto 0) := x"b9";
    constant REG_TRIG_SBIT_HITMAP_VFAT3_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT3_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT4_MSB_ADDR    : std_logic_vector(7 downto 0) := x"ba";
    constant REG_TRIG_SBIT_HITMAP_VFAT4_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT4_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT4_LSB_ADDR    : std_logic_vector(7 downto 0) := x"bb";
    constant REG_TRIG_SBIT_HITMAP_VFAT4_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT4_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT5_MSB_ADDR    : std_logic_vector(7 downto 0) := x"bc";
    constant REG_TRIG_SBIT_HITMAP_VFAT5_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT5_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT5_LSB_ADDR    : std_logic_vector(7 downto 0) := x"bd";
    constant REG_TRIG_SBIT_HITMAP_VFAT5_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT5_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT6_MSB_ADDR    : std_logic_vector(7 downto 0) := x"be";
    constant REG_TRIG_SBIT_HITMAP_VFAT6_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT6_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT6_LSB_ADDR    : std_logic_vector(7 downto 0) := x"bf";
    constant REG_TRIG_SBIT_HITMAP_VFAT6_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT6_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT7_MSB_ADDR    : std_logic_vector(7 downto 0) := x"c0";
    constant REG_TRIG_SBIT_HITMAP_VFAT7_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT7_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT7_LSB_ADDR    : std_logic_vector(7 downto 0) := x"c1";
    constant REG_TRIG_SBIT_HITMAP_VFAT7_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT7_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT8_MSB_ADDR    : std_logic_vector(7 downto 0) := x"c2";
    constant REG_TRIG_SBIT_HITMAP_VFAT8_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT8_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT8_LSB_ADDR    : std_logic_vector(7 downto 0) := x"c3";
    constant REG_TRIG_SBIT_HITMAP_VFAT8_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT8_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT9_MSB_ADDR    : std_logic_vector(7 downto 0) := x"c4";
    constant REG_TRIG_SBIT_HITMAP_VFAT9_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT9_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT9_LSB_ADDR    : std_logic_vector(7 downto 0) := x"c5";
    constant REG_TRIG_SBIT_HITMAP_VFAT9_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT9_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT10_MSB_ADDR    : std_logic_vector(7 downto 0) := x"c6";
    constant REG_TRIG_SBIT_HITMAP_VFAT10_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT10_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT10_LSB_ADDR    : std_logic_vector(7 downto 0) := x"c7";
    constant REG_TRIG_SBIT_HITMAP_VFAT10_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT10_LSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT11_MSB_ADDR    : std_logic_vector(7 downto 0) := x"c8";
    constant REG_TRIG_SBIT_HITMAP_VFAT11_MSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT11_MSB_LSB     : integer := 0;

    constant REG_TRIG_SBIT_HITMAP_VFAT11_LSB_ADDR    : std_logic_vector(7 downto 0) := x"c9";
    constant REG_TRIG_SBIT_HITMAP_VFAT11_LSB_MSB    : integer := 31;
    constant REG_TRIG_SBIT_HITMAP_VFAT11_LSB_LSB     : integer := 0;

    constant REG_TRIG_CTRL_SBIT_SOT_INVALID_BITSKIP_ADDR    : std_logic_vector(7 downto 0) := x"e2";
    constant REG_TRIG_CTRL_SBIT_SOT_INVALID_BITSKIP_MSB    : integer := 11;
    constant REG_TRIG_CTRL_SBIT_SOT_INVALID_BITSKIP_LSB     : integer := 0;


end registers;
