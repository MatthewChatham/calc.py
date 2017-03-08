# GUI

import tkinter

class GUI(tkinter.Tk):

    # Define constants for regular layout
    PADX = 2
    PADY = 2
    HEIGHT = 2
    WIDTH = 4

    def __init__(self):
        super().__init__()
        self.resizable(0,0)

        self.display = tkinter.Frame(self, height=2*self.HEIGHT, width=5*self.WIDTH + 6*self.PADX)
        self.display.grid(rowspan=2, columnspan=5)

        self.history = tkinter.StringVar()
        self.history.set('')
        self.histButton = tkinter.Label(self.display, height=self.HEIGHT, width=5*self.WIDTH + 4*self.PADY, textvariable=self.history)
        self.current = tkinter.StringVar()
        self.current.set('0')
        self.currentDisp = tkinter.Label(self.display, height=self.HEIGHT, width=5*self.WIDTH + 4*self.PADY, textvariable=self.current)

        self.histButton.grid()
        self.currentDisp.grid()

        self.nums = tkinter.Frame(self, height=4*self.HEIGHT, width=5*self.WIDTH)
        self.nums.grid()

        self.operation_pending = False
        self.last_entry = ''
        self.current_operator = ''
        self.pressed_decimal = False
        self.pressed_equals = False

        # Create number buttons
        row = -1
        for i in range(9):
            if (i % 3) == 0: row += 1
            column = i % 3
            value = (7 - 3 * row) + column
            button = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text=str(value), command=lambda row=row, column=column: self.entry(str((7 - 3 * row) + column)))
            button.grid(row=row, column=column, padx=self.PADX, pady=self.PADY)
        else: button0 = tkinter.Button(self.nums, height=self.HEIGHT, width=int(2.5*self.WIDTH), text=str(0), command=lambda: self.entry('0')).grid(row=3, column=0, columnspan=2)

        
        # Operator buttons
        self.button_div = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text="/", command=lambda: self.operator("/")).grid(row=0, column=3, padx=self.PADX, pady=self.PADY)
        self.button_times = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text="*", command=lambda: self.operator("*")).grid(row=1, column=3, padx=self.PADX, pady=self.PADY)
        self.button_minus = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text="-", command=lambda: self.operator("-")).grid(row=2, column=3, padx=self.PADX, pady=self.PADY)
        self.button_plus = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text='+', command=lambda: self.operator('+')).grid(row=3, column=3, padx=self.PADX, pady=self.PADY)

        # Decimal and clear
        self.button_dec = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text=".", command=lambda: self.decimal()).grid(row=3, column=2, padx=self.PADX, pady=self.PADY)
        self.button_clear = tkinter.Button(self.nums, height=self.HEIGHT, width=self.WIDTH, text="Clear", command=lambda: self.clear()).grid(row=3, column=4, padx=self.PADX, pady=self.PADY)

        self.button_eq = tkinter.Button(self.nums, height=4*self.HEIGHT, width=self.WIDTH, text="=", command=lambda: self.equals()).grid(row=0, column=4, rowspan=3)

    def entry(self, n):
        if self.current.get() == '0' or self.operation_pending or self.pressed_equals:
            self.current.set(n)
            self.operation_pending = False
        else: self.current.set(self.current.get() + n)
        self.operation_pending = False
        self.pressed_equals = False

    def clear(self):
        self.current.set('0')
        self.history.set('')
        self.operation_pending = False
        self.pressed_equals = False

    def decimal(self):
        # Deal with floating-point representation problem
        if not self.pressed_decimal:
            self.current.set(self.current.get() + '.')
        if self.pressed_equals or self.operation_pending: self.current.set('0.')
        self.pressed_decimal = True
        self.pressed_equals = False
        self.operation_pending = False

    def operator(self, op):
        # Compute total when operator pressed
        if self.operation_pending == True:
            self.history.set(self.history.get()[:-2] + op + " ")
        else:
            if self.history.get() == '': self.history.set(self.current.get() + " " + op + " ")
            else: self.history.set(self.history.get() + self.current.get() + " " + op + " ")
        self.current_operator = op
        self.operation_pending = True
        self.pressed_decimal = False
        self.pressed_equals = False

    def equals(self):
        if self.pressed_equals:
            expression = self.current.get() + self.current_operator + self.last_entry
            result = eval(expression)
            
            self.current.set(result)
        else:
            self.last_entry = self.current.get()
            expression = self.history.get() + self.current.get()
            result = eval(expression)
            self.current.set(result)
        self.history.set('')
        self.pressed_decimal = False
        self.pressed_equals = True


