#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <stdint.h>

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_MODE SPI_MODE_0
#define SPI_SPEED 500000  // 500 kHz
#define SPI_BITS_PER_WORD 8

int main() {
    int fd = open(SPI_DEVICE, O_RDWR);
    if (fd < 0) {
        perror("Failed to open SPI device");
        return EXIT_FAILURE;
    }

    // Set SPI mode
    uint8_t mode = SPI_MODE;
    if (ioctl(fd, SPI_IOC_WR_MODE, &mode) == -1) {
        perror("Failed to set SPI mode");
        close(fd);
        return EXIT_FAILURE;
    }

    // Set SPI speed
    if (ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &SPI_SPEED) == -1) {
        perror("Failed to set SPI speed");
        close(fd);
        return EXIT_FAILURE;
    }

    // Set bits per word
    uint8_t bits = SPI_BITS_PER_WORD;
    if (ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits) == -1) {
        perror("Failed to set bits per word");
        close(fd);
        return EXIT_FAILURE;
    }

    // Prepare the 32-bit command to send
    uint32_t tx_command = (0x27 << 1) | 0x01; // Shift 0x27 left by 1 and set the 8th bit
    uint8_t tx_buffer[4] = {
        (tx_command >> 24) & 0xFF, // 1st byte
        (tx_command >> 16) & 0xFF, // 2nd byte
        (tx_command >> 8) & 0xFF,  // 3rd byte
        tx_command & 0xFF           // 4th byte
    };

    uint8_t rx_buffer[4] = {0}; // Buffer for response

    struct spi_ioc_transfer transfer = {
        .tx_buf = (unsigned long)tx_buffer,
        .rx_buf = (unsigned long)rx_buffer,
        .len = sizeof(tx_buffer),
        .speed_hz = SPI_SPEED,
        .bits_per_word = bits,
        .delay_usecs = 0, // Add a delay if needed
        .cs_change = 0,    // Chip select should stay active
    };

    // Send the command
    if (ioctl(fd, SPI_IOC_MESSAGE(1), &transfer) < 1) {
        perror("Failed to send SPI message");
        close(fd);
        return EXIT_FAILURE;
    }

    // Process the response
    printf("Received: ");
    for (int i = 0; i < sizeof(rx_buffer); i++) {
        printf("0x%02x ", rx_buffer[i]);
    }
    printf("\n");

    // Clean up
    close(fd);
    return EXIT_SUCCESS;
}
