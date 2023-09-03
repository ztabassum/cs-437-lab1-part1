import picar_4wd as fc
import time
import random

slower_speed = 20
faster_speed = 30


ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

def scan_step(ref, ref2):
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    status = fc.get_status_at(current_angle, ref1=ref, ref2=ref2)#ref1

    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            scan_list.reverse()

        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

def main():
    while True:
        scan_list = scan_step(40,20) #make bigger as well
        if not scan_list or len(scan_list) < 10:
            continue
        front = scan_list[2:8] #expand on this
        left = scan_list[:2]
        right = scan_list[8:]
    
        if min(front) != 2: #detected something in front
            if min(left) == 2: # nothing to the left
                fc.turn_left(slower_speed)
            if min(right) == 2:
                fc.turn_right(slower_speed)
        else:
            print(scan_list)
            fc.forward(faster_speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
