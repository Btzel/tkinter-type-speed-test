VERY_LIGHT_GRAY = "#CFCFCF"

from tkinter import messagebox,END

class GameManager:
    def __init__(self,root,frame_list,line_list,type_body_manager,time_text,text_entry,placeholder,cpm_text,wpm_text):
        #references
        self.root = root
        self.type_body_manager = type_body_manager
        self.frame_list = frame_list
        self.line_list = line_list
        self.time_text = time_text
        self.text_entry = text_entry
        self.placeholder = placeholder
        self.cpm_text = cpm_text
        self.wpm_text = wpm_text

        self.after_id = None
        self.on_start = False
        self.time = 60 #seconds
        self.line_word_index = 0
        self.correct_word_count = 0
        self.incorrect_word_count = 0
        self.all_word_count = 0
        self.typed_character_count = 0
        self.correct_character_count = 0
        self.incorrect_character_count = 0

    def restart(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        for frame in self.frame_list:
            frame.destroy()
        self.frame_list.clear()
        self.line_list.clear()
        self.time_text.config(text=f"60")
        self.cpm_text.config(text=f"?")
        self.wpm_text.config(text=f"?")
        self.type_body_manager.line_count = 0
        self.frame_list,self.line_list = self.type_body_manager.create_type_body_paragraph(bg=VERY_LIGHT_GRAY)
        self.line_list[0][0].config(bg="blue",
                                    fg="white")
        self.text_entry.delete(0, END)
        self.text_entry.insert(0,self.placeholder)
        self.root.focus()

        self.on_start = False
        self.time = 60
        self.line_word_index = 0
        self.correct_word_count = 0
        self.incorrect_word_count = 0
        self.all_word_count = 0
        self.typed_character_count = 0
        self.correct_character_count = 0
        self.incorrect_character_count = 0

    def timer(self):
        self.time -= 1
        self.time_text.config(text=f"{self.time}")
        if self.time == 0:
            self.calculate()
            return
        self.after_id = self.root.after(1000,self.timer)

    def calculate(self):
        raw_cpm = self.typed_character_count
        correct_cpm = self.correct_character_count
        raw_wpm = raw_cpm/5
        correct_wpm = correct_cpm/5
        if self.typed_character_count > 0:
            correct_word_percent = float(self.correct_word_count / self.all_word_count)
            incorrect_word_percent = float(self.incorrect_word_count / self.all_word_count)
            correct_char_percent = float(self.correct_character_count / self.typed_character_count)
            incorrect_char_percent = float(self.incorrect_character_count / self.typed_character_count)
        else:
            messagebox.showinfo(title="Test Speed Test Results",
                                message="No data acquired due to not getting any characters given by you")
            self.root.focus()
            self.restart()
            return
        if self.time == 0:
            messagebox.showinfo(
                title="Test Speed Test Results",
                message=f"Raw CPM: {raw_cpm:.2f}\n"
                        f"RAW WPM: {raw_wpm:.2f}\n"
                        f"\n"
                        f"Correct CPM: {correct_cpm:.2f}\n"
                        f"Correct WPM: {correct_wpm:.2f}\n"
                        f"\n"
                        f"Correct Word Percent: {correct_word_percent:.2f}%\n"
                        f"Incorrect Word Percent: {incorrect_word_percent:.2f}%\n"
                        f"\n"
                        f"Correct Character Percent: {correct_char_percent:.2f}%\n"
                        f"Incorrect Character Percent: {incorrect_char_percent:.2f}%\n"
            )
            self.root.focus()
            self.restart()

    def check_answer(self,answer):
        self.all_word_count += 1
        if answer.lower() == self.line_list[0][self.line_word_index].cget('text'):
            self.correct_word_count += 1
            self.correct_character_count += len(answer)
            self.line_list[0][self.line_word_index].config(bg="green")
        else:
            self.line_list[0][self.line_word_index].config(bg="red")
            self.incorrect_word_count += 1
            for i in range(len(answer.lower())):
                for j in range(len(self.line_list[0][self.line_word_index].cget('text'))):
                    if i == j:
                        if answer.lower()[i] == self.line_list[0][self.line_word_index].cget('text')[j]:
                            self.correct_character_count += 1
                        else:
                            self.incorrect_character_count += 1
        self.typed_character_count += len(answer)
        if self.line_word_index < len(self.line_list[0])-1:
            self.line_list[0][self.line_word_index + 1].config(bg="blue",
                                                               fg="white")
        else:
            self.line_list[1][0].config(bg="blue",
                                        fg="white")
        self.line_word_index += 1
        if self.line_word_index > len(self.line_list[0]) - 1:
            self.frame_list[0].destroy()
            self.frame_list.pop(0)
            self.line_list.pop(0)

            new_frame,new_line = self.type_body_manager.create_type_body_line(bg=VERY_LIGHT_GRAY)

            self.frame_list.append(new_frame)
            self.line_list.append(new_line)
            self.line_word_index = 0

        current_correct_cpm = self.correct_character_count
        current_correct_wpm = current_correct_cpm / 5

        self.cpm_text.config(text=current_correct_cpm)
        self.wpm_text.config(text=current_correct_wpm)


