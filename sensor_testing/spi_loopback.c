#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>

#define SPI_DEVICE          "/dev/spidev0.0"

unsigned char tx_buffer[4];
unsigned char rx_buffer[4];
uint32_t len_data = 32;
uint32_t spi_speed = 12000000;
int fd;
int ret;
struct spi_ioc_transfer trx;
uint8_t looper;
uint32_t scratch32;

int main(void) {
    trx.tx_buf = (unsigned long)tx_buffer;
    trx.rx_buf = (unsigned long)rx_buffer;
    trx.bits_per_word = 8;
    trx.speed_hz = spi_speed;
    trx.delay_usecs = 0;
    trx.len = 4;

	// unsigned int num = 0b01001011000000000000000000000000; // r to r reg
	//unsigned int num = 0b00011111000000000000000000000000;  // info reg
	unsigned int num = 0b00100001000000000000000000000000;
	// Split the 32-bit number into bytes
    tx_buffer[0] = (num >> 24) & 0xFF; // Extract the highest byte
    tx_buffer[1] = (num >> 16) & 0xFF; // Extract the second byte
    tx_buffer[2] = (num >> 8) & 0xFF;  // Extract the third byte
    tx_buffer[3] = num & 0xFF;         // Extract the lowest byte

	for(looper=0; looper<4; ++looper) {
        rx_buffer[looper] = 0xFF;
    }
    
    fd = open(SPI_DEVICE, O_RDWR);
    if(fd < 0) {
        printf("Could not open the SPI device...\r\n");
        exit(EXIT_FAILURE);
    }

    ret = ioctl(fd, SPI_IOC_RD_MODE32, &scratch32);
    if(ret != 0) {
        printf("Could not read SPI mode...\r\n");
        close(fd);
        exit(EXIT_FAILURE);
    }

    scratch32 |= SPI_MODE_0;

    ret = ioctl(fd, SPI_IOC_WR_MODE32, &scratch32);
    if(ret != 0) {
        printf("Could not write SPI mode...\r\n");
        close(fd);
        exit(EXIT_FAILURE);
    }

    ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &scratch32);
    if(ret != 0) {
        printf("Could not read the SPI max speed...\r\n");
        close(fd);
        exit(EXIT_FAILURE);
    }

    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &scratch32);
    if(ret != 0) {
        printf("Could not write the SPI max speed...\r\n");
        close(fd);
        exit(EXIT_FAILURE);
    }

	printf("SENT ...\r\n");
    for(looper=0; looper<4; ++looper) {
        printf("%02x",tx_buffer[looper]);
    }
    printf("\r\n");
    
    printf("Current SPI buffer...\r\n");
    for(looper=0; looper<4; ++looper) {
        printf("%02x",rx_buffer[looper]);
    }
    printf("\r\n");
     printf("Size of trx: %zu bytes\n", sizeof(tx_buffer));
    ret = ioctl(fd, SPI_IOC_MESSAGE(1), &trx);
    if(ret != 0) {
        printf("SPI transfer returned %d...\r\n", ret);
    }

    printf("Received SPI buffer...\r\n");
    for(looper=0; looper<4; ++looper) {
        printf("%02x",rx_buffer[looper]);
    }
    printf("\r\n");

    close(fd);

    exit(EXIT_SUCCESS);
}
