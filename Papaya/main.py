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

from PyQt5 import QtWidgets, QtCore

from .raspberry_pi import MockPi
from .gui import Ui_MainWindow


def setup_logging():
    log.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] :: %(message)s",
        level=log.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )


class Game:
    def __init__(self, pi):
        log.info('Game Start')
        self.pi = pi

        self.status_message = 'Waiting for first team control.'
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

    def tick(self):
        self.button_check()
        self.update_score()

        if self.both_held:
            self.status_message = str(int(10 - (self.game_end_in.elapsed()/1000)))
        elif self.red_held or self.blue_held:
            self.status_message = str(int(10 - (self.team_change_in.elapsed()/1000)))

        return [self.red_temp_score, self.blue_temp_score, self.status_message]

    def change_team(self, team):
        log.info('Change team to {}'.format(team))
        if team == 'red':
            if self.blue_current_elapsed.isValid() and self.get_seconds(self.blue_current_elapsed) > 0:
                self.blue_score += int(self.blue_current_elapsed.elapsed()/1000)
            self.controlling_team = team
            self.red_current_elapsed.restart()
            self.status_message = 'Red team has control.'
        elif team == 'blue':
            if self.red_current_elapsed.isValid() and self.get_seconds(self.red_current_elapsed) > 0:
                self.red_score += int(self.red_current_elapsed.elapsed()/1000)
            self.controlling_team = team
            self.blue_current_elapsed.restart()
            self.status_message = 'Blue team has control.'

    @staticmethod
    def get_seconds(number):
        if not isinstance(number, QtCore.QElapsedTimer):
            raise TypeError('Must be a type of QElapsedTimer')
        return int(number.elapsed()/1000)

    def end(self):
        log.info('Game End')
        self.pi.cleanup()
        sys.exit()

    def update_score(self):
        if self.controlling_team == 'red':
            self.red_temp_score = self.red_score + self.get_seconds(self.red_current_elapsed)
            self.blue_temp_score = self.blue_score
        elif self.controlling_team == 'blue':
            self.blue_temp_score = self.blue_score + self.get_seconds(self.blue_current_elapsed)
            self.red_temp_score = self.red_score
        else:
            self.red_temp_score, self.blue_temp_score = self.red_score, self.blue_score

    def button_check(self):
        if self.pi.red_pressed() and self.pi.blue_pressed():
            self.both_buttons_pressed()
        elif self.pi.red_pressed():
            self.red_pressed()
        elif self.pi.blue_pressed():
            self.blue_pressed()
        else:
            self.none_pressed()

    # ---- Button Pressed States ---- #

    def both_buttons_pressed(self):
        if self.both_held:
            timer_value = self.game_end_in.elapsed()/1000
            if timer_value > 4:
                self.end()
        else:
            self.both_held = True
            self.game_end_in.start()

    def red_pressed(self):
        if self.controlling_team == 'red':
            self.status_message = 'Red team already has control.'
        else:
            if self.red_held:
                timer_value = self.team_change_in.elapsed()/1000
                if timer_value >= 4:
                    self.change_team('red')
            else:
                self.red_held = True
                self.team_change_in.start()

    def blue_pressed(self):
        if self.controlling_team == 'blue':
            self.status_message = 'Blue team already has control.'
        else:
            if self.blue_held:
                timer_value = self.team_change_in.elapsed()/1000
                if timer_value >= 4:
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


class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.pi = MockPi(self)
        self.game = Game(self.pi)

        self.tick_rate = QtCore.QTimer(self)
        self.tick_rate.setInterval(250)
        self.tick_rate.timeout.connect(self.tick)

        self.tick_rate.start()

        self.setupUi(self)
        self.show()

    def tick(self):
        info = self.game.tick()
        self.display(*info)

    def display(self, red_score, blue_score, status_message):
        self.red_team_score_lcd.display(red_score)
        self.blue_team_score_lcd.display(blue_score)

        self.status_label.setText(status_message)


def main():
    setup_logging()
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()

    sys.exit(app.exec_())
