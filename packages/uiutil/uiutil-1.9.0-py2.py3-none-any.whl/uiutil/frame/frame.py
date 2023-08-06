
import ttk

from ..mixin import AllMixIn
from ..helper.arguments import get_widget_kwargs, get_grid_kwargs


class BaseFrame(ttk.Frame,
                AllMixIn):

    def __init__(self,
                 parent,
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
        self._grid_columnspan = grid_columnspan
        self._grid_rowspan = grid_rowspan

        # Keep a list of frames added
        self._frames = []

        # Unfortunately everything Tkinter is written in Old-Style classes so it blows up if you use super!
        ttk.Frame.__init__(self, master=parent, **kwargs)
        AllMixIn.__init__(self, *args, **kwargs)

    def exists(self):
        return self.winfo_exists() != 0

    def close(self):
        self.cancel_poll()
        self.close_pool()

        for frame in self._frames:
            frame.close()

    def add_frame(self,
                  frame,
                  **kwargs):

        frame_kwargs = get_widget_kwargs(**kwargs)

        grid_kwargs = get_grid_kwargs(**kwargs)

        frame_object = frame(**frame_kwargs)
        frame_object.grid(**grid_kwargs)

        self._frames.append(frame_object)

        return frame_object
