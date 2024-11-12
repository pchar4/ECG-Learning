import spidev
import time

# Create SPI object connecting to /dev/spidev0.1
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 10000000  # Set speed to 12 MHz
i_final = 6000
i_init = 0

# Specify the file name
file_name = '512_chest_blue_left.txt'

# Open the file in write mode ('w'). This will create the file or overwrite it.
with open(file_name, 'w') as file:
        resp = spi.xfer2([0x21, 0x00, 0x00, 0x00]) # read cnfg_gen register
        resp = spi.xfer2([0x20, 0x08, 0x00, 0x04]) # read cnfg_gen register

        # using the default fmstr, will write to the cnfg_gen register if that needs to change
        resp = spi.xfer2([0x2B, 0x00, 0x00, 0x00]) # CNFG ECG addr = 0x15, 1 for rd --> 0x2B
        # resp = spi.xfer2([0x2A, 0x81, 0x50, 0x00])  # CNFG_ECG addr = 0x15, 0 for wr--> 0x2A
                                                    # Rate: 0b10: 128 sps, 0b10 + XX = 0x8
                                                    # Gain: 0b00: 40V/V ->  XX01 for nothing = 0x1
                                                    # X, DHPF, DLPF[1:0] -> DHPF = 1 for 0.5hz hpf, DLPF = 01 = 28.5 Hz = 0x5
        resp = spi.xfer2([0x2A, 0x00, 0x70, 0x00])  # CNFG_ECG addr = 0x15, 0 for wr--> 0x2A
                                                    # Rate: 0b00: 512 sps, 0b00 + XX = 0x0
                                                    # Gain: 0b00: 20V/V ->  0x0
                                                    # X, DHPF, DLPF[1:0] -> DHPF = 1 for 0.5hz hpf, DLPF = 11 = 153.6 Hz = 0x7
        resp = spi.xfer2([0x14, 0x00, 0x00, 0x00]) # FIFO_RST addr = 0x0A, 0 for wr --> 0x14
        while (i_init < i_final):

                # resp = spi.xfer2([0x12, 0x00, 0x00, 0x00]) # SYNCH addr = 0x09, 0 for wr --> 0x12
                resp = spi.xfer2([0x03, 0x00, 0x00, 0x00]) # STATUS register addr 0x01, + 1 for rd --> 0x03
                # print(bin(resp[1]))
                if((bin(resp[1]))[2] == "1"):
                        print("Reading ECG FIFO")
                        resp = spi.xfer2([0x43, 0x00, 0x00, 0x00]) # ECG_FIFO addr = 0x21, 1 for rd --> 0x43
                        print(hex(resp[1]), hex(resp[2]), hex(resp[3]))
                        file.write(f"{hex(resp[1]), hex(resp[2]), hex(resp[3])}\n")
                        i_init += 1;


