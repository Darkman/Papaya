"""
__/\\\\\\\\\\\\________________________________________________________________________________________________
 _\/\\\////////\\\________________________________/\\\__________________________________________________________
  _\/\\\______\//\\\______________________________\/\\\__________________________________________________________
   _\/\\\_______\/\\\__/\\\\\\\\\_____/\\/\\\\\\\__\/\\\\\\\\_______/\\\\\__/\\\\\____/\\\\\\\\\_____/\\/\\\\\\___
    _\/\\\_______\/\\\_\////////\\\___\/\\\/////\\\_\/\\\////\\\___/\\\///\\\\\///\\\_\////////\\\___\/\\\////\\\__
     _\/\\\_______\/\\\___/\\\\\\\\\\__\/\\\___\///__\/\\\\\\\\/___\/\\\_\//\\\__\/\\\___/\\\\\\\\\\__\/\\\__\//\\\_
      _\/\\\_______/\\\___/\\\/////\\\__\/\\\_________\/\\\///\\\___\/\\\__\/\\\__\/\\\__/\\\/////\\\__\/\\\___\/\\\_
       _\/\\\\\\\\\\\\/___\//\\\\\\\\/\\_\/\\\_________\/\\\_\///\\\_\/\\\__\/\\\__\/\\\_\//\\\\\\\\/\\_\/\\\___\/\\\_
        _\////////////______\////////\//__\///__________\///____\///__\///___\///___\///___\////////\//__\///____\///__


Who's Boxfriend?
"""

# Todo check timers of isValid()

import sys
import logging as log

# import RPi.GPIO as GPIO
from PyQt5 import QtWidgets, QtCore

from gui import Ui_MainWindow


def setup_logging():
    log.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] :: %(message)s",
        level=log.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )


# class Pi:
#     def __init__(self):
#         # GPIO pin numbers
#         self.red_button = 11
#         self.blue_button = 12
#         self.red_led = 13
#         self.blue_led = 40
#
#         self.gpio_setup()
#
#     def gpio_setup(self):
#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(self.red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(self.blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#         GPIO.setup(self.red_led, GPIO.OUT)
#         GPIO.setup(self.blue_led, GPIO.OUT)
#         GPIO.output(self.red_led, GPIO.HIGH)
#         GPIO.output(self.blue_led, GPIO.HIGH)
#
#     @staticmethod
#     def cleanup():
#         GPIO.cleanup()
#
#     def red_pressed(self):
#         if GPIO.input(self.red_button) == GPIO.HIGH:
#             return True
#         return False
#
#     def blue_pressed(self):
#         if GPIO.input(self.blue_button) == GPIO.HIGH:
#             return True
#         return False


class MockPi:
    def __init__(self):
        # GPIO pin numbers
        self.red_button = 11
        self.blue_button = 12
        self.red_led = 13
        self.blue_led = 40

        self.gpio_setup()

    def gpio_setup(self):
        pass

    @staticmethod
    def cleanup():
        pass

    def red_pressed(self):
        pass

    def blue_pressed(self):
        pass


