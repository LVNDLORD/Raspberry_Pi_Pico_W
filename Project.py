import micropython
micropython.alloc_emergency_exception_buf(100)


from machine import Pin, I2C, ADC, PWM
from piotimer import Piotimer as Timer
from fifo import Fifo
from led import Led 
from utime import sleep_ms
import ssd1306
import kubios

# Display
adc = ADC(26)
i2c = I2C(1, scl = Pin(15), sda = Pin(14))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


sampling_freq = 250 	#   samples per second
fifo = Fifo(2 * sampling_freq)		# size of the buffer is 2 seconds 500
N = sampling_freq // 25		# for display. Display every Nth sample
window = int(0.150 * sampling_freq)		# window 150ms between peak and moving avg
Rot_Push = Pin(12, Pin.IN, Pin.PULL_UP)
peaks_indexes = []
peak2peak_intervals = []
bpm_list =[]


# reading sensor values
def adc_read(tim):
    x = adc.read_u16()
    if x > 25000 and x < 60000: # filtering out error values read from sensor
        fifo.put(x)


timer = Timer(freq = sampling_freq, callback = adc_read)


# Welcome message
display.fill(0)
display.text('Press the knob', 10, 20)
display.text('to start', 35, 35)
display.text('measuring', 31, 50)
display.show()

# Start
while Rot_Push.value() == 1:
    sleep_ms(100)
display.fill(0)
display.show()


count = 0
run_time_in_sec = 30    # Time for pulse measurement
moving_avg = 32500
a = 4 / sampling_freq	# Weight for adding new data to moving average | 0.016 with 250 sampling_freq
n_threshold = 0
max_peak = 0
x1 = -1
y1 = 32
min_bpm = 30
max_bpm = 180


while count < run_time_in_sec * sampling_freq:  # 30*250=7500
    if not fifo.empty():
        x = fifo.get()
        count += 1
        moving_avg = (1 - a) * moving_avg + a * x # New moving average

        if x > moving_avg + 1000:	# adding some weight to moving avg to avoid false positives
            if x > max_peak:
                max_peak = x
                n_threshold = count		# set n_threshold as max_peak index(count)
        else:
            if (count - n_threshold) > window and n_threshold not in peaks_indexes:
                peaks_indexes.append(n_threshold)
                if len(peaks_indexes) > 2:
                    ppi_in_ms = (peaks_indexes[-1] - peaks_indexes[-2]) * 4 # ppi in ms of two last beats
                    peak2peak_intervals.append(ppi_in_ms) 
                    bpm = 60_000 / ppi_in_ms	# math formula for bpm based on 2 PPI ->  60 / (ppi_in_ms / 1000)
                    if bpm not in bpm_list and min_bpm < bpm < max_bpm:
                        bpm_list.append(bpm)
                        display.fill_rect(0, 51, 128, 64, 0)
                        display.text(f'BPM: {int(bpm)}', 40, 54) # momental bpm based on current PPI
                        display.show()
            max_peak = 0
            
        if count % N  == 0:
            y2 = int(25 * (moving_avg - x) / 10000 + 25) # Scale the value for max haight to be 50 instead of 64
            y2 = max(0, min(50, y2)) # Set the value limit between 0 and 50. Leaving 14px for displaying momental BPM values
            x2 = x1 + 1 # end point of the line segment
            display.line(x2, 0, x2, 50, 0) # clean line pix 0-50px for the pulse
            display.line(x1, y1, x2, y2, 1) # line pix 51-64 for the bpm value to display
            display.show()
            x1 = x2 # Update the starting point (x1, y1) for the next time
            if x1 > 127: # Looping the bpm graph from the left, if reaching the right end side of the screen
                x1 = -1
            y1 = y2


timer.deinit()
fifo.empty()

display.fill(0)
display.text(f"Please wait", 15, 15, 1)
display.text(f"for the data to be", 5, 27, 1)
display.text(f"processed...", 15, 39, 1)
display.show()

print(peak2peak_intervals) # Difference in ms between the peaks_indexes
kubios.calculate_data_in_cloud(peak2peak_intervals, run_time_in_sec)

