from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from time import sleep

from Machine import Machine

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    in other words, the frontend (grr)
    """
    button_called = False

    def __init__(self, machine: Machine, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.machine: Machine = machine
        self.machine.startup()
        print("startup done")

    def on_enter(self, *args):
        print("entered main screen")
        Clock.schedule_interval(self.update, 0.05)

    def on_leave(self, *args):
        print("left main screen")
        Clock.unschedule(self.update)

    def update(self, dt=None):
        pass

    def manual_button(self):
        self.button_called = True
        self.machine.manual_move()
        self.button_called = False

    def start_button(self):
        self.button_called = True
        self.machine.auto_move()
        self.button_called = False
        self.ids.magnet.text = "Hold ball"

    def manual_rotate_button(self):
        self.machine.manual_rotate()

    def magnet_button(self):
        if self.ids.magnet.text == "Hold ball":
            self.ids.magnet.text = "Drop ball"
        else:
            self.ids.magnet.text = "Hold ball"
        self.machine.magnet()

    def manual_rotate_slider(self):
        self.machine.manual_rotate_slider(self.ids.arm_slider.value)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

