"""

8 888888888o       ,o888888o.  `8.`8888.      ,8' 8 8888888888   8 888888888o.    8 8888 8 8888888888   b.             8 8 888888888o.
8 8888    `88.  . 8888     `88. `8.`8888.    ,8'  8 8888         8 8888    `88.   8 8888 8 8888         888o.          8 8 8888    `^888.
8 8888     `88 ,8 8888       `8b `8.`8888.  ,8'   8 8888         8 8888     `88   8 8888 8 8888         Y88888o.       8 8 8888        `88.
8 8888     ,88 88 8888        `8b `8.`8888.,8'    8 8888         8 8888     ,88   8 8888 8 8888         .`Y888888o.    8 8 8888         `88
8 8888.   ,88' 88 8888         88  `8.`88888'     8 888888888888 8 8888.   ,88'   8 8888 8 888888888888 8o. `Y888888o. 8 8 8888          88
8 8888888888   88 8888         88  .88.`8888.     8 8888         8 888888888P'    8 8888 8 8888         8`Y8o. `Y88888o8 8 8888          88
8 8888    `88. 88 8888        ,8P .8'`8.`8888.    8 8888         8 8888`8b        8 8888 8 8888         8   `Y8o. `Y8888 8 8888         ,88
8 8888      88 `8 8888       ,8P .8'  `8.`8888.   8 8888         8 8888 `8b.      8 8888 8 8888         8      `Y8o. `Y8 8 8888        ,88'
8 8888    ,88'  ` 8888     ,88' .8'    `8.`8888.  8 8888         8 8888   `8b.    8 8888 8 8888         8         `Y8o.` 8 8888    ,o88P'
8 888888888P       `8888888P'  .8'      `8.`8888. 8 8888         8 8888     `88.  8 8888 8 888888888888 8            `Yo 8 888888888P'

Who's Darkman?
"""

# Todo check timers of isValid()

import sys
import logging as log

from PyQt5 import QtWidgets, QtCore

from .raspberry_pi import Pi
from .gui import Ui_MainWindow


def setup_logging():
    log.basicConfig(
        format="[%(asctime)s] [%(levelname)-8s] :: %(message)s",
        level=log.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout
    )


class Timer(QtCore.QElapsedTimer):
    def __init__(self):
        super().__init__()
        self.restart()

    def secs_elapsed(self):
        return int(self.elapsed() / 1000)


class Game:
    def __init__(self, pi):
        log.info('Game Start')
        self.pi = pi

        self.status_message = 'NO TEAM HAS CONTROL'
        self.controlling_team = None

        self.team_change_in = Timer()
        self.game_end_in = Timer()

        self.red_held = False
        self.blue_held = False
        self.both_held = False

        self.red_score = 0
        self.blue_score = 0

        self.red_display = 0
        self.blue_display = 0

        self.red_current = Timer()
        self.red_current.invalidate()
        self.blue_current = Timer()
        self.blue_current.invalidate()

    def tick(self):
        self.button_check()
        self.update_score()
        return [self.red_display, self.blue_display, self.status_message]

    def change_team(self, team):
        log.info('Change team to {}'.format(team))
        if team == 'red':
            if self.blue_current.isValid() and self.blue_current.secs_elapsed() > 0:
                self.blue_score += self.blue_current.secs_elapsed()
            self.controlling_team = team
            self.status_message = 'FEDERAL COALITION HAS CONTROL'
            self.red_current.restart()
        elif team == 'blue':
            if self.red_current.isValid() and self.red_current.secs_elapsed() > 0:
                self.red_score += self.red_current.secs_elapsed()
            self.controlling_team = team
            self.status_message = 'SOVEREIGN STATES HAS CONTROL'
            self.blue_current.restart()

    def end(self):
        log.info('Game End')
        self.pi.cleanup()
        sys.exit()

    def update_score(self):
        if self.controlling_team == 'red':
            self.red_display = self.red_score + self.red_current.secs_elapsed()
            self.blue_display = self.blue_score
        elif self.controlling_team == 'blue':
            self.blue_display = self.blue_score + self.blue_current.secs_elapsed()
            self.red_display = self.red_score
        else:
            self.red_display, self.blue_display = self.red_score, self.blue_score

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
            timer_value = self.game_end_in.secs_elapsed()
            if timer_value > 4:
                self.end()
        else:
            self.both_held = True
            self.game_end_in.start()

    def red_pressed(self):
        if self.controlling_team == 'red':
            log.info('Red team already has control.')
        else:
            if self.red_held:
                timer_value = self.team_change_in.secs_elapsed()
                if timer_value >= 4:
                    self.change_team('red')
            else:
                self.red_held = True
                self.team_change_in.start()

    def blue_pressed(self):
        if self.controlling_team == 'blue':
            log.info('Blue team already has control.')
        else:
            if self.blue_held:
                timer_value = self.team_change_in.secs_elapsed()
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
        self.pi = Pi()
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
