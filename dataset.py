import math
from machine import I2C, Pin
import ssd1306

i2c = I2C(1, scl = Pin(15), sda = Pin(14))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

set_1 = [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]
set_2 = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]

# mean PPI, mean HR, SDNN, RMSSD

def mean_PPI(data_list):
    avg_PPI = int(sum(data_list)/ len(data_list))
    print(f'mean PPI = {avg_PPI} ms')
    return avg_PPI


def mean_HR(ppi):
    avg_HR = round(60 / (ppi / 1000))
    print(f'Mean HR = {avg_HR} bpm')
    return avg_HR
    
   
def sdnn(data_list, ppi):
    total_sum_sdnn = 0
    for i in data_list:
        total_sum_sdnn += (i-ppi)**2
    
    SDNN = math.ceil(math.sqrt(total_sum_sdnn / (len(data_list)-1)))
    print(f'sdnn = {SDNN} ms')
    return SDNN


def rmssd(data_list):
    total_sum_rmssd = 0
    for i in range(len(data_list)-1):
        total_sum_rmssd += math.pow(data_list[i+1]-data_list[i], 2)
        
    RMSSD = round(math.sqrt(total_sum_rmssd / (len(data_list)-1)))
    print(f'rmssd = {RMSSD} ms')
    return RMSSD
    

print('Test set 1')
mean_PPI_1 = mean_PPI(set_1)
mean_HR_1 = mean_HR(mean_PPI_1)
SDNN_1 = sdnn(set_1, mean_PPI_1)
RMSSD_1 = rmssd(set_1)
print('\n')

print('Test set 2')
mean_PPI_2 = mean_PPI(set_2)
mean_HR_2 = mean_HR(mean_PPI_2)
SDNN_2 = sdnn(set_2, mean_PPI_2)
RMSSD_2 = rmssd(set_2)


def display_set_1():
    display.fill(0)
    display.text(f'Data Set 1', 30, 0)
    display.text(f'Mean PPI= {mean_PPI_1}ms', 0, 14)
    display.text(f'Mean HR = {mean_HR_1} bpm', 0, 28)
    display.text(f'SDNN    = {SDNN_1} ms', 0, 42)
    display.text(f'RMSSD   = {RMSSD_1} ms', 0, 56)
    display.show()


def display_set_2():
    display.fill(0)
    display.text(f'Data Set 2', 30, 0)
    display.text(f'Mean PPI= {mean_PPI_2} ms', 0, 14)
    display.text(f'Mean HR = {mean_HR_2} bpm', 0, 28)
    display.text(f'SDNN    = {SDNN_2} ms', 0, 42)
    display.text(f'RMSSD   = {RMSSD_2} ms', 0, 56)
    display.show()


# assigning showing data on oled for buttons SW0 and SW2 on add-on board
button_SW0 = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
button_SW2 = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

while True:
    if button_SW0.value() == 1 and button_SW2.value() == 0:
        display_set_1()
    elif button_SW2.value() == 1 and button_SW0.value() == 0:
        display_set_2()




