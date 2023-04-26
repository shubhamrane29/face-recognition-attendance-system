import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import mysql.connector

def dept_wise_attendance():
    # Create the default window
    root = tk.Tk()
    root.title("Department Wise Attendance")

    # Create the list of options
    options_list = ["advance_tcp",
                    "component_engineer",
                    "distributed_computing",
                    "enterprise_system",
                    "image_processing",
                    "it_lab",
                    "it_project_management",
                    "marketing_research",
                    "mobile_computing",
                    "operational_management",
                    "project_stage_2",
                    "psycology",
                    "seminar",
                    "web_engineering"]

    # Variable to keep track of the option
    # selected in OptionMenu
    value_inside = tk.StringVar(root)

    # Set the default value of the variable
    value_inside.set("Select Subject")

    # Create the optionmenu widget and passing
    # the options_list and value_inside to it.
    question_menu = tk.OptionMenu(root, value_inside, *options_list)
    question_menu.pack()

    # Function to print the submitted option-- testing purpose

    def print_answers():
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shubham@123",
            database="attendance"
        )

        # Create a cursor object
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM {value_inside.get()}")

        rows = cursor.fetchall()

        # Clear the existing rows in the Treeview widget
        tree.delete(*tree.get_children())

        # Insert each row from the SQL table into the Treeview widget
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Submit button
    # Whenever we click the submit button, our submitted
    # option is printed ---Testing purpose
    submit_button = tk.Button(root, text='View Attendance', command=print_answers)
    submit_button.pack()

    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5"))

    # Set the headings for the columns
    tree.heading("col1", text="Name")
    tree.heading("col2", text="Department")
    tree.heading("col3", text="Date")
    tree.heading("col4", text="Time")
    tree.heading("col5", text="Subject")

    # Pack the Treeview widget into the window
    tree.pack()

    # Start the main loop to display the window
    root.mainloop()


def dept_wise_attendance_student():
    # Create the default window
    root = tk.Tk()
    root.title("Department Wise Attendance")

    # Create the list of options
    options_list = ["advance_tcp",
                    "component_engineer",
                    "distributed_computing",
                    "enterprise_system",
                    "image_processing",
                    "it_lab",
                    "it_project_management",
                    "marketing_research",
                    "mobile_computing",
                    "operational_management",
                    "project_stage_2",
                    "psycology",
                    "seminar",
                    "web_engineering"]

    # Variable to keep track of the option
    # selected in OptionMenu
    value_inside = tk.StringVar(root)

    name_label = tk.Label(root, text="Enter your name:")
    name_label.pack()

    name_entry = tk.Entry(root)
    name_entry.pack()

    # Set the default value of the variable
    value_inside.set("Select Subject")

    # Create the optionmenu widget and passing
    # the options_list and value_inside to it.
    question_menu = tk.OptionMenu(root, value_inside, *options_list)
    question_menu.pack()

    # Function to print the submitted option-- testing purpose

    def print_answers():
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shubham@123",
            database="attendance"
        )

        # Create a cursor object
        cursor = db.cursor()

        student_name = name_entry.get()

        cursor.execute(f"SELECT * FROM {value_inside.get()} WHERE name='{student_name}'")

        rows = cursor.fetchall()

        # Clear the existing rows in the Treeview widget
        tree.delete(*tree.get_children())

        # Insert each row from the SQL table into the Treeview widget
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Submit button
    # Whenever we click the submit button, our submitted
    # option is printed ---Testing purpose
    submit_button = tk.Button(root, text='View Attendance', command=print_answers)
    submit_button.pack()

    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5"))

    # Set the headings for the columns
    tree.heading("col1", text="Name")
    tree.heading("col2", text="Department")
    tree.heading("col3", text="Date")
    tree.heading("col4", text="Time")
    tree.heading("col5", text="Subject")

    # Pack the Treeview widget into the window
    tree.pack()

    # Start the main loop to display the window
    root.mainloop()