class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.pi = MockPi()
        self.controlling_team = None
        self.team_change_in = QtCore.QElapsedTimer()
        self.game_end_in = QtCore.QElapsedTimer()

        self.red_held = False
        self.blue_held = False
        self.both_held = False

        self.red_score = 0
        self.blue_score = 0

        self.red_temp_score = 0
        self.blue_temp_score = 0

        self.red_current_elapsed = QtCore.QElapsedTimer()
        self.blue_current_elapsed = QtCore.QElapsedTimer()
        # self.red_current_elapsed.restart()
        # self.blue_current_elapsed.restart()

        self.tick_rate = QtCore.QTimer(self)
        self.tick_rate.setInterval(250)
        self.tick_rate.timeout.connect(self.check_tick)

        self.setupUi(self)
        self.show()

        self.tick_rate.start()

    def display(self):
        self.red_team_score_lcd.display(self.red_temp_score)
        self.blue_team_score_lcd.display(self.blue_temp_score)
        if self.game_end_in != 0:
            self.status_label.setText(str(int(10 - (self.game_end_in.elapsed()/1000))))
        elif self.team_change_in != 0:
            self.status_label.setText(str(int(10 - (self.team_change_in.elapsed()/1000))))
        else:
            self.status_label.setText('{} team has control.'.format(self.controlling_team.capitalize()))

    def change_team(self, team):
        log.debug('Change Team')
        if team == 'red':
            if self.blue_current_elapsed.isValid() and self.get_seconds(self.blue_current_elapsed) > 0:
                self.blue_score += int(self.blue_current_elapsed.elapsed()/1000)
            self.controlling_team = team
            self.red_current_elapsed.restart()
            self.status_label.setText('Red team has control.')
        elif team == 'blue':
            if self.red_current_elapsed.isValid() and self.get_seconds(self.red_current_elapsed) > 0:
                self.red_score += int(self.red_current_elapsed.elapsed()/1000)
            self.controlling_team = team
            self.blue_current_elapsed.restart()
            self.status_label.setText('Blue team has control.')

    @staticmethod
    def get_seconds(number):
        if not isinstance(number, QtCore.QElapsedTimer):
            raise TypeError('Must be a type of QElapsedTimer')
        return int(number.elapsed()/1000)

    def end(self):
        log.debug('End Game')
        self.pi.cleanup()
        sys.exit()

    def update_score(self):
        log.debug('Red Elapsed: {},  Blue Elapsed: {}'.format(self.get_seconds(self.red_current_elapsed), self.get_seconds(self.blue_current_elapsed)))
        if self.controlling_team == 'red':
            self.red_temp_score = self.red_score + self.get_seconds(self.red_current_elapsed)
            self.blue_temp_score = self.blue_score
        elif self.controlling_team == 'blue':
            self.blue_temp_score = self.blue_score + self.get_seconds(self.blue_current_elapsed)
            self.red_temp_score = self.red_score
        else:
            self.red_temp_score, self.blue_temp_score = self.red_score, self.blue_score
        self.display()

    def check_tick(self):
        if self.red_checkbox.isChecked() and self.blue_checkbox.isChecked():
            self.both_buttons_pressed()
        elif self.red_checkbox.isChecked():
            self.red_pressed()
        elif self.blue_checkbox.isChecked():
            self.blue_pressed()
        else:
            self.none_pressed()
        self.update_score()

    # def tick(self):
    #     if self.pi.red_pressed() and self.pi.blue_pressed():
    #         self.both_buttons_pressed()
    #     elif self.pi.red_pressed():
    #         self.red_pressed()
    #     elif self.pi.blue_pressed():
    #         self.blue_pressed()
    #     else:
    #         self.none_pressed()
    #     self.update_score()

    # ---- Button Pressed States ---- #

    def both_buttons_pressed(self):
        if self.both_held:
            timer_value = self.game_end_in.elapsed()/1000
            if timer_value > 10:
                self.end()
        else:
            self.both_held = True
            self.game_end_in.start()

    def red_pressed(self):
        if self.controlling_team == 'red':
            self.status_label.setText('Red team already has control.')
        else:
            if self.red_held:
                timer_value = self.team_change_in.elapsed()/1000
                if timer_value >= 10:
                    self.change_team('red')
            else:
                self.red_held = True
                self.team_change_in.start()

    def blue_pressed(self):
        if self.controlling_team == 'blue':
            self.status_label.setText('Blue team already has control.')
        else:
            if self.blue_held:
                timer_value = self.team_change_in.elapsed()/1000
                if timer_value >= 10:
                    self.change_team('blue')
            else:
                self.blue_held = True
                self.team_change_in.start()

    def none_pressed(self):
        self.red_held = False
        self.blue_held = False
        self.both_held = False
        self.game_end_in.invalidate()
        self.team_change_in.invalidate()


def main():
    setup_logging()
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
