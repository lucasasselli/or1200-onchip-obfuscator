#
# Clock / Reset
#
set_location_assignment PIN_B8 -to rst_n_pad_i
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to rst_n_pad_i
set_location_assignment PIN_P11 -to sys_clk_pad_i
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sys_clk_pad_i

#
# UART0: RX <-> GPIO_2[0] (Pin 1, bottom header)
#        TX <-> GPIO_2[1] (Pin 2, bottom header)
#
set_location_assignment PIN_V10 -to uart0_srx_pad_i
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to uart0_srx_pad_i
set_location_assignment PIN_W10 -to uart0_stx_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to uart0_stx_pad_o

# #
# # I2C0: Connected to the EEPROM and Accelerometer
# #
# set_location_assignment PIN_F2 -to i2c0_scl_io
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c0_scl_io
# set_location_assignment PIN_F1 -to i2c0_sda_io
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c0_sda_io

# #
# # Accelerometer specific lines
# #
# set_location_assignment PIN_M2 -to accelerometer_irq_i
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to accelerometer_irq_i
# set_location_assignment PIN_G5 -to accelerometer_cs_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to accelerometer_cs_o

# #
# # I2C1: sda <-> GPIO_2[6] (Pin 11, bottom header)
# #       scl <-> GPIO_2[7] (Pin 12, bottom header)
# #
# set_location_assignment PIN_D15 -to i2c1_sda_io
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c1_sda_io
# set_location_assignment PIN_D14 -to i2c1_scl_io
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to i2c1_scl_io

# #
# # SPI0: Connected to the EPCS
# #
# set_global_assignment -name RESERVE_FLASH_NCE_AFTER_CONFIGURATION "USE AS REGULAR IO"
# set_global_assignment -name RESERVE_DATA0_AFTER_CONFIGURATION "USE AS REGULAR IO"
# set_global_assignment -name RESERVE_DATA1_AFTER_CONFIGURATION "USE AS REGULAR IO"
# set_global_assignment -name RESERVE_DCLK_AFTER_CONFIGURATION "USE AS REGULAR IO"
# set_location_assignment PIN_C1 -to spi0_mosi_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi0_mosi_o
# set_location_assignment PIN_H2 -to spi0_miso_i
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi0_miso_i
# set_location_assignment PIN_H1 -to spi0_sck_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi0_sck_o
# set_location_assignment PIN_D2 -to spi0_ss_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi0_ss_o

# #
# # SPI1: Connected to the AD converter
# #
# set_location_assignment PIN_B10 -to spi1_mosi_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi1_mosi_o
# set_location_assignment PIN_A9 -to spi1_miso_i
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi1_miso_i
# set_location_assignment PIN_B14 -to spi1_sck_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi1_sck_o
# set_location_assignment PIN_A10 -to spi1_ss_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi1_ss_o

# #
# # SPI2: MOSI <-> GPIO_2[2] (Pin  7, bottom header)
# #       MISO <-> GPIO_2[3] (Pin  8, bottom header)
# #       SCK  <-> GPIO_2[4] (Pin  9, bottom header)
# #       SS   <-> GPIO_2[5] (Pin 10, bottom header)
# #
# set_location_assignment PIN_C14 -to spi2_mosi_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi2_mosi_o
# set_location_assignment PIN_C16 -to spi2_miso_i
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi2_miso_i
# set_location_assignment PIN_C15 -to spi2_sck_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi2_sck_o
# set_location_assignment PIN_D16 -to spi2_ss_o
# set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to spi2_ss_o

