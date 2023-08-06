
import ttk

from ..mixin import AllMixIn


class BaseLabelFrame(ttk.Labelframe,
                     AllMixIn):

    def __init__(self,
                 parent,
                 title=None,
                 grid_row=0,
                 grid_column=0,
                 grid_padx=5,
                 grid_pady=5,
                 grid_columnspan=1,
                 grid_rowspan=1,
                 *args,
                 **kwargs):

        self.parent = parent
        self._grid_row = grid_row
        self._grid_column = grid_column
        self._grid_padx = grid_padx
        self._grid_pady = grid_pady
        self._grid_columnspan = grid_columnspan,
        self._grid_rowspan = grid_rowspan

        # Unfortunately everything Tkinter is written in Old-Style classes so it blows up if you use super!
        ttk.LabelFrame.__init__(self, master=parent, **kwargs)
        AllMixIn.__init__(self, *args, **kwargs)

        if title:
            self._set_title(title=title)

    def exists(self):
        return self.winfo_exists() != 0

    def close(self):
        self.cancel_poll()
        self.close_pool()
