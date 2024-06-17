from tkinter import *
from functools import partial  # to prevent unwanted windows
from datetime import date
import re


class Converter:

    def __init__(self):

        # initialise variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

        # common format for all buttons (Arial size 14, bold)
        button_font = ("Arial", "14", "bold")

        # background button colours doesn't work on Mac, see this link:
        # https://stackoverflow.com/questions/72056706/tkinter-button-background-color-is-not-working-in-mac-os
        button_bg_metre = "#0064C9"
        button_bg_feet = "#007FFF"
        button_bg_help = "#FF9933"
        button_bg_history = "#AD0000"

        # set up GUI frame
        self.altitude_frame = Frame(padx=10, pady=10)
        self.altitude_frame.grid()

        self.altitude_heading = Label(self.altitude_frame,
                                      text="Altitude Convertor",
                                      font=("Arial", "16", "bold"))

        self.altitude_heading.grid(row=0)

        instructions = "Please enter an altitude below and press one of the buttons to convert it."
        self.altitude_instructions = Label(self.altitude_frame,
                                           text=instructions,
                                           wrap=300, width=50,
                                           justify="left")

        self.altitude_instructions.grid(row=1)

        self.altitude_entry = Entry(self.altitude_frame,
                                    font=("Arial", "14"))
        self.altitude_entry.grid(row=2, padx=10, pady=10)

        self.output_label = Label(self.altitude_frame,
                                  text="",
                                  fg="#9A1B00")
        self.output_label.grid(row=3)

        # conversion, help and history/export buttons in another frame
        self.button_frame = Frame(self.altitude_frame)
        self.button_frame.grid(row=4)

        self.to_metres_button = Button(self.button_frame,
                                       text="To metres",
                                       bg=button_bg_metre,
                                       fg="#FFFFFF",
                                       font=button_font,
                                       width=12,
                                       command=lambda: self.altitude_convert("to_metres")
                                       )
        self.to_metres_button.grid(row=0, column=0, padx=5, pady=5)

        self.to_feet_button = Button(self.button_frame,
                                     text="To feet",
                                     bg=button_bg_feet,
                                     fg="#000000",
                                     font=button_font,
                                     width=12,
                                     command=lambda: self.altitude_convert("to_feet")
                                     )
        self.to_feet_button.grid(row=0, column=1, padx=5, pady=5)

        self.help_button = Button(self.button_frame,
                                  text="Help/Info",
                                  bg=button_bg_help,
                                  fg="#000000",
                                  font=button_font,
                                  width=12,
                                  command=self.to_help
                                  )
        self.help_button.grid(row=1, column=0, padx=5, pady=5)

        self.history_button = Button(self.button_frame,
                                     text="History/Export",
                                     bg=button_bg_history,
                                     fg="#FFFFFF",
                                     font=button_font,
                                     width=12,
                                     state=DISABLED,
                                     command=lambda: self.to_history(self.all_calculations)
                                     )
        self.history_button.grid(row=1, column=1, padx=5, pady=5)

    # checks for valid input, converts altitude
    def check_altitude(self):

        has_error = "no"
        error = "Please enter a number."

        response = self.altitude_entry.get()

        # check that user has entered a valid number
        try:
            response = float(response)
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

    # round answer function
    @staticmethod
    def round_ans(val):
        var_rounded = (val * 2 + 1) // 2
        return "{:.0f}".format(var_rounded)

    # check altitude is valid and convert it
    def altitude_convert(self, conversion_type):
        to_convert = self.check_altitude()

        if to_convert == "invalid":
            self.output_answer()
            return

        # convert to metres
        if conversion_type == "to_metres":
            # do calculation
            answer = to_convert / 3.281
            from_to = "{} feet is {} metres"

        # convert to feet
        else:
            answer = to_convert * 3.281
            from_to = "{} metres is {} feet"

        to_convert_rounded = self.round_ans(to_convert)
        answer_rounded = self.round_ans(answer)

        # create user output and add to calculation history
        feedback = from_to.format(to_convert_rounded,
                                  answer_rounded)
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

    # opens history / export dialogue
    def to_history(self, all_calculations):
        HistoryExport(self, all_calculations)

    # opens help / info dialogue box
    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):

        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # if users press cross at top, closes help window and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box,
                                width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold")
                                        )
        self.help_heading_label.grid(row=0)

        help_text = ("To use the program, simply enter the altitude you wish to convert and then choose to convert "
                     "either to metres or to feet. \n"
                     "Note that you must enter only numbers otherwise you will get an error message. \n"
                     "To see your calculation history and export it to a text file, "
                     "please click the 'History / Export' button")
        self.help_text_label = Label(self.help_frame,
                                     bg=background,
                                     text=help_text,
                                     wrap=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        # dismiss button
        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss",
                                     bg="#CC6600",
                                     fg="#000000",
                                     command=partial(self.close_help,
                                                     partner)
                                     )
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # set help button back to normal
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:

    def __init__(self, partner, calc_list):

        # set max number of calculations to 5
        max_calc = 5
        self.var_max_calc = IntVar()
        self.var_max_calc.set(max_calc)

        # set filename variable and date variable for when writing to file
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        # function converts contents of calculation list into string
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background colour
        self.history_box = Toplevel()

        # disable history button
        partner.history_button.config(state=DISABLED)

        # if users press cross at top, closes history window and 'releases' history button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box,
                                   width=300,
                                   height=200
                                   )
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame,
                                           text="History/Export",
                                           font=("Arial", "16", "bold")
                                           )
        self.history_heading_label.grid(row=0)

        # customise text and background colour for calculation area
        # depending on whether all or only some calculations are shown
        num_calc = len(calc_list)

        if num_calc > max_calc:
            calc_background = "#FFE6CC"     # peach
            showing_all = ("Here are your recent calculations ({}/{} calculations are shown). "
                           "Please export your calculations to see your full calculation "
                           "history".format(max_calc, num_calc))

        else:
            calc_background = "#B4FACB"     # pale green
            showing_all = "Below is your calculation history."

        # History text and label
        history_text = ("{}  \n\nAll calculations are shown to "
                        "the nearest whole number.".format(showing_all)
                        )
        self.text_instructions_label = Label(self.history_frame,
                                             text=history_text,
                                             width=45,
                                             justify="left",
                                             wraplength=300,
                                             padx=10,
                                             pady=10
                                             )
        self.text_instructions_label.grid(row=1)

        self.all_calc_label = Label(self.history_frame,
                                    text=calc_string_text,
                                    padx=10,
                                    pady=10,
                                    bg=calc_background,
                                    width=40,
                                    justify="left"
                                    )
        self.all_calc_label.grid(row=2)

        # instructions for saving files
        save_text = ("Either choose a custom file name (and push <Export>) "
                     "or simply push <Export> to save your calculations in a text file. "
                     "If the filename already exists, it will be overwritten!")
        self.save_instruction_label = Label(self.history_frame,
                                            text=save_text,
                                            wraplength=300,
                                            justify="left",
                                            width=40,
                                            padx=10,
                                            pady=10
                                            )
        self.save_instruction_label.grid(row=3)

        # filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff",
                                    width=25
                                    )
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_feedback = Label(self.history_frame,
                                       text="",
                                       fg="#9C0000",
                                       font=("Arial", "12", "bold")
                                       )
        self.filename_feedback.grid(row=5)

        # another frame for buttons
        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export",
                                    bg="#3399FF",
                                    fg="#000000",
                                    width=12,
                                    command=self.make_file
                                    )
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss",
                                     bg="#CC0000",
                                     fg="#000000",
                                     width=12,
                                     command=partial(self.close_history,
                                                     partner)
                                     )
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    # change calculation list into a string so that it can be outputted as a label
    def get_calc_string(self, var_calculations):
        # get maximum calculations to display (was set in __init__ function)
        max_calc = self.var_max_calc.get()
        calc_string = ""

        # generate string for writing to file (oldest calculation first)
        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"

        self.var_calc_list.set(oldest_first)

        # work out how many times need to loop to output either the last five or all calculations
        if len(var_calculations) >= max_calc:
            stop = max_calc

        else:
            stop = len(var_calculations)

        # iterate to all but last item, adding item and line break to calculation string
        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations)
                                            - item - 1]
            calc_string += "\n"

        calc_string = calc_string.strip()
        return calc_string

    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()

        filename_ok = ""
        date_part = self.get_date()

        # for default filename
        if filename == "":
            # get date and create default filename
            filename = "{}_altitude_calculations".format(date_part)

        # if users create their own filename
        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = ("Success! Your calculation history has been "
                       "saved as {}").format(filename)
            self.var_filename.set(filename)
            self.filename_feedback.config(text=success,
                                          fg="dark green")
            self.filename_entry.config(bg="#FFFFFF")

            # write content to file
            self.write_to_file()

        else:
            self.filename_feedback.config(text=filename_ok,
                                          fg="dark red")
            self.filename_entry.config(bg="#F8CECC")

    # retrieves date and creates YYYY_MM_DD string
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}_{}_{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    # checks that filename only contains letters, numbers and underscores.
    # Returns either "" if ok or the problem if there is an error
    @staticmethod
    def check_filename(filename):
        problem = ""

        # regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"

        # iterates through filename and checks each letter
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}. Use letters / numbers / underscores only.".format(problem)

        return problem

    # write history to text file
    def write_to_file(self):
        # retrieve date, filename and calculation history
        filename = self.var_filename.get()
        generated_date = self.var_todays_date.get()

        # set up strings to be written to file
        heading = "**** Altitude Calculations ****\n"
        generated = "Generated: {}\n".format(generated_date)
        sub_heading = "Here is your calculation history (oldest to newest) \n"
        all_calculations = self.var_calc_list.get()

        to_output_list = [heading, generated, sub_heading, all_calculations]

        # write output to file
        text_file = open(filename, "w+")

        for item in to_output_list:
            text_file.write(item)
            text_file.write("\n")

        # close file
        text_file.close()

    # closes help dialogue (used by button and x at top of dialogue)
    def close_history(self, partner):
        # set history button back to normal
        partner.history_button.config(state=NORMAL)
        self.history_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Altitude Converter")
    Converter()
    root.mainloop()
