from tkinter import *
from PIL import Image, ImageTk

from game_manager import GameManager
from type_body_manager import TypeBodyManager
WINDOW_RESOLUTION = (800,600)
DARK_GRAY = "#3B3B3B"
MIDDLE_GRAY = "#4F4F4F"
LIGHT_GRAY = "#5C5C5C"
MIDDLE_LIGHT_GRAY = "#A3A3A3"
VERY_LIGHT_GRAY = "#CFCFCF"
class Interface:
    def __init__(self):
        self.drag_x = 0
        self.drag_y = 0
        #root config
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry(
            f"{WINDOW_RESOLUTION[0]}x{WINDOW_RESOLUTION[1]}"
            f"+{(self.root.winfo_screenwidth() // 2 - WINDOW_RESOLUTION[0] // 2)}"
            f"+{(self.root.winfo_screenheight() // 2) - WINDOW_RESOLUTION[1] // 2}"
        )

        #title bar
        self.title_bar = Frame(
            self.root,
            bg=DARK_GRAY,
            relief="raised",
            bd=12,
            borderwidth=4,
        )

        self.title_bar_close_button = Button(
            self.title_bar,
            text='x',
            command=self.root.destroy
        )

        #canvas
        self.window = Canvas(
            self.root,
            bg=LIGHT_GRAY,
            highlightbackground=MIDDLE_GRAY
        )

        #title frame
        self.title_frame = Frame(
            self.window,
            bg=LIGHT_GRAY
        )

        #title text
        self.title_text = Label(
            self.title_frame,
            text="Typing Speed Text",
            font=("Verdana", 25, "bold"),
            bg=LIGHT_GRAY,
            fg=VERY_LIGHT_GRAY
        )

        #type frame
        self.type_frame = Frame(
            self.window,
            bg=LIGHT_GRAY,
            borderwidth=3,
            highlightthickness=2,
            highlightcolor=MIDDLE_LIGHT_GRAY,
            highlightbackground=MIDDLE_GRAY,
            relief="raised"
        )
        #type header
        self.type_header = Frame(
            self.type_frame,
            bg=MIDDLE_LIGHT_GRAY,
        )

        self.type_header_cpm_text = Label(
            self.type_header,
            text="Correct CPM:",
            font=("Verdana", 10),
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_header_cpm_text_result = Label(
            self.type_header,
            text="?",
            font=("Verdana", 10),
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_header_wpm_text = Label(
            self.type_header,
            text="WPM:",
            font=("Verdana", 10),
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_header_wpm_text_result = Label(
            self.type_header,
            text="?",
            font=("Verdana", 10),
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_header_time_text = Label(
            self.type_header,
            text="Time Left:",
            font=("Verdana",10),
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_header_time_text_result = Label(
            self.type_header,
            text="60",
            font=("Verdana",10),
            bg=MIDDLE_LIGHT_GRAY
        )
        self.original_icon = Image.open("./restart_icon.png")
        self.resized_icon = self.original_icon.resize((20,20),Image.Resampling.LANCZOS)
        self.restart_icon = ImageTk.PhotoImage(self.resized_icon)

        self.type_header_restart_button = Button(
            self.type_header,
            image=self.restart_icon, # type: ignore
            command=self.restart_game,
            bg=MIDDLE_LIGHT_GRAY,
            relief="solid",
            borderwidth=0,
        )

        #type body
        self.type_body = Frame(
            self.type_frame,
            bg=VERY_LIGHT_GRAY
        )

        self.type_body_manager = TypeBodyManager(self.type_body)
        self.type_body_frame_list,self.type_body_line_list=self.type_body_manager.create_type_body_paragraph(bg=VERY_LIGHT_GRAY)
        self.type_body_line_list[0][0].config(bg="blue",
                                              fg="white")
        #type bottom
        self.type_bottom = Frame(
            self.type_frame,
            bg=MIDDLE_LIGHT_GRAY
        )

        self.type_bottom_entry = Entry(
            self.type_bottom,
            bg=MIDDLE_LIGHT_GRAY,
            justify="center",
            highlightthickness=0,
        )
        self.place_holder = "Enter the first word and press space to start!"
        self.type_bottom_entry.insert(0,self.place_holder)
        self.type_bottom_entry.bind("<FocusIn>",self.on_focus_in)
        self.type_bottom_entry.bind("<space>",self.on_space)

        self.game_manager = GameManager(
            root=self.root,
            frame_list=self.type_body_frame_list,
            line_list=self.type_body_line_list,
            type_body_manager=self.type_body_manager,
            time_text = self.type_header_time_text_result,
            text_entry=self.type_bottom_entry,
            placeholder = self.place_holder,
            cpm_text=self.type_header_cpm_text_result,
            wpm_text=self.type_header_wpm_text_result
        )

        #packing widgets
        self.title_bar.pack(fill="x",side="top")
        self.title_bar_close_button.pack(side="right")
        self.window.pack(expand=True,fill="both",side="top")
        self.title_frame.pack(side="top",pady=25)
        self.title_text.pack()
        self.type_frame.pack(side="top")
        self.type_header.pack(side="top")
        self.type_body.pack(side="top",fill="x",expand=True)
        self.type_bottom.pack(side="top",fill="x",expand=True)
        self.type_bottom_entry.pack(fill="x",expand=True,pady=5)

        #header grid
        self.type_header_cpm_text.grid(column=0,row=0,padx=(50,5))
        self.type_header_cpm_text_result.grid(column=1,row=0,padx=(0,10))
        self.type_header_wpm_text.grid(column=2,row=0,padx=(0,5))
        self.type_header_wpm_text_result.grid(column=3,row=0,padx=(0,10))
        self.type_header_time_text.grid(column=4,row=0,padx=(0,5))
        self.type_header_time_text_result.grid(column=5,row=0,padx=(0,50))
        self.type_header_restart_button.grid(column=6,row=0,padx=(0,5),pady=(3,3))
        #events
        self.title_bar.bind('<Button-1>', self.start_window_drag)
        self.title_bar.bind('<B1-Motion>', self.on_window_drag)
        #mainloop
        self.root.mainloop()

    def on_space(self,event):
        if not self.game_manager.on_start:
            self.game_manager.on_start = True
            self.root.after(1000,self.game_manager.timer) #type: ignore
        answer = self.type_bottom_entry.get().replace(" ","")
        self.type_bottom_entry.delete(0,END)
        self.game_manager.check_answer(answer=answer)

    def on_focus_in(self,event):
        if self.type_bottom_entry.get() == self.place_holder:
            self.type_bottom_entry.delete(0,END)

    def restart_game(self):
        self.game_manager.restart()
    def start_window_drag(self, event):
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()

    def on_window_drag(self, event):
        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y
        self.root.geometry(f"+{x}+{y}")

Interface()