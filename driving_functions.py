'''
The driving_functions file provides all the logic for the robot to move.
Inputs are also controlled from this file.
'''

class var():
    duty_turn_left = 0
    duty_turn_false = 1
    duty_turn_right = 0

    div_right = 1
    div_left = 1

    duty_list = [0, 0, 0, 0]
    duty_list_send = [0, 0, 0, 0]

    forward_duty_left = 0
    reverse_duty_left = 0
    forward_duty_right = 0
    reverse_duty_right = 0

    select_robot = 0

    increment = 25

    # 20 is the minimum otherwise the program breaks the robot
    if increment < 20:
        increment = 20
    minimum = 100 - 2*increment
    
def set_orientation_to_seek(action):
    if action == 'v':
        return 315
    elif action == 'b':
        return 0
    elif action == 'n':
        return 45
    elif action == 'g':
        return 270
    elif action == 'h':
        return 90
    elif action == 't':
        return 225
    elif action == 'y':
        return 180
    elif action == 'u':
        return 135

def change_robot(action):
    if action == '1':    
        var.select_robot = 0
    elif action == '2':
        var.select_robot = 1    
    return var.select_robot, 'q'

def stop_reset():

    var.duty_turn_left = 0
    var.duty_turn_false = 1
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.duty_list = [0, 0, 0, 0]
    var.duty_list_send = [0, 0, 0, 0]

    var.forward_duty_left = 0
    var.reverse_duty_left = 0
    var.forward_duty_right = 0
    var.reverse_duty_right = 0

def correcting_action_values(action):

    # robot movement
    if action == 119:  # w
        return 'w'
    elif action == 97:  # a
        return 'a'
    elif action == 115:  # s
        return 's'
    elif action == 100:  # d
        return 'd'
    elif action == 101 or action == 82:  # e or up
        return 'e'
    elif action == 	120 or action == 84:  # x or down
        return 'x'
    elif action == 99 or action == 83:  # c or left
        return 'c'
    elif action == 122 or action == 81:  # z or right
        return 'z'

    # robot reset
    elif action == 113:  # q
        return 'q'

    # robot orientation
    elif action == 116:  # t
        return 't'
    elif action == 121:  # y
        return 'y'
    elif action == 117:  # u
        return 'u'
    elif action == 103:  # g
        return 'g'
    elif action == 104:  # h
        return 'h'
    elif action == 118:  # v
        return 'v'
    elif action == 98:  # b
        return 'b'
    elif action == 110:  # n
        return 'n'

    # robot select
    elif action == 49:  # 1
        return '1'
    elif action == 50:  # 2
        return '2'

    # set straight driving
    elif action == 111:  # o
        return 'o'
    elif action == 112:  # p
        return 'p'
    
    else:
        return -1

def full_speed():
    var.duty_turn_false = 1
    var.duty_turn_left = 0
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.forward_duty_left = 100
    var.reverse_duty_left = 0
    var.forward_duty_right = 100
    var.reverse_duty_right = 0

def full_reverse():
    var.duty_turn_left = 0
    var.duty_turn_false = 1
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.forward_duty_left = 0
    var.reverse_duty_left = 100
    var.forward_duty_right = 0
    var.reverse_duty_right = 100

def quick_left_turn():
    var.duty_turn_left = 0
    var.duty_turn_false = 1
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.forward_duty_left = 0
    var.reverse_duty_left = 100 - var.increment
    var.forward_duty_right = 100 - var.increment
    var.reverse_duty_right = 0

def quick_right_turn():
    var.duty_turn_left = 0
    var.duty_turn_false = 1
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.forward_duty_left = 100 - var.increment
    var.reverse_duty_left = 0
    var.forward_duty_right = 0
    var.reverse_duty_right = 100 - var.increment

def reset():
    var.duty_turn_left = 0
    var.duty_turn_false = 1
    var.duty_turn_right = 0

    var.div_right = 1
    var.div_left = 1

    var.duty_list = [0, 0, 0, 0]
    var.duty_list_send = [0, 0, 0, 0]

    var.forward_duty_left = 0
    var.reverse_duty_left = 0
    var.forward_duty_right = 0
    var.reverse_duty_right = 0

