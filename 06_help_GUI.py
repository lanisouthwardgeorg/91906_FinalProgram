from tkinter import *
from functools import partial # to prevent unwanted windows


class Converter:

    def __init__(self):
        # common format for all buttons (Arial size 14, bold, white text)
        button_font = ("Arial", "14", "bold")
        button_fg = "#000000"
        # background button colours doesn't work on Mac, see this link:
        # https://stackoverflow.com/questions/72056706/tkinter-button-background-color-is-not-working-in-mac-os
        button_bg_help = "#CC6600"

        # set up GUI frame
        self.altitude_frame = Frame(padx=10, pady=10)
        self.altitude_frame.grid()

        # conversion, help and history/export buttons
        self.button_frame = Frame(self.altitude_frame)
        self.button_frame.grid(row=4)

        self.help_button = Button(self.button_frame,
                                  text="Help/Info",
                                  bg=button_bg_help,
                                  fg=button_fg,
                                  font=button_font, width=12,
                                  command=self.to_help)
        self.help_button.grid(row=1, column=0, padx=5, pady=5)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):

        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # if users press cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, bg=background,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("To use the program, simply enter the altitude you wish to convert and then choose to convert "
                     "either to metres or to feet. \n\n"
                     "Note that you must enter only numbers otherwise you will get an error message. \n\n"
                     "To see your calculation history and export it to a text file, "
                     "please click the 'History / Export' button")
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wrap=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#000000",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # put help button back to normal
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Altitude Converter")
    Converter()
    root.mainloop()
