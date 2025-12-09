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
arm_low_revs = 0.6
arm_high_revs = 0.9

#
# TODO: Replace the placeholders above with your project's actual
# imports. Then, in Machine.__init__, initialize the appropriate
# objects (for example self.dpiComputer and self.dpiStepper) so the rest of
# this class can call into your hardware layer.
# ------------------------------------------------------------------


class Machine:

    piston_high = True

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

        dpiStepper.moveToHomeInSteps(0, 1, 1600,
                                     32000)
        dpiStepper.setCurrentPositionInSteps(stepper_num, 0)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, 3)

    def auto_move(self):
        self.default_position()
        if dpiComputer.readDigitalIn(high_pos):
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_high_revs, True)
            dpiComputer.writeServo(piston_servo, 100) #lower piston slightly
            dpiComputer.writeServo(magnet_servo, 180) #magnet on
            sleep(1)
            dpiComputer.writeServo(piston_servo, 90) #raise piston
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_low_revs, True)
            dpiComputer.writeServo(piston_servo, arm_low)  #lower piston
            sleep(1)
            dpiComputer.writeServo(magnet_servo, 90) #magnet off
            sleep(1)
            dpiComputer.writeServo(piston_servo, 90)  # raise piston

            self.piston_high = False

        elif dpiComputer.readDigitalIn(low_pos):
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_low_revs, True)
            dpiComputer.writeServo(piston_servo, arm_low)  # lower piston
            sleep(0.5)
            dpiComputer.writeServo(magnet_servo, 180)  # magnet on
            sleep(1)
            dpiComputer.writeServo(piston_servo, 90)  # raise piston
            dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, arm_high_revs, True)
            dpiComputer.writeServo(piston_servo, 100)  # slightly lower piston
            dpiComputer.writeServo(magnet_servo, 90)  # magnet off
            sleep(1)
            dpiComputer.writeServo(piston_servo, 90)  # raise piston

            self.piston_high = True

    def manual_move(self):
        if self.piston_high:
            dpiComputer.writeServo(piston_servo, arm_low)
            self.piston_high = False
        else:
            dpiComputer.writeServo(piston_servo, arm_high)
            self.piston_high = True

    def default_position(self):
        dpiComputer.writeServo(piston_servo, 90)
        dpiComputer.writeServo(magnet_servo, 90)
        self.piston_high = True

    def startup(self):
        #TODO: Implement startup functionality
        self.stepper_startup()
        dpiComputer.writeServo(magnet_servo, 90)
        dpiComputer.writeServo(piston_servo, 90)