#
# SDRAM
#
set_location_assignment PIN_U17 -to sdram_a_pad_o[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[0]
set_location_assignment PIN_W19 -to sdram_a_pad_o[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[1]
set_location_assignment PIN_V18 -to sdram_a_pad_o[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[2]
set_location_assignment PIN_U18 -to sdram_a_pad_o[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[3]
set_location_assignment PIN_U19 -to sdram_a_pad_o[4]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[4]
set_location_assignment PIN_T18 -to sdram_a_pad_o[5]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[5]
set_location_assignment PIN_T19 -to sdram_a_pad_o[6]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[6]
set_location_assignment PIN_R18 -to sdram_a_pad_o[7]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[7]
set_location_assignment PIN_P18 -to sdram_a_pad_o[8]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[8]
set_location_assignment PIN_P19 -to sdram_a_pad_o[9]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[9]
set_location_assignment PIN_T20 -to sdram_a_pad_o[10]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[10]
set_location_assignment PIN_P20 -to sdram_a_pad_o[11]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[11]
set_location_assignment PIN_R20 -to sdram_a_pad_o[12]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_a_pad_o[12]

set_location_assignment PIN_Y21 -to sdram_dq_pad_io[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[0]
set_location_assignment PIN_Y20 -to sdram_dq_pad_io[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[1]
set_location_assignment PIN_AA22 -to sdram_dq_pad_io[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[2]
set_location_assignment PIN_AA21 -to sdram_dq_pad_io[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[3]
set_location_assignment PIN_Y22 -to sdram_dq_pad_io[4]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[4]
set_location_assignment PIN_W22 -to sdram_dq_pad_io[5]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[5]
set_location_assignment PIN_W20 -to sdram_dq_pad_io[6]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[6]
set_location_assignment PIN_V21 -to sdram_dq_pad_io[7]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[7]
set_location_assignment PIN_P21 -to sdram_dq_pad_io[8]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[8]
set_location_assignment PIN_J22 -to sdram_dq_pad_io[9]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[9]
set_location_assignment PIN_H21 -to sdram_dq_pad_io[10]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[10]
set_location_assignment PIN_H22 -to sdram_dq_pad_io[11]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[11]
set_location_assignment PIN_G22 -to sdram_dq_pad_io[12]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[12]
set_location_assignment PIN_G20 -to sdram_dq_pad_io[13]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[13]
set_location_assignment PIN_G19 -to sdram_dq_pad_io[14]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[14]
set_location_assignment PIN_F22 -to sdram_dq_pad_io[15]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dq_pad_io[15]

set_location_assignment PIN_V22 -to sdram_dqm_pad_o[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dqm_pad_o[0]
set_location_assignment PIN_J21 -to sdram_dqm_pad_o[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_dqm_pad_o[1]

set_location_assignment PIN_T21 -to sdram_ba_pad_o[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_ba_pad_o[0]
set_location_assignment PIN_T22 -to sdram_ba_pad_o[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_ba_pad_o[1]

set_location_assignment PIN_U21 -to sdram_cas_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_cas_pad_o

set_location_assignment PIN_N22 -to sdram_cke_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_cke_pad_o

set_location_assignment PIN_U20 -to sdram_cs_n_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_cs_n_pad_o

set_location_assignment PIN_U22 -to sdram_ras_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_ras_pad_o

set_location_assignment PIN_V20 -to sdram_we_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_we_pad_o

set_location_assignment PIN_L14 -to sdram_clk_pad_o
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to sdram_clk_pad_o

#
# GPIO0
#
set_location_assignment PIN_A8 -to gpio0_io[0]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[0]
set_location_assignment PIN_A9 -to gpio0_io[1]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[1]
set_location_assignment PIN_A10 -to gpio0_io[2]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[2]
set_location_assignment PIN_B10 -to gpio0_io[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[3]
set_location_assignment PIN_D13 -to gpio0_io[4]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[4]
set_location_assignment PIN_C13 -to gpio0_io[5]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[5]
set_location_assignment PIN_E14 -to gpio0_io[6]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[6]
set_location_assignment PIN_D14 -to gpio0_io[7]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio0_io[7]

#============================================================
# GPIO1 (Switches)
#============================================================
set_location_assignment PIN_C10  -to gpio1_i[0]
set_location_assignment PIN_C11  -to gpio1_i[1]
set_location_assignment PIN_D12  -to gpio1_i[2]
set_location_assignment PIN_C12 -to gpio1_i[3]
set_instance_assignment -name IO_STANDARD "3.3-V LVTTL" -to gpio1_i[*]
