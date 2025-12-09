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
        if self.button_called:
            self.ids.auto_move.disabled = True
            self.ids.manual_move.disabled = True
            self.ids.auto_move.fill_color = "dimgray"
            self.ids.manual_move.fill_color = "dimgray"
        else:
            self.ids.auto_move.disabled = False
            self.ids.manual_move.disabled = False
            self.ids.auto_move.fill_color = "turquoise"
            self.ids.manual_move.fill_color = "turquoise"

    def manual_button(self):
        self.ids.auto_move.disabled = True
        self.ids.manual_move.disabled = True
        self.button_called = True
        self.update()
        sleep(0.05)
        self.machine.manual_move()
        sleep(1)
        self.button_called = False

    def start_button(self):
        self.ids.auto_move.disabled = True
        self.ids.manual_move.disabled = True
        self.button_called = True
        self.update()
        sleep(0.05)
        self.machine.auto_move()
        sleep(1)
        self.button_called = False

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

