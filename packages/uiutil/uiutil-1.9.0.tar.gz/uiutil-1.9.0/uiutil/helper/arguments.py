ROW = u'row'
COLUMN = u'column'

GRID_KWARGS = (ROW,
               COLUMN,
               u'columnspan',
               u'rowspan',
               u'sticky',
               u'padx',
               u'pady')

START = u'start'
CURRENT = u'current'
NEXT = u'next'


def pop_mandatory_kwarg(kwargs,
                        key):
    try:
        return kwargs.pop(key)
    except KeyError:
        raise ValueError(u'Missing mandatory parameter "{key}"'.format(key=key))


def pop_kwarg(kwargs,
              key,
              default=None):
    try:
        return kwargs.pop(key)
    except KeyError:
        return default


def raise_on_positional_args(caller, args):
    if args:
        raise ValueError(u'positional arguments are not accepted by {c}'.format(c=caller.__class__))


def kwargs_only(f):
    def new_f(**kwargs):
        return f(**kwargs)
    return new_f


def get_grid_kwargs(frame=None,
                    **kwargs):

    grid_kwargs = {key: value
                   for key, value in kwargs.iteritems()
                   if key in GRID_KWARGS}

    default_row = 0 if frame is None else frame.row.current
    default_column = 0 if frame is None else frame.column.current

    # Don't need to set row or column in the original call
    # if it's just the current value
    grid_kwargs[ROW] = grid_kwargs.get(ROW, default_row)

    if grid_kwargs[ROW] == START:
        grid_kwargs[ROW] = frame.row.start()

    elif grid_kwargs[ROW] == NEXT:
        grid_kwargs[ROW] = frame.row.next()

    elif grid_kwargs[ROW] == CURRENT:
        # Don't need to set CURRENT, as it's used by default,
        # but added for those why prefer to use it in their
        # calls.
        grid_kwargs[ROW] = frame.row.current

    grid_kwargs[COLUMN] = grid_kwargs.get(COLUMN, default_column)

    if grid_kwargs[COLUMN] == START:
        grid_kwargs[COLUMN] = frame.column.start()

    elif grid_kwargs[COLUMN] == NEXT:
        grid_kwargs[COLUMN] = frame.column.next()

    elif grid_kwargs[COLUMN] == CURRENT:
        # Don't need to set CURRENT, as it's used by default,
        # but added for those why prefer to use it in their
        # calls.
        grid_kwargs[COLUMN] = frame.column.current

    return grid_kwargs


def get_widget_kwargs(**kwargs):
        return {key: value
                for key, value in kwargs.iteritems()
                if key not in GRID_KWARGS}
