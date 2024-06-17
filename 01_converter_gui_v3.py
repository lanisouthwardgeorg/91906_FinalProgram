from tkinter import *


class Converter:

    def __init__(self):

        # initialise variables (such as feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # common format for all buttons (Arial size 14, bold, white text)
        button_font = ("Arial", "14", "bold")
        button_fg = "#000000"
        # background button colours doesn't work on Mac, see this link:
        # https://stackoverflow.com/questions/72056706/tkinter-button-background-color-is-not-working-in-mac-os
        button_bg_metre = "#990099"
        button_bg_feet = "#009900"
        button_bg_help = "#CC6600"
        button_bg_history = "#004C99"

        # set up GUI frame
        self.altitude_frame = Frame(padx=10, pady=10)
        self.altitude_frame.grid()

        self.altitude_heading = Label(self.altitude_frame,
                                      text="Altitude Convertor",
                                      font=("Arial", "16", "bold"))

        self.altitude_heading.grid(row=0)

        instructions = "Please enter an altitude below and press one of the buttons to convert it from metres to feet."
        self.altitude_instructions = Label(self.altitude_frame,
                                           text=instructions,
                                           wrap=300, width=50,
                                           justify="left")

        self.altitude_instructions.grid(row=1)

        self.altitude_entry = Entry(self.altitude_frame,
                                    font=("Arial", "14"))
        self.altitude_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.output_label = Label(self.altitude_frame,
                                  text="",
                                  fg="#9A1B00")
        self.output_label.grid(row=3)

        # conversion, help and history/export buttons
        self.button_frame = Frame(self.altitude_frame)
        self.button_frame.grid(row=4)

        self.to_metres_button = Button(self.button_frame,
                                       text="To metres",
                                       bg=button_bg_metre,
                                       fg=button_fg,
                                       font=button_font,
                                       width=12,
                                       command=lambda: self.altitude_convert(0)
                                       )
        self.to_metres_button.grid(row=0, column=0, padx=5, pady=5)

        self.to_feet_button = Button(self.button_frame,
                                     text="To feet",
                                     bg=button_bg_feet,
                                     fg=button_fg,
                                     font=button_font,
                                     width=12,
                                     command=lambda: self.altitude_convert(0)
                                     )
        self.to_feet_button.grid(row=0, column=1, padx=5, pady=5)

        self.help_button = Button(self.button_frame,
                                  text="Help/Info",
                                  bg=button_bg_help,
                                  fg=button_fg,
                                  font=button_font,
                                  width=12
                                  )
        self.help_button.grid(row=1, column=0, padx=5, pady=5)

        self.history_button = Button(self.button_frame,
                                     text="History/Export",
                                     bg=button_bg_history,
                                     fg=button_fg,
                                     font=button_font,
                                     width=12,
                                     state=DISABLED
                                     )
        self.history_button.grid(row=1, column=1, padx=5, pady=5)

    # checks for valid input, converts altitude
    def check_altitude(self, min_value):

        has_error = "no"
        error = "Please enter a number that is more than {}".format(min_value)

        response = self.altitude_entry.get()

        # check that user has entered a valid number
        try:
            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # sets var_has_error so that entry box and labels can be correctly formatted by formatting function
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # if no errors
        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")

            # return number to be converted and enable history button
            self.history_button.config(state=NORMAL)
            return response

    @staticmethod
    def round_ans(val):
        var_rounded = (val * 2 + 1) // 2
        return "{:.0f}".format(var_rounded)

    # check altitude is valid and convert it
    def altitude_convert(self, min_val):
        to_convert = self.check_altitude(min_val)

        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        # convert to metres
        elif min_val == 0:
            # do calculation
            answer = to_convert / 3.281
            from_to = "{} f is {} m"

        # convert to feet
        else:
            answer = to_convert * 3.281
            from_to = "{} f is {} m"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            # create user output and add to calculation history
            feedback = from_to.format(to_convert,
                                      answer)
            self.var_feedback.set(feedback)

            self.all_calculations.append(feedback)

            # delete code below when history component is working
            print(self.all_calculations)

        self.output_answer()

    # shows user output and clears entry widget ready for next calculation
    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000")
            self.altitude_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00")
            self.altitude_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Altitude Converter")
    Converter()
    root.mainloop()
