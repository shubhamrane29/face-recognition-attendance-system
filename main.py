import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import cv2
from PIL import Image, ImageTk

import os
from datetime import datetime, timedelta
import subprocess

import mysql.connector

import face_cam
import dashboard


class Login_page:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry('1350x800+0+0')
        self.root.configure(bg='black')

        self.var_email = StringVar()
        self.var_password = StringVar()

        frame = Frame(self.root, bg='white')
        frame.place(x=610, y=100, width=340, height=450)

        get_str = Label(frame, text='User Login')
        get_str.place(x=150, y=100)

        # Username
        username = lbl = Label(frame, text='Email Id')
        username.place(x=40, y=150)

        self.txtuser = ttk.Entry(frame)
        self.txtuser.place(x=40, y=175, width=270)

        # Password
        password = lbl = Label(frame, text='Password')
        password.place(x=40, y=210)

        self.txtpass = ttk.Entry(frame)
        self.txtpass.place(x=40, y=235, width=270)

        # Login Button
        loginbtn = Button(frame, text='Login', command=self.login_first)
        loginbtn.place(x=150, y=300)

        # register button
        registerbtn = Button(frame, text='Register', command=self.register)
        registerbtn.place(x=20, y=350)

    def login_first(self):
        if self.txtuser.get() == '' or self.txtpass.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        elif self.txtuser.get() == 'teacher@admin' or self.txtpass.get() == 'Admin@2023':
            open_main = messagebox.askyesno('Admin', 'Access only Admin')
            if open_main > 0:
                self.admin_profile()
            else:
                if not open_main:
                    return
        else:
            conn = mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='Shubham@123',
                                           database='attendance')
            my_cursor = conn.cursor()

            email_input = self.txtuser.get()
            password_input = self.txtpass.get()

            query = "SELECT * FROM register WHERE email=%s AND password=%s"

            my_cursor.execute(query, (email_input, password_input))
            rows = my_cursor.fetchall()
            if len(rows) > 0:
                # dept_wise_attendance_student(email_input)
                dashboard.dept_wise_attendance_student()
            else:
                messagebox.showerror('Error', 'Invalid Username or Password')

            conn.commit()
            conn.close()

    def register(self):
        self.s1 = tk.Toplevel(self.root)
        self.s1.title("Register")
        self.s1.geometry('1350x800+0+0')
        self.s1.configure(bg='black')

        # Create Variables
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_confpass = StringVar()

        frame = Frame(self.s1)
        frame.place(x=250, y=100, width=800, height=550)

        register_lbl = Label(frame, text='REGISTER HERE')
        register_lbl.place(x=50, y=50)

        # Name
        name = Label(frame, text='Full Name')
        name.place(x=50, y=150)

        name_entry = ttk.Entry(frame, textvariable=self.var_name)
        name_entry.place(x=50, y=180, width=250)

        # Email
        email = Label(frame, text='Email')
        email.place(x=370, y=150)

        email_entry = ttk.Entry(frame, textvariable=self.var_email)
        email_entry.place(x=370, y=180, width=250)

        # Password
        password = Label(frame, text='Password')
        password.place(x=50, y=240)

        password_entry = ttk.Entry(frame, textvariable=self.var_password)
        password_entry.place(x=50, y=270, width=250)

        # Confirm Password
        confpass = Label(frame, text='Confirm Password')
        confpass.place(x=370, y=240)

        confpass_entry = ttk.Entry(frame, textvariable=self.var_confpass)
        confpass_entry.place(x=370, y=270, width=250)

        # Register Button
        register_b = Button(frame, text='Next', command=self.register_data)
        register_b.place(x=50, y=320)

    def register_data(self):
        if self.var_name.get() == '' or self.var_password == '':
            messagebox.showerror('Error', 'All fields are required')
        elif self.var_password.get() != self.var_confpass.get():
            messagebox.showerror('Error', 'Password and Confirm Password must be same')
        else:
            conn = mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='Shubham@123',
                                           database='attendance')
            my_cursor = conn.cursor()
            query = ('select * from register where email=%s')
            value = (self.var_email.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row != None:
                messagebox.showerror('Error', 'User with that Email already exists')
                return self.register()
            else:
                my_cursor.execute('insert into register values(%s,%s,%s)', (
                    self.var_name.get(),
                    self.var_email.get(),
                    self.var_password.get(),
                ))
            conn.commit()
            conn.close()
            self.login_teacher()

    def login_teacher(self):
        self.s2 = tk.Toplevel(self.s1)
        self.s2.geometry('1200x520+350+100')
        self.s2.configure(bg='black')

        register_b = tk.Button(self.s2, text='Register', command=self.register_new_user)
        register_b.place(x=1000, y=350, height=50, width=100)

        self.webcam_label = tk.Label(self.s2)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        if name in ['unknown_person', 'no_person_found']:
            messagebox.showinfo('Unknown user', 'User Unknown, Please register yourself or try again')
        else:
            messagebox.showinfo('Welcome back', 'Welcome, {}'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.s2)
        self.register_new_user_window.geometry("1200x520+370+120")
        self.register_new_user_window.configure(bg='black')

        self.accept_button_register_new_user_window = tk.Button(self.register_new_user_window, text = 'Accept', command = self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300, height=50, width=100)

        self.try_again_button_register_new_user_window = tk.Button(self.register_new_user_window, text='Try again', command=self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400, height=50, width=100)

        self.capture_label = tk.Label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.var_name.get()

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        messagebox.showinfo('Success!', 'User was registered successfully!')

        self.register_new_user_window.destroy()

    def admin_teacher(self):
        # Establish a connection to the database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shubham@123",
            database="attendance"
        )

        # Create a cursor object
        cursor = db.cursor()

        # Execute a SELECT query to retrieve the email and password data
        query = "SELECT email, password FROM admin_access"
        cursor.execute(query)

        # Fetch the rows as a list of tuples
        rows = cursor.fetchall()

        # Loop through the rows to check if the entered email and password match any of the rows
        for row in rows:
            if self.txtuser.get() == row[0] and self.txtpass.get() == row[1]:
                # Allow access to the application
                # code here
                break
        else:
            # Display an error message if no match is found
            # code here
            pass

        # Close the cursor and database connection
        cursor.close()
        db.close()

    def admin_profile(self):
        self.s4 = Toplevel(self.root)
        self.s4.geometry('1200x520+350+100')
        self.s4.configure(bg='black')

        attendance_b = tk.Button(self.s4, text='Attendance', bg='white', command=self.choose_department)
        attendance_b.place(x=500, y=200, height=50, width=200)

        stu_attendance_b = tk.Button(self.s4, text='View Student Attendance', bg='white', command=dashboard.dept_wise_attendance)
        stu_attendance_b.place(x=500, y=250, height=50, width=200)

    def choose_department(self):
        self.s5 = Toplevel(self.s4)
        self.s5.geometry('1200x520+350+100')
        self.s5.configure(bg='black')

        IT_b = tk.Button(self.s5, text='IT', bg='white', command=self.choose_it)
        IT_b.place(x=500, y=200, height=50, width=200)

        CSBS_b = tk.Button(self.s5, text='CSBS', bg='white', command=self.choose_csbs)
        CSBS_b.place(x=500, y=250, height=50, width=200)

    def choose_it(self):
        self.s6 = Toplevel(self.s5)
        self.s6.geometry('1200x520+350+100')
        self.s6.configure(bg='black')

        def web_engineering():
            face_cam.face_camera('web_engineering')

        we = tk.Button(self.s6, text='Web Engineering', bg='white', command=web_engineering)
        we.place(x=500, y=50, height=50, width=200)

        def component_engineer():
            face_cam.face_camera('component_engineer')

        ce = tk.Button(self.s6, text='Component Engineer', bg='white', command=component_engineer)
        ce.place(x=500, y=100, height=50, width=200)

        def distributed_computing():
            face_cam.face_camera('distributed_computing')

        dc = tk.Button(self.s6, text='Distributed computing', bg='white', command=distributed_computing)
        dc.place(x=500, y=150, height=50, width=200)

        def advance_tcp():
            face_cam.face_camera('advance_tcp')

        ip = tk.Button(self.s6, text='Advanced TCP/IP', bg='white', command=advance_tcp)
        ip.place(x=500, y=200, height=50, width=200)

        def it_lab():
            face_cam.face_camera('it_lab')

        lab = tk.Button(self.s6, text='IT Lab-V', bg='white', command=it_lab)
        lab.place(x=500, y=250, height=50, width=200)

        def project_stage_2():
            face_cam.face_camera('project_stage_2')

        ps = tk.Button(self.s6, text='Project Stage-2', bg='white', command=project_stage_2)
        ps.place(x=500, y=300, height=50, width=200)

    def choose_csbs(self):
        self.s6 = Toplevel(self.s5)
        self.s6.geometry('1200x520+350+100')
        self.s6.configure(bg='black')

        def operational_management():
            face_cam.face_camera('operational_management')

        oper_manage = tk.Button(self.s6, text='Operational management', bg='white', command=operational_management)
        oper_manage.place(x=500, y=50, height=50, width=200)

        def enterprise_system():
            face_cam.face_camera('enterprise_system')

        es = tk.Button(self.s6, text='Enterprise system', bg='white', command=enterprise_system)
        es.place(x=500, y=100, height=50, width=200)

        def it_project_management():
            face_cam.face_camera('it_project_management')

        project_manage = tk.Button(self.s6, text='IT project management', bg='white', command=it_project_management)
        project_manage.place(x=500, y=150, height=50, width=200)

        def marketing_research():
            face_cam.face_camera('marketing_research')

        market = tk.Button(self.s6, text='Marketing research & management', bg='white', command=marketing_research)
        market.place(x=500, y=200, height=50, width=200)

        def psycology():
            face_cam.face_camera('psycology')

        psy = tk.Button(self.s6, text='Psychology', bg='white', command=psycology)
        psy.place(x=500, y=250, height=50, width=200)

        def image_processing():
            face_cam.face_camera('image_processing')

        img_pro = tk.Button(self.s6, text='Image processing', bg='white', command=image_processing)
        img_pro.place(x=500, y=300, height=50, width=200)

        def seminar():
            face_cam.face_camera('seminar')

        semi = tk.Button(self.s6, text='Seminar', bg='white', command=seminar)
        semi.place(x=500, y=350, height=50, width=200)

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = Login_page()
    app.start()