# quick_actions != standing_still_operations
def quick_actions(action):
    if action == 'e':
        full_speed()
    elif action == 'x':
        full_reverse()
    elif action == 'z':
        quick_left_turn()
    elif action == 'c':
        quick_right_turn()
    elif action == 'q':
        reset()

def standing_move_forward():
    var.forward_duty_left = 0
    var.reverse_duty_left = 0
    var.forward_duty_right = 0
    var.reverse_duty_right = 0
    var.forward_duty_left = var.minimum
    var.forward_duty_right = var.minimum

def standing_move_back():
    var.forward_duty_left = 0
    var.reverse_duty_left = 0
    var.forward_duty_right = 0
    var.reverse_duty_right = 0
    var.reverse_duty_left = var.minimum
    var.reverse_duty_right = var.minimum

def standing_turn_left():
    if var.forward_duty_left != 0:
        if var.forward_duty_left == var.minimum:
            var.forward_duty_left = 0
            var.reverse_duty_right = 0
        else:
            var.forward_duty_left -= var.increment
            var.reverse_duty_right -= var.increment
    elif var.forward_duty_right == 0:
        var.forward_duty_right = var.minimum
        var.reverse_duty_left = var.minimum
    elif var.forward_duty_right < 100:
        var.forward_duty_right += var.increment
        var.reverse_duty_left += var.increment

def standing_turn_right():
    if var.forward_duty_right != 0:
        if var.forward_duty_right == var.minimum:
            var.forward_duty_right = 0
            var.reverse_duty_left = 0
        else:
            var.forward_duty_right -= var.increment
            var.reverse_duty_left -= var.increment
    elif var.forward_duty_left == 0:
        var.forward_duty_left = var.minimum
        var.reverse_duty_right = var.minimum
    elif var.forward_duty_left < 100:
        var.forward_duty_left += var.increment
        var.reverse_duty_right += var.increment

def operations_standing_still(action):
    # if standing still
    if (var.duty_list[0] and var.duty_list[2]) == 0 and \
            (var.duty_list[1] and var.duty_list[3]) == 0:
        if action == 'w':
            standing_move_forward()
        elif action == 's':
            standing_move_back()
        elif action == 'a':
            standing_turn_left()
        elif action == 'd':
            standing_turn_right()

def moving_forward_increase_speed():
    if var.forward_duty_left < 100:
        var.forward_duty_left += var.increment
        var.forward_duty_right += var.increment

def moving_forward_decrease_speed():
    if var.forward_duty_left == var.minimum:
        var.forward_duty_left = 0
        var.forward_duty_right = 0
    elif var.forward_duty_left > var.minimum:
        var.forward_duty_left -= var.increment
        var.forward_duty_right -= var.increment

def moving_forward_turn_left():
    if var.duty_turn_left == 1:
        pass
    elif var.duty_turn_false == 1:
        var.duty_turn_false = 0
        var.duty_turn_left = 1
    elif var.duty_turn_right == 1:
        var.duty_turn_right = 0
        var.duty_turn_false = 1
    else:
        pass

def moving_forward_turn_right():
    if var.duty_turn_left == 1:
        var.duty_turn_left = 0
        var.duty_turn_false = 1
    elif var.duty_turn_false == 1:
        var.duty_turn_false = 0
        var.duty_turn_right = 1
    elif var.duty_turn_right == 1:
        pass
    else:
        pass

def operations_moving_forward(action):
    # if moving forward
    if ((var.duty_list[0] and var.duty_list[2]) != 0) and \
            ((var.duty_list[1] and var.duty_list[3]) == 0):

        # increase speed
        if action == 'w':
            moving_forward_increase_speed()      

        # decrease speed
        elif action == 's':
            moving_forward_decrease_speed()

        # turn left
        elif action == 'a':
            moving_forward_turn_left()

        #turn right
        elif action == 'd':
            moving_forward_turn_right()

