# encoding: utf-8
import logging_helper


from Tkconstants import NORMAL, DISABLED, HORIZONTAL, E, W, EW, FLAT, SUNKEN
from ttk import Style

from stateutil.incrementor import Incrementor
from uiutil.window.root import RootWindow
from uiutil.frame.frame import BaseFrame
from uiutil.widget.button import Button

logging = logging_helper.setup_logging()


RED_BUTTON = u'red.TButton'
AMBER_BUTTON = u'amber.TButton'
GREEN_BUTTON = u'green.TButton'
NORMAL_BUTTON = u'TButton'


def next_style(style):
    if style is RED_BUTTON:
        return AMBER_BUTTON
    elif style is AMBER_BUTTON:
        return GREEN_BUTTON
    elif style is GREEN_BUTTON:
        return RED_BUTTON
    raise ValueError(u'Unknown style:{style}'.format(style=style))


class TheFrame(BaseFrame):

    BUTTON_WIDTH = 20
    BUTTON_ONE = u'Button One'
    BUTTON_TWO = u'Button Two'

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self,
                           *args,
                           **kwargs)

        self.style.configure(RED_BUTTON, foreground='red')
        self.style.configure(AMBER_BUTTON, relief=SUNKEN, foreground='orange', background='yellow')
        self.style.configure(GREEN_BUTTON, relief=FLAT, foreground='green')

        self.widgets = {}

        self.widgets[self.BUTTON_ONE] = Button(state=NORMAL,
                                               initial_value=self.BUTTON_ONE,
                                               width=self.BUTTON_WIDTH,
                                               command=lambda: self.cycle_style(self.BUTTON_ONE),
                                               column=self.column.next(),
                                               style=GREEN_BUTTON,
                                               sticky=E)

        self.widgets[self.BUTTON_TWO] = Button(state=NORMAL,
                                               initial_value=self.BUTTON_TWO,
                                               width=self.BUTTON_WIDTH,
                                               command=lambda: self.cycle_style(self.BUTTON_TWO),
                                               row=self.row.next(),
                                               style=RED_BUTTON,
                                               sticky=E)
        self.widget_style = {self.BUTTON_ONE: GREEN_BUTTON,
                             self.BUTTON_TWO: RED_BUTTON}

    def cycle_style(self,
                    event=None):
        self.widget_style[event] = next_style(self.widget_style[event])
        self.widgets[event].configure(style=self.widget_style[event])


class StandaloneFrame(RootWindow):

    def __init__(self, *args, **kwargs):
        super(StandaloneFrame, self).__init__(*args, **kwargs)

    def _setup(self):
        __row = Incrementor()
        __column = Incrementor()

        self.title(u"Test Frame")

        TheFrame(parent=self._main_frame,
                 grid_row=__row.next(),
                 grid_column=__column.current)


if __name__ == u'__main__':
    StandaloneFrame(width=650, height=400)
