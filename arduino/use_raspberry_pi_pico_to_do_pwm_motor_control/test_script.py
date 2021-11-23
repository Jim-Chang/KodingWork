from machine import PWM, Pin

# 宣告 pin define
left_fwd = PWM(Pin(6))
left_bwd = PWM(Pin(7))
right_fwd = PWM(Pin(8))
right_bwd = PWM(Pin(9))

# 測試左馬達
left_fwd.duty_u16(65535) # 左馬達會全速正轉
left_fwd.duty_u16(32768) # 左馬達會半速正轉 
left_fwd.duty_u16(0)     # 左馬達會停止
left_bwd.duty_u16(65535) # 左馬達會全速反轉 

# 測試右馬達
right_fwd.duty_u16(65535) # 右馬達會全速正轉
right_fwd.duty_u16(32768) # 右馬達會半速正轉 
right_fwd.duty_u16(0)     # 右馬達會停止
right_bwd.duty_u16(65535) # 右馬達會全速反轉 


# 使用 TwoWayMotor class 來控制
from two_way_motor import TwoWayMotor, FORWARD, BACKWARD

left_motor = TwoWayMotor(6, 7)
right_motor = TwoWayMotor(8, 9)

left_motor.set_speed(30, FORWARD)    # 左馬達正轉 30% 轉速
right_motor.set_speed(85, BACKWARD)  # 右馬達反轉 85% 轉速