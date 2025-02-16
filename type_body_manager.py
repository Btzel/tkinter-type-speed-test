from tkinter import *
import random

class TypeBodyManager:
    def __init__(self,type_body):
        #type body reference
        self.type_body = type_body
        #word list
        self.word_list = self.create_words_list()

        self.line_count = 0
        self.word_count = 0

    def create_type_body_paragraph(self,bg):
        type_body_frame_list = []
        type_body_line_list = []
        while self.line_count < 8:
            type_body_line_frame, type_body_line_texts_list = self.create_type_body_line(bg)
            type_body_frame_list.append(type_body_line_frame)
            type_body_line_list.append(type_body_line_texts_list)
            self.line_count += 1
        return type_body_frame_list,type_body_line_list

    def create_type_body_line(self,bg):
        type_body_line_texts = []
        type_body_line_frame = Frame(
            self.type_body,
            bg=bg
        )
        type_body_line_frame.pack(side="top",
                            fill="x",
                            expand=False)

        random_words = self.pick_random_words()
        for word in random_words:
            type_body_text = Label(
                type_body_line_frame,
                text=word,
                font=("Verdana",15),
                bg=bg
            )
            type_body_text.pack(side="left",
                                expand=True,
                                fill="x")
            type_body_line_texts.append(type_body_text)
        return type_body_line_frame,type_body_line_texts

    def pick_random_words(self):
        character_number = 0
        random_words = []
        while character_number < 32:
            random_word_index = random.randint(0,len(self.word_list))
            random_word = self.word_list[random_word_index]
            random_words.append(random_word)
            self.word_list.pop(random_word_index)
            character_number += len(random_word) + 1
        return random_words

    @staticmethod
    def create_words_list():
        word_list = []
        with open(file="words_alpha.txt",mode="r") as words_file:
            for word in words_file.readlines():
                word = word.replace("\n","")
                if len(word) == 4 or len(word) ==5:
                    word_list.append(word)
        return word_list




