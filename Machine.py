# ------------------------------------------------------------------
# Hardware import TEMPLATE - replace these commented examples with
# the actual imports used by your platform / hardware.
#
# Examples:
# - USB/serial-based controllers:
#     import serial
# - If you're using the DPi modules, uncomment or replace below:
#     from dpeaDPi.DPiComputer import DPiComputer
#     from dpeaDPi.DPiStepper import DPiStepper
#
# TODO: Replace the placeholders above with your project's actual
# imports. Then, in Machine.__init__, initialize the appropriate
# objects (for example self.dpiComputer and self.dpiStepper) so the rest of
# this class can call into your hardware layer.
# ------------------------------------------------------------------


class Machine:
    def __init__(self, **kwargs):
        #TODO: Initialize your hardware interfaces here
        pass

    def halt(self):
        #TODO: Implement halt functionality
        pass

    def startup(self):
        #TODO: Implement startup functionality
        pass