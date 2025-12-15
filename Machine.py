# ------------------------------------------------------------------
# Hardware import TEMPLATE - replace these commented examples with
# the actual imports used by your platform / hardware.
#
# Examples:
# - USB/serial-based controllers:
#     import serial
# - If you're using the DPi modules, uncomment or replace below:
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep
from kivy.clock import Clock
from functools import partial

dpiComputer = DPiComputer()
dpiStepper = DPiStepper()

#labelling things to make life easier
low_pos = dpiComputer.IN_CONNECTOR__IN_0
high_pos = dpiComputer.IN_CONNECTOR__IN_1
stepper_num = 0

#for servos, 90 is off, 180 is on
magnet_servo = 1
piston_servo = 0
arm_high = 90
arm_low = 170
arm_low_revs = 0.85
arm_high_revs = 0.5

#
# TODO: Replace the placeholders above with your project's actual
# imports. Then, in Machine.__init__, initialize the appropriate
# objects (for example self.dpiComputer and self.dpiStepper) so the rest of
# this class can call into your hardware layer.
# ------------------------------------------------------------------


class Machine:

    piston_high = True
    magnet_on = False

    def __init__(self, **kwargs):
        #TODO: Initialize your hardware interfaces here
        dpiStepper.setBoardNumber(0)

    def halt(self):
        #TODO: Implement halt functionality
        dpiStepper.enableMotors(False)
        dpiComputer.writeServo(piston_servo, 90)
        dpiComputer.writeServo(magnet_servo, 90)
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 0, True)

    def stepper_startup(self):
        dpiStepper.enableMotors(True)
        microstepping = 8
        dpiStepper.setMicrostepping(microstepping)
        speed_steps_per_second = 400 * microstepping
        accel_steps_per_second_per_second = speed_steps_per_second
        dpiStepper.setSpeedInStepsPerSecond(stepper_num, speed_steps_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(stepper_num, accel_steps_per_second_per_second)
        stepperStatus = dpiStepper.getStepperStatus(stepper_num)
        print(f"Pos = {stepperStatus}")

        dpiStepper.moveToHomeInSteps(0, 1, 1600, 32000)
        dpiStepper.setCurrentPositionInSteps(stepper_num, 0)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, 3)

    def auto_move(self, dt=None):
        self.default_position()
        if not dpiComputer.readDigitalIn(high_pos):
            # dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_high_revs, True)
            # dpiComputer.writeServo(piston_servo, arm_low) #lower piston
            # dpiComputer.writeServo(magnet_servo, 180) #magnet on
            # sleep(1)
            # dpiComputer.writeServo(piston_servo, 90) #raise piston
            # dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_low_revs, True)
            # dpiComputer.writeServo(piston_servo, arm_low)  #lower piston
            # sleep(2.5)
            # dpiComputer.writeServo(magnet_servo, 90) #magnet off
            # dpiComputer.writeServo(piston_servo, 90)  # raise piston
            Clock.schedule_once(partial(self.move_and_grab,True, True),0)
            Clock.schedule_once(partial(self.move, arm_low_revs), 5)
            Clock.schedule_once(partial(self.move_and_grab,False, False), 8)


        elif not dpiComputer.readDigitalIn(low_pos):
            # print("I acknowledge the existence of your ball at the low end, I simply do not want to move")
            # dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_low_revs, True)
            # dpiComputer.writeServo(piston_servo, arm_low)  # lower piston
            # sleep(2.5)
            # dpiComputer.writeServo(magnet_servo, 180)  # magnet on
            # dpiComputer.writeServo(piston_servo, 90)  # raise piston
            # dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_high_revs, True)
            # dpiComputer.writeServo(piston_servo, arm_low)  #  lower piston
            # sleep(1)
            # dpiComputer.writeServo(magnet_servo, 90)  # magnet off
            # dpiComputer.writeServo(piston_servo, 90)  # raise piston
            Clock.schedule_once(partial(self.move_and_grab,True, False),0)
            Clock.schedule_once(partial(self.move, arm_high_revs), 7)
            Clock.schedule_once(partial(self.move_and_grab,False, True), 10)

        else:
            print("your sensor is not working (yum)")


    def move_and_grab(self, grab, high, dt=None):
        if grab:
            magnet_num = 180
        else:
            magnet_num = 90

        if high:
            arm_angle = arm_high_revs
            delay = 3
        else:
            arm_angle = arm_low_revs
            delay = 1

        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_angle, True)
        dpiComputer.writeServo(piston_servo, arm_low)  # lower piston
        Clock.schedule_once(partial(self.grab, magnet_num, delay), delay)

    def grab(self, magnet_num, delay, dt=None):
        dpiComputer.writeServo(magnet_servo, magnet_num)  # magnet on
        Clock.schedule_once(self.arm_raise, delay)

    def move(self, pos, dt=None):
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, pos, True)

    def arm_raise(self, dt=None):
        dpiComputer.writeServo(piston_servo, 90)  # raise piston

    def manual_move(self):
        if self.piston_high:
            dpiComputer.writeServo(piston_servo, arm_low)
            self.piston_high = False
        else:
            dpiComputer.writeServo(piston_servo, arm_high)
            self.piston_high = True
        return True

    def manual_rotate(self):
        if dpiStepper.getCurrentPositionInRevolutions(stepper_num)[1] > 0.7:
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_high_revs, True)
        else:
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_low_revs, True)
        return True

    def magnet(self):
        if self.magnet_on:
            dpiComputer.writeServo(magnet_servo, 90)  # magnet off
            self.magnet_on = False
        else:
            dpiComputer.writeServo(magnet_servo, 180) #magnet on
            self.magnet_on = True
        return True

    def manual_rotate_slider(self, slider_value):
        arm_pos = arm_low_revs - (arm_low_revs-arm_high_revs)*slider_value/100
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_pos, True)
        return True

    def default_position(self):
        dpiComputer.writeServo(piston_servo, 90)
        dpiComputer.writeServo(magnet_servo, 90)
        self.piston_high = True
        self.magnet_on = False

    def startup(self):
        self.stepper_startup()
        dpiComputer.writeServo(magnet_servo, 90)
        dpiComputer.writeServo(piston_servo, 90)