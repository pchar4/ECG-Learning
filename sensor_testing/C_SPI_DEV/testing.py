import spidev
import time

# Create SPI object connecting to /dev/spidev0.1
spi = spidev.SpiDev(0, 0)
spi.max_speed_hz = 10000000  # Set speed to 12 MHz

try:
    while True:
        resp = spi.xfer2([0x3B, 0x00, 0x00, 0x00]) # CNFG_RTOR1 addr = 0x1D, 1 for rd --> 0x3B
        print(resp)
        time.sleep(1)
        resp = spi.xfer2([0x3A, 0x3F, 0xA3, 0x00]) # CNFG_RTOR1 addr = 0x1D, 1 for rd --> 0x3B
        print(resp)
        time.sleep(1)
        # resp = spi.xfer2([0x20, 0x08, 0x00, 0x04])
        # print(resp)
        # time.sleep(1)
        
        # resp = spi.xfer2([0x1F, 0x00, 0x00, 0x00])
        resp = spi.xfer2([0x4B, 0x00, 0x00, 0x00])
        # resp = spi.xfer2([0x03, 0x00, 0x00, 0x00])
        # 00 3F 23 00
        print(resp)
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
