import spidev
import time

# Create SPI object connecting to /dev/spidev0.1
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 10000000  # Set speed to 10 MHz

try:
        # D[19] must be 1
        print("Reading CNFG_GEN Register")
        resp = spi.xfer2([0x21, 0x00, 0x00, 0x00]) # read cnfg_gen register
        print("Writing CNFG_GEN Register")
        resp = spi.xfer2([0x20, 0x08, 0x00, 0x04]) # read cnfg_gen register
        print(hex(resp[0]), hex(resp[1]), hex(resp[2]), hex(resp[3]))

        # using the default fmstr, will write to the cnfg_gen register if that needs to change
        print("Reading ECG_CNFG_REG")
        resp = spi.xfer2([0x2B, 0x00, 0x00, 0x00]) # CNFG ECG addr = 0x15, 1 for rd --> 0x2B
        print(hex(resp[0]), hex(resp[1]), hex(resp[2]), hex(resp[3]))
        # print(hex(resp))
        print("Writing ECG_CNFG_REG")
        resp = spi.xfer2([0x2A, 0x81, 0x50, 0x00])  # CNFG_ECG addr = 0x15, 0 for wr--> 0x2A
                                                    # Rate: 0b10: 128 sps, 0b10 + XX = 0x8
                                                    # Gain: 0b00: 40V/V ->  XX01 for nothing = 0x1
                                                    # X, DHPF, DLPF[1:0] -> DHPF = 1 for 0.5hz hpf, DLPF = 01 = 28.5 Hz = 0x5
        # print(hex(resp))
        print(hex(resp[0]), hex(resp[1]), hex(resp[2]), hex(resp[3]))
        resp = spi.xfer2([0x14, 0x00, 0x00, 0x00]) # Doing a reset, 0x0A + 0 for wr = 0x14
        while True:
                resp = spi.xfer2([0x03, 0x00, 0x00, 0x00]) # STATUS register addr 0x01, + 1 for rd --> 0x03
                # print(bin(resp[1]))
                if((bin(resp[1]))[2] == "1"):
                        print("Reading ECG FIFO")
                        resp = spi.xfer2([0x43, 0x00, 0x00, 0x00]) # ECG_FIFO addr = 0x21, 1 for rd --> 0x43
                        print(hex(resp[0]), hex(resp[1]), hex(resp[2]), hex(resp[3]))
        
        # resp = spi.xfer2([0x3B, 0x00, 0x00, 0x00]) # CNFG_RTOR1 addr = 0x1D, 1 for rd --> 0x3B
        # print(hex(resp))
        # time.sleep(1)
        # resp = spi.xfer2([0x3A, 0x3F, 0xA3, 0x00]) # CNFG_RTOR1 addr = 0x1D, 0 for wr --> 0x3A
        # print(hex(resp))
        # time.sleep(1)
        # resp = spi.xfer2([0x20, 0x08, 0x00, 0x04])
        # print(resp)
        # time.sleep(1)
        
        # resp = spi.xfer2([0x1F, 0x00, 0x00, 0x00])
        # resp = spi.xfer2([0x4B, 0x00, 0x00, 0x00])
        # resp = spi.xfer2([0x03, 0x00, 0x00, 0x00])
        # 00 3F 23 00
        # print(hex(resp))
        # time.sleep(1)

except KeyboardInterrupt:
    spi.close()
