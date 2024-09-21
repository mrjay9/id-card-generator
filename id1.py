from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import re
from datetime import datetime

class ID_Card_Generator:
    def __init__(self, root):
        # Window settings
        root.geometry("1000x600+200+50")
        root.title("ID Card Generator")
        root.resizable(False, False)
        
        # Title Label
        title = Label(root, text="ID CARD GENERATOR", font=("times new roman", 38), bg='#272dd6', fg="white")
        title.place(x=0, y=0, relwidth=1)

        # Variables to hold user input and photo path
        self.var_student_id = StringVar()
        self.var_student_name = StringVar()
        self.var_student_dept = StringVar()
        self.var_student_session = StringVar()
        self.var_student_dob = StringVar()
        self.var_student_mobile = StringVar()
        self.photo_path = ""

        # Frame for input details
        det_Frame = Frame(root, bd=2, relief=RIDGE, bg="white")
        det_Frame.place(x=50, y=100, width=500, height=460)
        
        # Section title in the input frame
        Label(det_Frame, text="Enter Details", font=("goudy old style", 20, "bold"), bg='#013246', fg="white").place(x=0, y=0, relwidth=1)
        
        # Labels for input fields
        labels = ["Name", "Roll no.", "Course/Branch", "Session", "D.O.B.", "Mobile No."]
        for i, text in enumerate(labels):
            Label(det_Frame, text=text, font=("times new roman", 15, 'bold')).place(x=20, y=60 + i * 40)

        # Text fields for user input
        self.txt_student_id = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_id, bg="lightyellow")
        self.txt_student_id.place(x=200, y=60)

        self.txt_student_name = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_name, bg="lightyellow")
        self.txt_student_name.place(x=200, y=100)
        # Validate numeric input for roll number
        self.txt_student_name.config(validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))

        self.txt_student_dept = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_dept, bg="lightyellow")
        self.txt_student_dept.place(x=200, y=140)

        self.txt_student_session = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_session, bg="lightyellow")
        self.txt_student_session.place(x=200, y=180)

        self.txt_student_dob = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_dob, bg="lightyellow")
        self.txt_student_dob.place(x=200, y=220)

        self.txt_student_mobile = Entry(det_Frame, font=("times new roman", 15, 'bold'), textvariable=self.var_student_mobile, bg="lightyellow")
        self.txt_student_mobile.place(x=200, y=260)
        # Validate numeric input for mobile number
        self.txt_student_mobile.config(validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))

        # Buttons for generating and clearing ID cards
        Button(det_Frame, text="Generate ID", command=self.generate, font=("times new roman", 18, 'bold'), bg="#2eb82e", fg="white").place(x=210, y=340, width=180, height=30)
        Button(det_Frame, text="Clear", command=self.clear, font=("times new roman", 18, 'bold'), bg="#ff1a1a", fg="black").place(x=332, y=300, width=120, height=28)

        # Label for status messages
        self.lbl_msg = Label(det_Frame, font=("times new roman", 20), bg="white")
        self.lbl_msg.place(x=0, y=400, relwidth=1)

        # Frame for displaying the generated ID card
        self.card_Frame = Frame(root, bd=2, relief=RIDGE, bg="white")
        self.card_Frame.place(x=600, y=100, width=320, height=260)
        # ID Card title
        Label(self.card_Frame, text="Student ID Card", font=("goudy old style", 17, "bold"), bg='#013246', fg="white").place(x=0, y=0, relwidth=1)

        # Label to show the generated ID card image
        self.card_image = Label(self.card_Frame, bg='white')
        self.card_image.place(x=10, y=30, width=300, height=220)

        # Button to upload a photo
        Button(root, text="Upload Photo", command=self.upload_photo, font=("times new roman", 17, 'bold'), bg="#607d8b", fg="white").place(x=185, y=402, width=170, height=28)

    # Validation function for numeric inputs
    def validate_numeric(self, value):
        return value.isdigit() or value == ""

    # Validation function for session format
    def validate_session(self, value):
        return re.match(r'^\d{4}-\d{4}$', value) is not None

    # Validation function for date format
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    # Function to clear all fields and ID card display
    def clear(self):
        self.var_student_id.set('')
        self.var_student_name.set('')
        self.var_student_dept.set('')
        self.var_student_session.set('')
        self.var_student_dob.set('')
        self.var_student_mobile.set('')
        self.card_image.config(image='')
        self.lbl_msg.config(text="")
        self.txt_student_id.focus()

    # Function to upload a photo for the ID card
    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.photo_path = file_path

    # Function to generate the ID card
    def generate(self):
        # Validate input fields
        if not all([self.var_student_id.get(), self.var_student_name.get(), self.var_student_dept.get(), self.var_student_session.get(), self.var_student_dob.get(), self.var_student_mobile.get()]):
            self.lbl_msg.config(text="Please Enter All Details !!", fg="red")
        elif not self.validate_date(self.var_student_dob.get()):
            messagebox.showerror("Invalid Date", "Please enter the date in DD/MM/YYYY format.")
        elif not self.validate_session(self.var_student_session.get()):
            messagebox.showerror("Invalid Session", "Please enter the session in YYYY-YYYY format.")
        else:
            # Create a new ID card image
            id_card_width, id_card_height = 320, 220
            card_image = Image.new('RGB', (id_card_width, id_card_height), color='white')
            draw = ImageDraw.Draw(card_image)
            
            # Draw card borders and title
            draw.rectangle([(10, 10), (id_card_width-10, id_card_height-10)], outline='black', width=2)
            draw.rectangle([(0, 0), (id_card_width, 30)], fill='#013246')
            
            # Add photo if available
            if self.photo_path:
                photo = Image.open(self.photo_path)
                photo = photo.resize((90, 120), Image.Resampling.LANCZOS)
                photo_x, photo_y = 15, 40
                draw.rectangle([(photo_x - 1, photo_y - 1), (photo_x + 90 + 1, photo_y + 120 + 1)], outline='black', width=1)
                card_image.paste(photo, (photo_x, photo_y))

            # Define fonts for text
            font_title = ImageFont.truetype("arial.ttf", 18)
            font_text = ImageFont.truetype("arial.ttf", 12)
            font_hod = ImageFont.truetype("arial.ttf", 10)

            # Add text details to the card
            draw.text((120, 10), "Student ID Card", font=font_title, fill='white')
            details = [
                f"Name:  {self.var_student_id.get()}",
                f"Roll no.:  {self.var_student_name.get()}",
                f"Course/Branch:  {self.var_student_dept.get()}",
                f"Session:  {self.var_student_session.get()}",
                f"D.O.B.:  {self.var_student_dob.get()}",
                f"Mobile No.:  {self.var_student_mobile.get()}"
            ]
            for i, detail in enumerate(details):
                draw.text((120, 50 + i * 20), detail, font=font_text, fill='black')

            # Add signature lines
            draw.text((242, id_card_height - 42), "Sign. of HOD", font=font_hod, fill='black')
            draw.text((20, id_card_height - 42), "Sign. of Campus Director", font=font_hod, fill='black')

            # Save the generated ID card
            if not os.path.exists("ID_CARDS"):
                os.makedirs("ID_CARDS")
            id_card_path = f"ID_CARDS/student_{self.var_student_name.get()}.png"
            card_image.save(id_card_path)

            # Display the generated ID card
            self.im = ImageTk.PhotoImage(card_image)
            self.card_image.config(image=self.im)
            self.lbl_msg.config(text="ID Card Generated Successfully !!", fg="green")

# Create and run the application
root = Tk()
ID_Card_Generator(root)
root.mainloop()
