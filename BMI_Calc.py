#!/user/bin/env python3
"""This program creates a simple BMI calculator that can be run in both measurement systems."""
import tkinter as tk
import customtkinter as ctk
from BMI_Settings import *


class Window(ctk.CTk):
    def __init__(self):

        # Window Setup
        super().__init__(fg_color=PINK)
        self.title("BMI Calculator")
        # self.iconbitmap()  # this would make an ico file the window icon
        self.icon = tk.PhotoImage(file="muffin.png")  # opens image
        self.wm_iconbitmap()  # converts the image to an icon
        self.iconphoto(True, self.icon)  # sets the image as the window's icon
        self.geometry("400x400")
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        # data
        self.metric_toggle = ctk.BooleanVar(value=False)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65.0)
        self.bmi_str = ctk.StringVar()
        self.update_bmi()

        # tracing
        self.height_int.trace("w", self.update_bmi)  # trace either when reading or writing the value
        self.weight_float.trace("w", self.update_bmi)
        self.metric_toggle.trace("w", self.change_unit)

        # widget
        BMI(self, self.bmi_str)
        self.weight_input = Weight_Input(self, self.weight_float, self.metric_toggle)
        self.height_input = Height_Input(self, self.height_int, self.metric_toggle)
        Unit_Switch(self, self.metric_toggle)

    def change_unit(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()

    def update_bmi(self, *args):  # when running trace, tkinter adds arguments.
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2, 1)
        self.bmi_str.set(str(bmi_result))  # update bmi_str by passing in the result

    def change_title_bar_color(self):
        try:
            from ctypes import windll, byref, sizeof, c_int
            HWMD = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWMD, 35, byref(c_int(BMI_Settings.TITLE_HEX_COLOR)), sizeof(c_int))
        except:
            pass

    # widgets


class BMI(ctk.CTkLabel):
    def __init__(self, parent: ctk.CTk, bmi: ctk.StringVar):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight="bold")  # has to be made before the init
        super().__init__(parent, textvariable=bmi, font=font, text_color=WHITE)
        self.grid(column=0, row=0, rowspan=2, sticky="news")


class Weight_Input(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, weight: ctk.DoubleVar, metric_toggle: ctk.BooleanVar):
        super().__init__(parent, fg_color=WHITE)
        self.metric_toggle = metric_toggle
        self.weight = weight
        self.grid(column=0, row=2, sticky="news", padx=10, pady=10)

        # output logic
        self.output_string = ctk.StringVar()
        self.update_weight()

        # layout
        self.columnconfigure((0, 4), weight=2, uniform="b")
        self.columnconfigure((1, 3), weight=1, uniform="b")
        self.columnconfigure(2, weight=3, uniform="b")
        self.rowconfigure(0, weight=1, uniform="b")

        # widgets
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        small_font = ctk.CTkFont(family=FONT, size=SMALL_INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, textvariable=self.output_string, text_color=BLACK, font=font)
        label.grid(column=2, row=0)

        minus_button = ctk.CTkButton(self,
                                     text="-",
                                     font=font,
                                     text_color=BLACK,
                                     fg_color=LIGHT_GRAY,
                                     hover_color=GRAY,
                                     corner_radius=CORNER_RADIUS,
                                     command=lambda: self.update_weight(("minus", "large")))
        minus_button.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

        small_minus_button = ctk.CTkButton(self,
                                           text="-",
                                           font=small_font,
                                           text_color=BLACK,
                                           fg_color=LIGHT_GRAY,
                                           hover_color=GRAY,
                                           corner_radius=CORNER_RADIUS,
                                           command=lambda: self.update_weight(("minus", "small")))
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

        plus_button = ctk.CTkButton(self,
                                    text="+",
                                    font=font,
                                    text_color=BLACK,
                                    fg_color=LIGHT_GRAY,
                                    hover_color=GRAY,
                                    corner_radius=CORNER_RADIUS,
                                    command=lambda: self.update_weight(("plus", "large")))
        plus_button.grid(row=0, column=4, sticky="ns", padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self,
                                          text="+",
                                          font=small_font,
                                          text_color=BLACK,
                                          fg_color=LIGHT_GRAY,
                                          hover_color=GRAY,
                                          corner_radius=CORNER_RADIUS,
                                          command=lambda: self.update_weight(("plus", "small")))
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

    def update_weight(self, info: tuple = None):
        if info:
            if not self.metric_toggle.get():
                amount = 1 if info[1] == "large" else 0.1
                weight = round(float(self.weight.get()), 1)
                if info[0] == "plus":
                    self.weight.set(weight + amount)
                else:
                    self.weight.set(weight - amount)
            else:
                amount = 0.4535924 if info[1] == "large" else 0.02834952
                if info[0] == "plus":
                    self.weight.set(self.weight.get() + amount)
                else:
                    self.weight.set(self.weight.get() - amount)
        else:
            if not self.metric_toggle:
                weight = round(self.weight.get(), 1)
                self.weight.set(weight)
            else:
                self.weight.set(self.weight.get())
        if self.metric_toggle.get():
            total = self.weight.get() / 0.4535924
            pounds = int(total)
            ounces = int(round((total - pounds) * 16, 0))
            self.output_string.set(f"{pounds}lbs {ounces}oz")
        elif not self.metric_toggle.get():
            self.output_string.set(f"{round(self.weight.get(), 1)}kg")


class Height_Input(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, height: ctk.IntVar, metric_toggle: ctk.BooleanVar):
        self.metric_toggle = metric_toggle
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE)
        super().__init__(parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky="news", padx=10, pady=10)
        self.height = height

        # widgets
        slider = ctk.CTkSlider(self,
                               orientation="horizontal",
                               from_=33,
                               to=300,
                               variable=height,
                               button_color=PINK,
                               button_hover_color=LIGHT_PINK,
                               progress_color=PINK,
                               fg_color=GRAY,
                               command=self.update_text)
        slider.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        # output logic
        self.output_string = ctk.StringVar()
        self.update_text(height.get())
        output_text = ctk.CTkLabel(self, textvariable=self.output_string, font=font, text_color=BLACK)
        output_text.pack(side="left", padx=20, pady=10)

    def update_text(self, amount: int):
        if not self.metric_toggle.get():
            amount = str(int(amount))
            if len(amount) < 3:
                meter = 0
                centimeter = amount
            else:
                meter = amount[0]
                centimeter = amount[1:]
            self.output_string.set(f"{meter}.{centimeter}m")
        elif self.metric_toggle.get():
            feet, inches = divmod(int(amount) / 2.54, 12)
            self.output_string.set(f"{int(feet)}\' {int(inches)}\"")


class Unit_Switch(ctk.CTkButton):
    def __init__(self, parent: ctk.CTk, metric_toggle: ctk.BooleanVar):
        self.metric_toggle = metric_toggle
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight="bold")
        super().__init__(parent,
                         text="Metric ",
                         fg_color=PINK,
                         font=font,
                         width=20,
                         hover_color=DARK_PINK,
                         text_color=WHITE,
                         corner_radius=CORNER_RADIUS,
                         command=self.change_units)
        self.place(relx=0.999, rely=0.001, anchor="ne")

    def change_units(self):
        # change the metric boolean
        self.metric_toggle.set(not self.metric_toggle.get())

        if not self.metric_toggle.get():
            self.configure(text="Metric ")
        elif self.metric_toggle.get():
            self.configure(text="English")


if __name__ == "__main__":
    Window().mainloop()
