import RPi.GPIO as GPIO


class Pi:
    def __init__(self):
        # GPIO pin numbers
        self.red_button = 11
        self.blue_button = 12
        self.red_led = 13
        self.blue_led = 40

        self.gpio_setup()

    def gpio_setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.red_led, GPIO.OUT)
        GPIO.setup(self.blue_led, GPIO.OUT)
        GPIO.output(self.red_led, GPIO.HIGH)
        GPIO.output(self.blue_led, GPIO.HIGH)

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    def red_pressed(self):
        if GPIO.input(self.red_button) == GPIO.HIGH:
            return True
        return False

    def blue_pressed(self):
        if GPIO.input(self.blue_button) == GPIO.HIGH:
            return True
        return False


# class MockPi:
#     def __init__(self, gui):
#         self.gui = gui
#
#     @staticmethod
#     def cleanup():
#         pass
#
#     def red_pressed(self):
#         return self.gui.red_checkbox.isChecked()
#
#     def blue_pressed(self):
#         return self.gui.blue_checkbox.isChecked()
