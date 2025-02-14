from tkinter import *
import tkinter as tk
import customtkinter

class MakeWindow:
    def __init__(self, root, Title, elements, width=750, height=1000,):
        self.root = root
        self.root.title(Title)
        self.root.geometry(f"{height}x{width}")

        self.frame = customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")  
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

#creates a dictionary to store refrence to entry box and text stored in entry box , for example if "hello" is entered into entry box with 
#placeholder text 'Username' , dictionary will store 'Username' : 'hello'
        self.entry_boxes = {}

        for i in range(len(elements)):
            if elements[i][0] == "Label":
                customtkinter.CTkLabel(self.frame, text=elements[i][1], font=(elements[i][2], elements[i][3]), text_color=elements[i][4]).pack(pady=10)
            
            elif elements[i][0] == "Button":
                function = elements[i][5]
                customtkinter.CTkButton(self.frame, text=elements[i][1], font=(elements[i][2], elements[i][3]), fg_color=elements[i][4], command=function).pack(pady=10)
           
            elif elements[i][0] == "EntryBox":
                entry = customtkinter.CTkEntry(self.frame, placeholder_text=(elements[i][1]), width=(elements[i][2]), height=(elements[i][3]))
                entry.pack()
                # Store reference to entry widget
                self.entry_boxes[elements[i][1]] = entry

            elif elements[i][0] == "ComboBox":
                Combo = customtkinter.CTkComboBox(self.frame, values=[elements[i][1], elements[i][2], elements[i][3]])
                Combo.pack()
    # Store reference to ComboBox widget
                self.entry_boxes[elements[i][1]] = Combo
            
            elif elements[i][0] == "TextBox":
                TextBox=customtkinter.CTkTextbox(self.frame,width=elements[i][1],height=elements[i][2],state=elements[i][3])
                TextBox.pack()

                self.entry_boxes[elements[i][1]]=TextBox


#function that fetches whatever is stored in a dictionary be using the refrence to the placeholder text as a parameter 
    def get_entry_value(self, name):
        if name in self.entry_boxes:
            entry_value = self.entry_boxes[name].get()
            print(entry_value)

            return(entry_value)

    def get_combo_value(self,name):
        if name in self.entry_boxes:
            # Access the ComboBox object using the key and get its value
            combo_box_value = self.entry_boxes[name].get()
            print(combo_box_value)
            return combo_box_value
        
    #def Insert_TextBox(self,name,value):

     #   self.entry_boxes[name].insert(value)
      #  print(self.entry_boxes[name].get())
       # return

    def add_label(self, text,size=18):
        for item in text:
            label = customtkinter.CTkLabel(self.frame, text=item, font=("Arial", size))
            label.pack(pady=10, padx=10, anchor='center', side='top', fill='both')
    
    def add_label_string(self, text,size=18):
        label = customtkinter.CTkLabel(self.frame, text=text, font=("Arial", size))
        label.pack(pady=10, padx=10, anchor='center', side='top', fill='both')

    def Messages(self,text):
        TextBox = customtkinter.CTkTextbox(self.frame)
        TextBox.pack()
        TextBox.insert(text=text)