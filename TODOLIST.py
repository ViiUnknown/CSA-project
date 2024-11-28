import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import pickle
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List")
        self.tasks = []
        # File path to store information
        self.file_path  = 'to-do-list.pkl'

        #Load tasks from file if it exists
        self.load_tasks()

         # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=0)  # Header row (fixed size)
        self.root.grid_rowconfigure(1, weight=0)  # Search bar row (fixed size)
        self.root.grid_rowconfigure(2, weight=1)  # Task list row (expandable)
        self.root.grid_rowconfigure(3, weight=0)  # Buttons row (fixed size)
        self.root.grid_columnconfigure(0, weight=1)  # First column
        self.root.grid_columnconfigure(1, weight=1)  # Second column
        self.root.grid_columnconfigure(2, weight=1)  # Third column
        self.root.grid_columnconfigure(3, weight=0)

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#4CAF50", pady=10)  # Modern color
        self.header_frame.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.header_label = tk.Label(
            self.header_frame, 
            text="TO-DO LIST", 
            font=("Helvetica", 20, "bold"), 
            bg="#4CAF50", 
            fg="white"
        )
        self.header_label.pack(pady=5)

        # Search Frame
        self.search_frame = tk.Frame(self.root)
        self.search_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=10, pady=5)

        tk.Label(self.search_frame, text="Search:", font=("Helvetica", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(self.search_frame, width=25, font=("Helvetica", 10))
        self.search_entry.pack(side="left", padx=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_tasks)
        self.search_button.pack(side="left", padx=5)
        self.clear_search_button = tk.Button(self.search_frame, text="Clear", command=self.clear_search)
        self.clear_search_button.pack(side="left", padx=5)

        # Task display listbox
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, font=("Helvetica", 10))
        self.task_listbox.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        scrollbar = tk.Scrollbar(self.root, command=self.task_listbox.yview)
        scrollbar.grid(row=2, column=3, sticky="ns")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Add Task Button
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task, bg="#2196F3", fg="white", font=("Helvetica", 10))
        self.add_task_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Delete Task Button
        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_tasks, bg="#f44336", fg="white", font=("Helvetica", 10))
        self.delete_task_button.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        # Mark Completed Button
        self.mark_completed_button = tk.Button(self.root, text="Mark as Complete", command=self.mark_task_completed, bg="#FF9800", fg="white", font=("Helvetica", 10))
        self.mark_completed_button.grid(row=3, column=2, sticky="ew", padx=10, pady=5)

        # Update display with loaded tasks
        self.update_task_display()


    def add_task(self):
        #Create a window for adding a task
        task_window = tk.Toplevel(self.root)
        task_window.geometry("300x400")
        task_window.title("Add New Task")

        #Task Description entry
        tk.Label(task_window, text="Task Description: ").pack(pady=5)
        task_description = tk.Entry(task_window, width=60)
        task_description.pack(pady=5)

        #Date Picker
        tk.Label(task_window, text="Select Due Date:").pack(pady=5)
        calendar = Calendar(task_window, date_pattern="yyyy-mm-dd")
        calendar.pack(pady=5)

        #Time Picker
        time_frame = tk.Frame(task_window)
        time_frame.pack(pady=5)

        tk.Label(time_frame, text="Time").pack(side="left")
        hour_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=2, format="%02.0f")
        hour_spinbox.pack(side="left")
        tk.Label(time_frame, text=":").pack(side="left")
        minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=2, format="%02.0f")
        minute_spinbox.pack(side="left")

        def save_tasks():
            task_text = task_description.get()
            if task_text:
                selected_date = calendar.get_date()
                hour = int(hour_spinbox.get())
                minute = int(minute_spinbox.get())
                due_date = datetime.strptime(selected_date, "%Y-%m-%d").replace(hour=hour, minute=minute)

                task = {"task": task_text, "due_date": due_date, "completed": False}
                self.tasks.append(task)
                self.save_tasks()
                self.update_task_display()
                task_window.destroy()

            else:
                messagebox.showerror("Input Error", "Please enter a task description.")

        tk.Button(task_window, text="Add Task", command=save_tasks).pack(pady=10)


    def delete_tasks(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            self.save_tasks()
            self.update_task_display()
        else:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
    
    def mark_task_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[selected_task_index[0]]
            task["completed"] = not task["completed"]
            self.save_tasks()
            self.update_task_display()
        else:
            messagebox.showwarning("Select Task", "Please select a task to mark as completed.")  
   
    def search_tasks(self):
        query = self.search_entry.get().lower()
        if query:
            filtered_tasks = [
                task for task in self.tasks
                if query in task["task"].lower() or query in task["due_date"].strftime('%Y-%m-%d %H:%M')
            ]
            self.update_task_display(filtered_tasks)

        else:
            messagebox.showinfo("Search", "Enter a keyword or date to search.")

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.update_task_display()

    def update_task_display(self, task_list=None):
        self.task_listbox.delete(0, tk.END)
        task_list = task_list if task_list else self.tasks
        for task in task_list:
            if task["completed"]:
                status = "✔"
                task_text = f"{status} {task['task']} - Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')}"
            else:
                task_text = f"{task['task']} - Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')}"
                
            self.task_listbox.insert(tk.END, task_text)

    def save_tasks(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as f:
                self.tasks = pickle.load(f)

            for task in self.tasks:
                if "completed" not in task:
                    task["completed"] = False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = ToDoApp(root)
    root.mainloop()