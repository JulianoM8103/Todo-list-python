import tkinter as tk
import json

class TodoList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Todo List")
        self.pack()

        # Create the menu bar
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

        # Create the task frame
        task_frame = tk.Frame(self)
        task_frame.pack(side="left")

        # Create the task listbox
        self.task_listbox = tk.Listbox(task_frame)
        self.task_listbox.pack(side="left", fill="both", expand=True)
        self.task_listbox.config(height=15, width=30)

        # Create the task buttons
        task_button_frame = tk.Frame(task_frame)
        task_button_frame.pack(side="right", padx=5)

        add_task_button = tk.Button(task_button_frame, text="Add Task", command=self.add_task_window)
        add_task_button.pack(pady=5)

        edit_task_button = tk.Button(task_button_frame, text="Edit Task", command=self.edit_task_window)
        edit_task_button.pack(pady=5)

        remove_task_button = tk.Button(task_button_frame, text="Remove Task", command=self.remove_task)
        remove_task_button.pack(pady=5)

        # Load the tasks from the JSON file
        with open("todo_data.json", "r") as f:
            self.data = json.load(f)

        # Load the tasks into the task listbox
        for task in self.data["tasks"]:
            self.task_listbox.insert("end", f"{task['title']} - {task['description']}")

    def add_task_window(self):
        # Create the add task window
        add_task_window = tk.Toplevel(self)

        # Create the title label and entry
        title_label = tk.Label(add_task_window, text="Title:")
        title_label.pack()

        title_entry = tk.Entry(add_task_window)
        title_entry.pack()

        # Create the description label and entry
        description_label = tk.Label(add_task_window, text="Description:")
        description_label.pack()

        description_entry = tk.Entry(add_task_window)
        description_entry.pack()

        # Create the add task button
        add_task_button = tk.Button(add_task_window, text="Add Task", command=lambda: self.add_task(title_entry.get(), description_entry.get()))
        add_task_button.pack()

    def add_task(self, title, description):
        # Add the task to the listbox
        self.task_listbox.insert("end", f"{title} - {description}")

        # Add the task to the data
        self.data["tasks"].append({"title": title, "description": description})

        # Save the data to the JSON file
        with open("todo_data.json", "w") as f:
            json.dump(self.data, f)

    def edit_task_window(self):
        # Get the selected task from the listbox
        selection = self.task_listbox.curselection()

        if len(selection) == 1:
            # Get the task data from the data
            task = self.data["tasks"][selection[0]]

            # Create the edit task window
            edit_task_window = tk.Toplevel(self)
        
                # Create the title label and entry
        title_label = tk.Label(edit_task_window, text="Title:")
        title_label.pack()

        title_entry = tk.Entry(edit_task_window)
        title_entry.insert(0, task["title"])
        title_entry.pack()

        # Create the description label and entry
        description_label = tk.Label(edit_task_window, text="Description:")
        description_label.pack()

        description_entry = tk.Entry(edit_task_window)
        description_entry.insert(0, task["description"])
        description_entry.pack()

        # Create the edit task button
        edit_task_button = tk.Button(edit_task_window, text="Edit Task", command=lambda: self.edit_task(selection[0], title_entry.get(), description_entry.get()))
        edit_task_button.pack()

    def edit_task(self, index, title, description):
        # Update the task in the listbox
        self.task_listbox.delete(index)
        self.task_listbox.insert(index, f"{title} - {description}")

        # Update the task in the data
        self.data["tasks"][index]["title"] = title
        self.data["tasks"][index]["description"] = description

        # Save the data to the JSON file
        with open("todo_data.json", "w") as f:
            json.dump(self.data, f)

    def remove_task(self):
        # Get the selected tasks from the listbox
        selection = self.task_listbox.curselection()

        if len(selection) > 0:
            # Remove the tasks from the listbox
            for index in reversed(selection):
                self.task_listbox.delete(index)

        # Remove the tasks from the data
        self.data["tasks"] = [task for index, task in enumerate(self.data["tasks"]) if index not in selection]

        # Save the data to the JSON file
        with open("todo_data.json", "w") as f:
            json.dump(self.data, f)

root = tk.Tk()
app = TodoList(master=root)
app.mainloop()