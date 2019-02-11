from tkinter import BooleanVar, Radiobutton, StringVar, Checkbutton


class ChoiceType:
    CHECK_BOX = "checkbox_type"
    RADIO_BUTTON = "radiobutton_type"


class ChoiceItemFactory:
    choice_type = None

    def __init__(self, master):
        self.master = master

    def of(self, choice_type: ChoiceType):
        self.choice_type = choice_type
        return self

    def get(self, text):
        var = None
        choice_btn = None
        if self.choice_type == ChoiceType.RADIO_BUTTON:
            var = StringVar()
            choice_btn = Radiobutton(self.master, text=text,
                                     variable=var,
                                     value=text,
                                     command=self.click,
                                     font=("Times New Roman", 14))
        elif self.choice_type == ChoiceType.CHECK_BOX:
            var = BooleanVar()
            choice_btn = Checkbutton(self.master, text=text,
                                     variable=var,
                                     command=self.click,
                                     font=("Times New Roman", 14))

        return {
            "var": var,
            "choice_btn": choice_btn
        }

    def click(self):
        print(self)
