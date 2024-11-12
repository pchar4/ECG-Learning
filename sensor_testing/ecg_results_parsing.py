import matplotlib.pyplot as plt
import numpy as np
# Specify input and output file names
input_file = '512_chest_blue_right.txt'  # Change to your actual input file name
output_file = 'output.txt'  # Change to your desired output file name
plot_file = 'output.txt'

def hex_to_int(hex_value):
    num = int(hex_value, 16)
    # Convert hex to int
    num >>= 6  # Right shift by 6
    # Check for two's complement (assuming 18 bits)
    if num >= (1 << (18 - 1)):  # If the sign bit is set
        num -= (1 << 18)  # Convert to negative
    return num

def pad_hex(hex_str):
    # Remove '0x' prefix, pad to 2 digits if necessary, and re-add prefix
    return hex_str[2:].zfill(2)

def process_hex_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Strip any whitespace and parentheses, then split the string
            hex_numbers = line.strip("()\n").replace("'", "").split(", ")
            # print(hex_numbers)
            # Pad each hex number
            out_str = "0x"
            for num in hex_numbers:
                # print(num)
                padded_num = pad_hex(num)
                print(padded_num)
                out_str = out_str + padded_num
            # Concatenate padded hex numbers and write to the output file
            outfile.write(out_str + "\n")


# Run the processing function
process_hex_file(input_file, output_file)


def plot_hex_file(plot_file):
    integers = []
    
    with open(plot_file, 'r') as infile:
        for line in infile:
            # Strip whitespace and newlines
            hex_value = line.strip().strip("\n")
            # Convert hex to int
            int_value = hex_to_int(hex_value)

            # Sanity check that the values were "valid" by looking at the e_tag
            reversed_string = ''.join(reversed(bin(int_value)))
            print(reversed_string[3:6])

            integers.append(int_value)
            # print(bin(int_value))

    return integers


def spectrum_plotter(sps, samples):
    dt = 1/sps

    # creating time series
    time_series = []
    for i in range(len(samples)):
        time_series.append(i*dt)
    np_samples = np.array(samples)
    np_time = np.array(time_series)

    # Apply FFT
    N = len(np_samples)
    fft_result = np.fft.fft(np_samples)
    
    # Calculate frequencies
    freqs = np.fft.fftfreq(N, d=dt)
    
    # Calculate the magnitude of the FFT result
    magnitude = np.abs(fft_result)
    
    # Only take the positive frequencies
    pos_mask = freqs > 0
    freqs = freqs[pos_mask]
    magnitude = magnitude[pos_mask]
    return freqs, magnitude

# Process the file and get the integers
int_values = plot_hex_file(plot_file)

# Compute the frequency spectrums
frequencies, magnitudes = spectrum_plotter(512, int_values)

# Create a figure with two subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 10))

# Plotting the integers
axs[0].plot(int_values, marker='.')
axs[0].set_title('Voltage Values ' + input_file)
axs[0].set_xlabel('Index')
axs[0].set_ylabel('Voltage')
axs[0].set_ylim(-1000, 1000)
axs[0].grid()

# Plotting the frequency spectrum
axs[1].plot(frequencies, magnitudes)
axs[1].set_title('Frequency Spectrum')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Magnitude')
axs[1].grid()

int_values_averaged = int_values.copy()
for i in range(1, len(int_values) -1):
    int_values_averaged[i] = (int_values[i-1] + int_values[i] + int_values[i+1]) / 3

# Plotting the integers
axs[2].plot(int_values_averaged, marker='.')
axs[2].set_title('Averaged Values of ECG Readings')
axs[2].set_xlabel('Index')
axs[2].set_ylabel('Voltage')
axs[2].set_ylim(-1000, 1000)
axs[2].grid()

# Adjust layout and show
plt.tight_layout()
plt.show()

# # Process the file and get the integers
# int_values = plot_hex_file(plot_file)

# # Plotting the integers
# plt.plot(int_values, marker='.')
# plt.title('Voltage Values of ECG Readings')
# plt.xlabel('Index')
# plt.ylabel('Voltage')
# plt.ylim(-1000, 1000)
# plt.grid()
# plt.show()

# frequencies, magnitudes = spectrum_plotter(128, int_values)
# plt.plot(frequencies, magnitudes)
# plt.title('Frequency Spectrum')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Magnitude')
# plt.grid()
# plt.show()
