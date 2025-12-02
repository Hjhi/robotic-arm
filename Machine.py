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

dpiComputer = DPiComputer()
dpiStepper = DPiStepper()

#labelling sensors to make life easier
low_pos = dpiComputer.IN_CONNECTOR__IN_0
high_pos = dpiComputer.IN_CONNECTOR__IN_1

#for servos, 90 is off, 180 is on
magnet_servo = 0
piston_servo = 1

#
# TODO: Replace the placeholders above with your project's actual
# imports. Then, in Machine.__init__, initialize the appropriate
# objects (for example self.dpiComputer and self.dpiStepper) so the rest of
# this class can call into your hardware layer.
# ------------------------------------------------------------------


class Machine:
    def __init__(self, **kwargs):
        #TODO: Initialize your hardware interfaces here
        dpiStepper.setBoardNumber(0)

    def halt(self):
        #TODO: Implement halt functionality
        dpiStepper.enableMotors(False)
        dpiComputer.writeServo(1, 0)
        dpiComputer.writeServo(0, 90)
        dpiStepper.moveToAbsolutePositionInRevolutions(0, 0, True)

    def stepper_startup(self):
        dpiStepper.enableMotors(True)
        microstepping = 8
        dpiStepper.setMicrostepping(microstepping)
        speed_steps_per_second = 400 * microstepping
        accel_steps_per_second_per_second = speed_steps_per_second
        dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
        stepperStatus = dpiStepper.getStepperStatus(0)
        print(f"Pos = {stepperStatus}")

        dpiStepper.moveToHomeInSteps(0, 1, 1600,
                                     32000)
        dpiStepper.setCurrentPositionInSteps(0, 0)
        dpiStepper.setSpeedInRevolutionsPerSecond(0, 3)

    def auto_move(self):
        if dpiComputer.readDigitalIn(low_pos):
            pass
        elif dpiComputer.readDigitalIn(high_pos):
            pass

    def manual_move(self):



    def startup(self):
        #TODO: Implement startup functionality
        self.stepper_startup()
        dpiComputer.writeServo(1, 0)
        dpiComputer.writeServo(0, 90)