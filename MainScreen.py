from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from time import sleep

from Machine import *


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    in other words, the frontend (grr)
    """

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
        print('updating main screen')

    def pressed(self):
        """
        Example button touch event method
        This method is called from main.kv
        :return: None
        """
        print("Button pressed!")

    def start_button(self):
        Machine.auto_move(self.machine)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

