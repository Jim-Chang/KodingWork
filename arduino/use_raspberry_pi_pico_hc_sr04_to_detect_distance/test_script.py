from machine import Pin, time_pulse_us
import time

# 宣告 trig 和 echo pin
trig_pin = Pin(0, Pin.OUT)
echo_pin = Pin(1, Pin.IN)

# 對 trig pin 送 10us 長的方波
trig_pin.high()
time.sleep_us(10)
self.trig_pin.low()

# 透過內建函數 time_pulse_us，計算 echo pin 方波持續時間
# 第一個參數給定要測量的 pin
# 第二個參數給定 1 表示計算 high 持續時間
# 第三個參數給定 timeout 時間
echo_t = time_pulse_us(echo_pin, 1, timeout_us=58000)

# 依照官方文件描述
# 如果回傳 -2 表示等 echo pin 拉高超時
# 如果回傳 -1 表示 echo pin 拉高時間太長而超時
if echo_t == -2:
    print('timeout to wait echo to be high.')
elif echo_t == -1:
    print('timeout to measure echo pulse width')
else:
    # 將 echo_t 轉換成距離，這邊單位為 cm
    # 另，除以 29 約等於乘 0.034
    distance = (echo_t / 2.0) / 29
    print('distance is', distance)


# 使用 HCSR04 class 來控制
from hc_sr04 import HCSR04
sensor = HCSR04(0, 1)
distance = sensor.get_distance_in_cm()
print('distance is', distance)