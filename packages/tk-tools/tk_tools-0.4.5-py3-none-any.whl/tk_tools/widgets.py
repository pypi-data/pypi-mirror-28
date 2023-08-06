import tkinter as tk


class SmartWidget:
    r"""
    Superclass which contains basic elements of the 'smart' widgets.
    """
    def __init__(self):
        self.var = None

    def add_callback(self, callback: callable):
        r"""
        Add a callback on change

        :param callback: callable function
        :return: None
        """
        def internal_callback(*args):
            callback()

        self.var.trace('w', internal_callback)

    def get(self):
        r"""
        Retrieve the value of the dropdown

        :return: the value of the current variable
        """
        return self.var.get()

    def set(self, value):
        r"""
        Set the value of the dropdown

        :param value: a string representing the
        :return: None
        """
        self.var.set(value)


class SmartOptionMenu(tk.OptionMenu, SmartWidget):
    r"""
    Classic drop down entry with built-in tracing variable.::

        # create the dropdown and grid
        som = SmartOptionMenu(root, ['one', 'two', 'three'])
        som.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
        print(som.get())

        # add the callback function to the dropdown
        som.add_callback(callback)

    :param data: the tk parent frame
    :param options: a list containing the drop down options
    :param initial_value: the initial value of the dropdown
    :param callback: a function
    """
    def __init__(self, parent, options: list, initial_value: str=None,
                 callback: callable=None):
        self.var = tk.StringVar(parent)
        self.var.set(initial_value if initial_value else options[0])

        self.option_menu = tk.OptionMenu.__init__(self, parent, self.var,
                                                  *options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


class SmartSpinBox(tk.Spinbox, SmartWidget):
    r"""
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.::

        # create the smart spinbox and grid
        ssb = SmartSpinBox(root)
        ssb.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(ssb.get())

        # add the callback function to the spinbox
        ssb.add_callback(callback)

    :param parent: the tk parent frame
    :param entry_type: 'str', 'int', 'float'
    :param callback: python callable
    :param options: any options that are valid for tkinter.SpinBox
    """
    def __init__(self, parent, entry_type: str='float',
                 callback: callable=None, **options):
        r"""
        Constructor for SmartSpinBox


        """
        sb_options = options.copy()

        print('sb_options: ', sb_options)

        if entry_type == 'str':
            self.var = tk.StringVar()
        elif entry_type == 'int':
            self.var = tk.IntVar()

        elif entry_type == 'float':
            self.var = tk.DoubleVar()
        else:
            raise ValueError('Entry type must be "str", "int", or "float"')

        sb_options['textvariable'] = self.var
        tk.Spinbox.__init__(parent, **sb_options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


class SmartCheckbutton(tk.Checkbutton, SmartWidget):
    r"""
    Easy-to-use spinbox.  Takes most options that work with a normal SpinBox.
    Attempts to call your callback function - if assigned - whenever there
    is a change to the spinbox.::

        # create the smart spinbox and grid
        scb = SmartCheckbutton(root)
        scb.grid()

        # define a callback function that retrieves
        # the currently selected option
        def callback():
            print(scb.get())

        # add the callback function to the checkbutton
        scb.add_callback(callback)

    :param parent: the tk parent frame
    :param callback: python callable
    :param options: any options that are valid for tkinter.Checkbutton
    """
    def __init__(self, parent, callback: callable=None, **options):
        self.var = tk.BooleanVar()
        tk.Checkbutton.__init__(parent, variable=self.var, **options)

        if callback is not None:
            def internal_callback(*args):
                callback()
            self.var.trace('w', internal_callback)


class ByteLabel(tk.Label):
    # todo: refactor into a BinaryLabel with arbitrary bit width
    r"""
    Displays a byte value binary. Provides methods for
    easy manipulation of bit values.::

        # create the label and grid
        bl = ByteLabel(root, 255)
        bl.grid()

        # toggle highest bit
        bl.toggle_msb()

    :param parent: the tk parent frame
    :param value: the initial value, default is 0
    :param options: prefix string for identifiers
    """
    def __init__(self, parent, value: int=0, prefix: str="", **options):
        super().__init__(parent, **options)

        assert -1 < value < 256

        self._value = value
        self._prefix = prefix
        self._text_update()

    def get(self):
        r"""
        Return the current value

        :return: the current integer value
        """
        return self._value

    def set(self, value: int):
        r"""
        Set the current value

        :param value:
        :return: None
        """
        assert -1 < value < 256

        self._value = value
        self._text_update()

    def _text_update(self):
        self["text"] = self._prefix + str(bin(self._value))[2:].zfill(8)

    def get_bit(self, position: int):
        r"""
        Returns the bit value at position

        :param position: integer between 0 and 7, inclusive
        :return: the value at position as a integer
        """
        assert -1 < position < 8

        return self._value & (1 << position)

    def toggle_bit(self, position: int):
        r"""
        Toggles the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        assert -1 < position < 8

        self._value ^= (1 << position)
        self._text_update()

    def set_bit(self, position: int):
        r"""
        Sets the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        assert -1 < position < 8

        self._value |= (1 << position)
        self._text_update()

    def clear_bit(self, position: int):
        r"""
        Clears the value at position

        :param position: integer between 0 and 7, inclusive
        :return: None
        """
        assert -1 < position < 8

        self._value &= ~(1 << position)
        self._text_update()

    def get_msb(self):
        self.get_bit(7)

    def toggle_msb(self):
        self.toggle_bit(7)

    def get_lsb(self):
        self.get_bit(0)

    def set_msb(self):
        self.set_bit(7)

    def clear_msb(self):
        self.clear_bit(7)

    def toggle_lsb(self):
        self.toggle_bit(0)

    def set_lsb(self):
        self.set_bit(0)

    def clear_lsb(self):
        self.clear_bit(0)