def moving_backwards_increase_speed():
    if var.reverse_duty_left < 100:
        var.reverse_duty_left += var.increment
        var.reverse_duty_right += var.increment

def moving_backwards_decrease_speed():
    if var.reverse_duty_left == var.minimum:
        var.reverse_duty_left = 0
        var.reverse_duty_right = 0
    elif var.reverse_duty_left > var.minimum:
        var.reverse_duty_left -= var.increment
        var.reverse_duty_right -= var.increment

def moving_backwards_turn_left():
    if var.duty_turn_left == 1:
        pass
    elif var.duty_turn_false == 1:
        var.duty_turn_false = 0
        var.duty_turn_left = 1
    elif var.duty_turn_right == 1:
        var.duty_turn_right = 0
        var.duty_turn_false = 1
    else:
        pass

def moving_backwards_turn_right():
    if var.duty_turn_left == 1:
        var.duty_turn_left = 0
        var.duty_turn_false = 1
    elif var.duty_turn_false == 1:
        var.duty_turn_false = 0
        var.duty_turn_right = 1
    elif var.duty_turn_right == 1:
        pass
    else:
        pass

def operations_moving_backwards(action):
    # if moving backwards
    if ((var.duty_list[0] and var.duty_list[2]) == 0) and \
            ((var.duty_list[1] and var.duty_list[3]) != 0):

        # increase speed 
        if action == 's':
            moving_backwards_increase_speed()
            
        # decrease speed    
        elif action == 'w':
            moving_backwards_decrease_speed()
            
        # turn left
        elif action == 'd':
            moving_backwards_turn_left()
            
        # turn right
        elif action == 'a':
            moving_backwards_turn_right()

def prep_data_for_code_logic():
    var.duty_list[1] = var.reverse_duty_left
    var.duty_list[2] = var.forward_duty_right
    var.duty_list[3] = var.reverse_duty_right
    var.duty_list[0] = var.forward_duty_left

    if var.reverse_duty_left > 100:
        var.reverse_duty_left = 100
    if var.forward_duty_right > 100:
        var.reverse_duty_left = 100
    if var.reverse_duty_right > 100:
        var.reverse_duty_left = 100
    if var.forward_duty_left > 100:
        var.reverse_duty_left = 100

def is_moving_forward():
    # return a one if the car is move forward only
    if (var.duty_list[2] > 0) and (var.duty_list[2] == var.duty_list[0]):
        return 1
    else:
        return 0

def prep_data_for_topic():
    var.duty_list_send[0] = var.forward_duty_left / var.div_left
    var.duty_list_send[1] = var.reverse_duty_left / var.div_left
    var.duty_list_send[2] = var.forward_duty_right / var.div_right
    var.duty_list_send[3] = var.reverse_duty_right / var.div_right

    key = str(int(var.duty_list_send[0])) + ',' \
        + str(int(var.duty_list_send[1])) + ',' \
        + str(int(var.duty_list_send[2])) + ',' \
        + str(int(var.duty_list_send[3]))
    return key

def increase_wheel_speed_to_turn():
    if var.duty_turn_left == 1:
        var.div_left = 1
        var.div_right = 0.6
    elif var.duty_turn_false == 1:
        var.div_left = 1
        var.div_right = 1
    elif var.duty_turn_right == 1:
        var.div_left = 0.6
        var.div_right = 1

def decrease_wheel_speed_to_turn():
    if var.duty_turn_left == 1:
        var.div_left = 2
        var.div_right = 1
    elif var.duty_turn_false == 1:
        var.div_left = 1
        var.div_right = 1
    elif var.duty_turn_right == 1:
        var.div_left = 1
        var.div_right = 2

def set_turn_factor_when_moving():
    if (var.forward_duty_left == var.minimum) or \
            (var.reverse_duty_left == var.minimum):
        increase_wheel_speed_to_turn()
        
    if (var.forward_duty_left > var.minimum) or \
            (var.reverse_duty_left > var.minimum):
        decrease_wheel_speed_to_turn()