
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from tkinter import filedialog
from tkinter import *
import tkcalendar as tkc
import tkinter.ttk as ttk
import customtkinter as ctk
import pandas as pd
import time
import math
import webbrowser
from dateutil import parser



def open_youtube_video():
    webbrowser.open("https://www.youtube.com/watch?v=PcbvWvVIIz4&t=5s")

    
class Listify:
    def __init__(self, master):

        self.root=root
        self.master = master
        master.title("Listify")
        self.tasks = []
        self.create_widgets()
        self.check_deadlines()

    
    def cut():
        root.clipboard_clear()
        root.clipboard_append(root.selection_get())

    # Function to handle the copy event
    def copy():
        root.clipboard_clear()
        root.clipboard_append(root.selection_get())

    # Function to handle the paste event
    def paste():
        try:
            text = root.clipboard_get()
            root.insert(INSERT, text)
        except TclError:
            pass


    def check_deadlines(self):
        tasks_to_remove = []
        now = datetime.datetime.now()

        for _, task in enumerate(self.tasks):
            if task["deadline"] == "Deadline":
                continue
            deadline = parser.parse(str(task["deadline"]))
            reminder = deadline - datetime.timedelta(minutes=15)
            if reminder <= now < deadline:
                if not task.get('reminder_shown'):
                    messagebox.showwarning("Reminder", f"Task {task['task']} is due in 15 minutes- deadline is approaching.")
                    task['reminder_shown'] = "15 minutes"
            elif now >= deadline and task.get('reminder_shown') != "due time":
                messagebox.showwarning("Reminder", f"Task {task['task']} deadline has reached and is overdue.")
                task['reminder_shown'] = "due time"
                self.master.after(math.ceil((deadline - now).total_seconds() * 1000), self.update_countdown, task["task_id"])
                tasks_to_remove.append(task)


        self.master.after(1 * 1000, self.check_deadlines)
        


    def create_widgets(self):
        
        img_label = tk.Label()
        img_label.image = tk.PhotoImage(file="./main_logo.png")
        img_label['image'] = img_label.image

    
        img_label.pack()
        # Create the task frame
        task_frame = ctk.CTkFrame(self.master)
        task_frame.pack()

        # Create the task label
        task_label = ctk.CTkLabel(task_frame, text="Task:")
        task_label.grid(row=0, column=0, padx=5, pady=5)

        # Create the task entry
        self.task_entry = ctk.CTkEntry(task_frame)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create the project label
        project_label = ctk.CTkLabel(task_frame, text="Project:")
        project_label.grid(row=1, column=0, padx=5, pady=5)

        # Create the project entry
        self.project_entry = ctk.CTkEntry(task_frame)
        self.project_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create the deadline label
        deadline_label = ctk.CTkLabel(task_frame, text="Deadline:")
        deadline_label.grid(row=2, column=0, padx=5, pady=5)

        # Create the deadline entry frame
        self.deadline_entry = ctk.CTkFrame(task_frame)
        self.deadline_entry.grid(row=2, column=1, padx=5, pady=5)
        

        # Create the calendar widget
        self.Calendar = tkc.DateEntry(self.deadline_entry, style='my.DateEntry', width=12, background='darkblue', foreground='white', borderwidth=2)
        self.show_calendar_btn = ctk.CTkButton(self.deadline_entry, text="Select Date", command=self.show_calendar)
        self.show_calendar_btn.grid(row=0, column=0, padx=5, pady=5)
        self.selected_date_label = tk.Label(self.deadline_entry, text="No date selected")
        self.selected_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.Calendar.configure(background="black", disabledbackground="black", bordercolor="black", 
               headersbackground="black", normalbackground="black", foreground='white', normalforeground='cyan', headersforeground='white')
        
        
        # Create the time Combobox
        self.time_combobox = ttk.Combobox(self.deadline_entry, foreground='grey',values=[f"{i:02d}:{j:02d}" for i in range(24) for j in range(60)])
        self.time_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.time_combobox.set("00:00")
        
        # Create the priority label
        priority_label = ctk.CTkLabel(task_frame, text="Priority:")
        priority_label.grid(row=3, column=0, padx=5, pady=5)

        # Create the priority entry
        self.priority_var = tk.StringVar()
        self.priority_var.set("High")
        self.priority_entry = tk.OptionMenu(task_frame, self.priority_var, "High", "Medium", "Low")
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)
        self.priority_entry.configure(fg='grey')

        # Create the add task button
        add_task_button = ctk.CTkButton(task_frame, text="Add Task", command=self.add_task)
        add_task_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Create the task list frame
        task_list_frame = ctk.CTkFrame(self.master)
        task_list_frame.pack()

        # Create the task list label
        task_list_label = ctk.CTkLabel(task_list_frame, text="Tasks:")
        task_list_label.grid(row=0, column=0, columnspan=2)

        # Create the task list treeview
        self.task_tree = ttk.Treeview(task_list_frame, columns=("task", "project", "deadline", "priority"))
        self.task_tree.heading("#0", text="Task")
        self.task_tree.heading("#1", text="Project")
        self.task_tree.heading("#2", text="Deadline")
        self.task_tree.heading("#3", text="Priority")
        self.task_tree.heading("#4", text="Task Due In")
        self.task_tree.column("#0", stretch=tk.YES,)
        self.task_tree.column("#1", stretch=tk.YES)
        self.task_tree.column("#2", stretch=tk.YES)
        self.task_tree.column("#3", stretch=tk.YES)
        self.task_tree.column("#4", stretch=tk.YES)


        
        self.task_tree.grid(row=1, column=0, columnspan=2)
        s = ttk.Style()
        s.configure("Treeview.Heading", foreground="black")

        # Create the task list scrollbar
        task_list_scrollbar = ctk.CTkScrollbar(task_list_frame)
        task_list_scrollbar.grid(row=1, column=2, sticky="ns")

        # Set the task list treeview and scrollbar to scroll together
        self.task_tree.configure(yscrollcommand=task_list_scrollbar.set)
        task_list_scrollbar.configure(command=self.task_tree.yview)

        # Create the task list buttons frame
        task_list_buttons_frame = ctk.CTkFrame(task_list_frame)
        task_list_buttons_frame.grid(row=2, column=0, columnspan=2, pady=5)

        load_tasks_button = ctk.CTkButton(task_list_buttons_frame, text="Load Tasks", command=self.load_tasks_from_excel)
        load_tasks_button.grid(row=1, column=1, padx=5, pady=5)

        # Create the edit task button
        edit_task_button = ctk.CTkButton(task_list_buttons_frame, text="Edit Task", command=self.edit_task)
        edit_task_button.grid(row=0, column=0, padx=5, pady=5)

        # Create the delete task button
        delete_task_button = ctk.CTkButton(task_list_buttons_frame, text="Delete Task", command=self.delete_task)
        delete_task_button.grid(row=0, column=1, padx=5, pady=5)
        
        #Create the help tutorial button
        btn = ctk.CTkButton(root, text="Help/Tutorial Video", command=open_youtube_video, fg_color="grey")
        btn.pack(side="bottom", anchor="se")

        # Create the export to csv button
        export_to_excel_button = ctk.CTkButton(task_list_buttons_frame, text="Export to Excel", command=self.export_to_excel)
        export_to_excel_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Create the search label
        search_label = ctk.CTkLabel(task_list_buttons_frame, text="Find:")
        search_label.grid(row=4, column=0, padx=5, pady=40, sticky="e")
        
        # Create the search entry
        self.search_entry = ctk.CTkEntry(task_list_buttons_frame)
        self.search_entry.grid(row=4, column=1, padx=5, pady=40)
        
        # Create the search button
        search_button = ctk.CTkButton(task_list_buttons_frame, text="Find", command=self.search_task)
        search_button.grid(row=4, column=2, padx=5, pady=40)
        
        
        self.root.bind("<Control-c>", self.copy)
        self.root.bind("<Control-x>", self.cut)
        self.root.bind("<Control-v>", self.paste)
        self.root.bind("<Command-c>", self.copy)
        self.root.bind("<Command-x>", self.cut)
        self.root.bind("<Command-v>", self.paste)


    def show_calendar(self):
        self.Calendar.drop_down()
        self.Calendar.bind("<<DateEntrySelected>>", self.update_selected_date)
    
    def update_selected_date(self, event):
        selected_date = self.Calendar.get()
        self.selected_date_label.config(text=selected_date)
        
    def search_task(self):
        task = self.search_entry.get()
        for i in self.task_tree.get_children():
            item_values = self.task_tree.item(i, 'values')
            for value in item_values:
                if task in str(value):
                    self.task_tree.selection_set(i)
                    self.task_tree.see(i)
                    break
            else:
                continue
            break
        else:
            messagebox.showinfo("Not Found", f"{task} is not found")



    def add_task(self):
        task = self.task_entry.get()
        project = self.project_entry.get()
        deadline = self.Calendar.get_date()
        time = self.time_combobox.get()
        deadline_time = datetime.datetime.strptime(time, "%H:%M").time()
        deadline = datetime.datetime.combine(deadline, deadline_time)
        deadline = deadline.strftime("%Y-%m-%d %H:%M")
        

        priority = self.priority_var.get()

        if task == "":
            messagebox.showerror("Error", "Please enter a task.")
            return
        if project == "":
            messagebox.showerror("Error", "Please enter a project.")
            return
        if deadline == "":
            messagebox.showerror("Error", "Please enter a deadline.")
            return
        if priority == "":
            messagebox.showerror("Error", "Please enter a priority.")
            return

        
        task_id = self.task_tree.insert("", "end", text=task, values=(project, deadline, priority))
        self.task_tree.item(task_id, tags=(priority,))
        

        if priority == "High":
            self.task_tree.item(task_id, tags=("high_priority",))
            
        elif priority == "Medium":
            self.task_tree.item(task_id, tags=("medium_priority",))
            
        elif priority == "Low":
            self.task_tree.item(task_id, tags=("low_priority",))
        
        self.colour_update(task_id, priority) 
        
        
        self.tasks.append({"task_id": task_id, "task": task, "project": project, "deadline": deadline, "priority": priority})
        messagebox.showwarning("Success", "Task added and reminder created successfully. In order to receive reminders for '{}', do not close Listify.".format(task))
        self.master.after(1000, self.update_countdown, task_id)
        self.update_countdown(task_id)
        self.task_entry.delete(0, tk.END)
        self.project_entry.delete(0, tk.END)
        self.priority_var.set("High")
        
        
    # Create a function to update the countdown label
    def update_countdown(self, task_id):
        task = None
        for _, t in enumerate(self.tasks):
            if t["task_id"] == task_id:
                task = t
                break
        if task is None:
            return

        now = datetime.datetime.now()
        deadline = parser.parse(str(task["deadline"]))
        delta = deadline - now

        if now >= deadline:
            self.task_tree.set(task_id, "#4", "Overdue")
            return
        else:
            days, seconds = divmod(delta.days * 86400 + delta.seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            seconds = seconds % 60
            self.task_tree.set(task_id, "#4", f"{days}d {hours}h {minutes}m {seconds}s")

        self.master.after(1000, self.update_countdown, task_id)


    def edit_task(self):
        selected_task = self.task_tree.selection()

        if not selected_task:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        task_id = selected_task[0]
        task_data = self.task_tree.item(task_id)

        self.task_entry.delete(0, tk.END)
        self.task_entry.insert(0, task_data["text"])

        self.project_entry.delete(0, tk.END)
        self.project_entry.insert(0, task_data["values"][0])

        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, task_data["values"][1])

        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, task_data["values"][2])

        self.task_tree.delete(task_id)

        for i, task in enumerate(self.tasks):
            if task["task_id"] == task_id:
                del self.tasks[i]

        self.save_tasks()

    def delete_task(self):
        selected_tasks = self.task_tree.selection()
        if not selected_tasks:
            messagebox.showerror("Error", "Please select a task to delete.")
            return
    
        for task_id in selected_tasks:
            if task_id in self.task_tree.get_children():
                self.task_tree.delete(task_id)
                for i, task in enumerate(self.tasks):
                    if task["task_id"] == task_id:
                        del self.tasks[i]

    def export_to_excel(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", initialdir=os.getcwd(), initialfile = "tasks.xlsx")
        self.file_path = filepath
        if filepath:
            tasks = pd.DataFrame(self.tasks, columns=["task", "project", "deadline", "priority"])
            tasks.to_excel(filepath, index=False)
        self.save_tasks(filepath)

    def load_tasks_from_excel(self):
        file_path = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select file", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
        self.file_path = file_path
        try:
            if os.path.exists(file_path):
                tasks = pd.read_excel(file_path)
                for i, row in tasks.iterrows():
                    task = row["task"]
                    project = row["project"]
                    deadline = row["deadline"]
                    priority = row["priority"]
                    task_id = self.task_tree.insert("", "end", text=task, values=(project, deadline, priority))
                    self.colour_update(task_id, priority)                       
                    self.tasks.append({"task_id": task_id, "task": task, "project": project, "deadline": deadline, "priority": priority})
                    self.update_countdown(task_id)
        except FileNotFoundError:
            pass
        except ValueError as e:
            print(e)
            messagebox.showerror("Error", "Invalid Excel file")

    def save_tasks(self, filepath):
        tasks = pd.DataFrame(self.tasks, columns=["task", "project", "deadline", "priority"])
        tasks.to_excel(filepath, index=False)


    def colour_update(self,task_id, priority):
        if priority == "High":
            self.task_tree.item(task_id, tags=("high_priority",))
            self.task_tree.tag_configure("high_priority", foreground="pink")
        elif priority == "Medium":
            self.task_tree.item(task_id, tags=("medium_priority",))
            self.task_tree.tag_configure("medium_priority", foreground="orange")
        elif priority == "Low":
            self.task_tree.item(task_id, tags=("low_priority",))
            self.task_tree.tag_configure("low_priority", foreground="cyan")

            
root = ctk.CTk()
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icon.png'))
root.overrideredirect(1)
app_width = 600
app_height = 400


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.configure(bg="black")

logo = tk.PhotoImage(file="./splash_screen_logo.png")
logo_label = tk.Label(root, image=logo, bg="#232324")
logo_label.pack(pady=20)

loading_text = tk.StringVar()
loading_label = tk.Label(root, textvariable=loading_text, fg="white", bg="#232324", font=("Arial", 14))
loading_label.pack()

loading_label = tk.Label(root, text="Loading...", fg="grey", bg="#232324", font=("Arial", 12))
loading_label.pack()


root.update()

loading_text.set("Loading User Interface")
root.update()

progress_bar = ttk.Progressbar(root, length=400)
progress_bar.pack(pady=20)

for i in range(101):
    progress_bar["value"] = i
    progress_bar.update()
    time.sleep(0.03)
    if i == 33:
        loading_text.set("Loading Assets")
        root.update()
    elif i == 67:
        loading_text.set("Initializing")
        root.update()


copyright_label = tk.Label(root, text="Developed by Omeir Ali | All Rights Reserved © 2023", fg="grey", bg="#232324", font=("Arial", 12))
copyright_label.pack(side="right", padx=20, pady=20)

root.after(500, root.destroy)
root.mainloop()
root = ctk.CTk()
app_width = 1020
app_height = 840


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')


root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./icon.png'))

to_do_list = Listify(root)
__author__ = "Developed by: Omeir Ali"
__copyright__ = "Copyright (C) 2023 Omeir Ali"
__license__ = "Public Domain"
__version__ = "1.0"
root.mainloop()

