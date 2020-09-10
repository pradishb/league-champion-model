'''Module that contains the the utility functions of gui'''
import datetime
import tkinter

__all__ = ['logger', 'log', 'history']


class Logger:
    '''Base logger class'''

    def __init__(self, pygubu_builder=None, log_format='%H:%M:%S'):
        self.pygubu_builder = pygubu_builder
        self.log_format = log_format
        self.history = []

    def widget_exists(self, name):
        '''Checks if a widget exists'''
        if self.pygubu_builder is None:
            return False
        return name in self.pygubu_builder.objects

    def write(self, message, console='console'):
        '''Writes the message'''
        self.history.append(message)
        if self.pygubu_builder is None:
            print(message, end='')
        else:
            self.pygubu_builder.get_object(console).insert(tkinter.END, message)
            self.pygubu_builder.get_object(console).see('end')

    def log(self, message, console='console'):
        '''Logs a message to the console with time'''
        date_time = datetime.datetime.now().strftime(self.log_format)
        self.write(f'>> {date_time} - {message}\n', console)


logger = Logger()
log = logger.log
history = logger.history
