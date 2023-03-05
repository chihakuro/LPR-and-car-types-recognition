# Import library for GUI
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from pathlib import Path

# Import library for model
import os
import time
from ultralytics import YOLO
from rielocr import *
from char import *

# Import library for saving to CSV
import pandas as pd

# Create main window
root = tk.Tk()
root.title("License Plate Recognition")
# set window logo
logo = Path(__file__).with_name('logo.ico')
root.iconbitmap(logo)
root.geometry("1000x500")

# create input and output frames
input_frame = tk.Frame(root, width=500, height=500)
input_frame.pack(side="left", fill="both", expand=True)

output_frame = tk.Frame(root, width=500, height=500)
output_frame.pack(side="right", fill="both", expand=True)

# create black line to separate frames
separator = tk.Frame(root, width=2, bg="black")
separator.place(relx=0.5, rely=0, relheight=1, anchor="n")

# add widgets to input and output frames
bold = ("Calibri", 10, "bold")
normal = ("Calibri", 10)
image_list = []
vehicle_count = 0
license_plate_count = 0
vehicle_prob = []
license_plate_prob = []
license_plate_number = []
input = []
image_date = []
image_time = []
vehicle_type = []
max_array_length = 0

# input area label
input_label = tk.Label(input_frame, text="Input Area", font=bold, anchor="nw", justify="left")
input_label.pack(side="top", padx=10, pady=5, anchor="nw")

# Help button
def help_dialog():
    title = "Help"
    message = "This program is designed to recognize license plate and vehicle type.\n\n" \
              "To use this program, please follow the steps below:\n" \
              "1. Click on the 'Open Images...' button to select the images you want to process.\n" \
              "2. Click on the 'Start Recognition!' button to start the process.\n" \
              "3. Click on the 'Save to CSV!' button to save the results to a CSV file.\n" \
              "Note: You can also use the 'Next >' and '< Previous' buttons to navigate through the images."

    messagebox.showinfo(title, message)

# About button
def about_dialog():
    title = "About Plate Vehicle Recognition"
    message = "This program is designed to recognize license plate and vehicle type.\n\n" \
              "Developed by: Group 5\n" \
              "Version: Patch 1.01 - Release 1.00\n" \
              "Date: February 25, 2023\n" \
              "License: Open Source"

    messagebox.showinfo(title, message)

# open images function
def open_images(): #Can open multiple images at once
    global image_list, image_count, image_number, image, image_tk, image_label, next_button, previous_button, image_number_label, canvas
    # remove current image and its prediction
    try:
        image_label.destroy()
        next_button.destroy()
        previous_button.destroy()
        image_number_label.destroy()
        image_list = []
        image_count = 0
        
    except:
        pass

    # open images
    image_list = filedialog.askopenfilenames(title="Select images", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*")))
    print(image_list)
    
    image_count = len(image_list)
    image_number = 0

    # display first image
    image = Image.open(image_list[image_number])
    image = image.resize((400, 300), Image.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(canvas, image=image_tk)
    image_label.pack()

    # create next and previous buttons
    next_button = tk.Button(input_frame, text="Next >", font=normal, border=2, relief="solid", width=10, height=1, command=next_image)
    next_button.place(relx=0.75, rely=0.8)
    previous_button = tk.Button(input_frame, text="< Previous", font=normal, border=2, relief="solid", width=10, height=1, command=previous_image)
    previous_button.place(relx=0.15, rely=0.8)

    # create current image number of total image count label that updates when next or previous buttons are clicked
    image_number_label = tk.Label(input_frame, text="Image " + str(image_number+1) + " of " + str(image_count), font=normal)
    image_number_label.place(relx=0.45, rely=0.8)

    # update image number label
    def update_image_number_label():
        image_number_label.config(text="Image " + str(image_number+1) + " of " + str(image_count))
        root.after(100, update_image_number_label)
    update_image_number_label()

# next image function
def next_image():
    global image_list, image, image_tk, canvas, image_label, image_number, image_count

    # remove current image
    image_label.destroy()

    # display next image
    image_number += 1
    if image_number == image_count:
        image_number = 0
    image = Image.open(image_list[image_number])
    image = image.resize((400, 300), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(canvas, image=image_tk)
    image_label.pack()

# previous image function
def previous_image():
    global image_list, image, image_tk, canvas, image_label, image_number, image_count

    # remove current image
    image_label.destroy()

    # display previous image
    image_number -= 1
    if image_number == -1:
        image_number = image_count - 1
    image = Image.open(image_list[image_number])
    image = image.resize((400, 300), Image.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(canvas, image=image_tk)
    image_label.pack()

# create menu bar
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open", command=open_images)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

about_menu = tk.Menu(menubar, tearoff=0)
about_menu.add_command(label="Help", command=help_dialog)
about_menu.add_command(label="About", command=about_dialog)
menubar.add_cascade(label="About", menu=about_menu)

root.config(menu=menubar)

# make a "Open Images..." button
open_images_button = tk.Button(input_frame, text="Open Images...", font=normal, border=2, relief="solid", width=20, height=1, command=open_images)
open_images_button.pack(side="top", padx=10, pady=5)

# make a canvas to display images
canvas = tk.Canvas(input_frame, width=400, height=300, bg="white")
canvas.create_text(200, 160, text="No image selected :((", font=normal)
canvas.pack(side="top", padx=30, pady=5)

# start recognition function
def start_recognition():
    global image_list, vehicle_count, license_plate_count, vehicle_prob, license_plate_prob, license_plate_number, input, image_date, image_time, vehicle_type

    # remove the previous output
    try:
        vehicle_count = 0
        license_plate_count = 0
        vehicle_prob = []
        license_plate_prob = []
        license_plate_number = []
        input = []
        image_date = []
        image_time = []
        vehicle_type = []
        overview_text.destroy()
        details_text.destroy()
        progress_bar.destroy()
    except:
        pass

    if len(image_list) == 0:
        messagebox.showerror("Error", "Please select at least one image!")
    else:
        # show progress bar
        progress_bar = ttk.Progressbar(output_frame, orient="horizontal", length=425, mode="determinate")
        progress_bar.place(relx=0.1, rely=0.1)
        progress_bar["maximum"] = 100
        progress_bar["value"] = 0

        # update progress bar
        def update_progress_bar():
            progress_bar["value"] += 40
            if progress_bar["value"] < 100:
                root.after(100, update_progress_bar)
        update_progress_bar()

        # given trained model file 'best.pt' using yolo v8, load model and get number of vehicles and license plates
        for image in image_list:
            input.append(image)
            # resize image to 640x640
            image = Image.open(image)
            image = image.resize((640, 640), Image.Resampling.LANCZOS)
        
        # get best.pt file if it belongs to the same directory as the python file
        m = Path(__file__).with_name('best.pt')
        model = YOLO(m)
        out = model.predict(show=True, source=input, stream=False)
        for result in out:
            for i in result:
                i = i.boxes.boxes
                if i is None:
                    messagebox.showerror("Error", "No vehicle or license plate detected!")
                print(i)
                for j in i:
                    vpb = (j[4]*100).item()
                    vpb = round(vpb, 2)
                    if j[5] == 0:
                        vehicle_count += 1
                        vehicle_type.append('Car')
                        vehicle_prob.append(vpb)

                    elif j[5] == 1:
                        license_plate_count += 1
                        x1, y1, x2, y2 = j[0].item(), j[1].item(), j[2].item(), j[3].item()
                        image = Image.open(image_list[image_number])
                        cropped_image = image.crop((x1, y1, x2, y2))
                        cropped_image.save("cropped_image.jpg")
                        ocr = rielocr("cropped_image.jpg")
                        license_plate_number.append(ocr)
                        license_plate_prob.append(vpb)

                    elif j[5] == 2:
                        vehicle_count += 1
                        vehicle_type.append('Bicycle')
                        vehicle_prob.append(vpb)
                    elif j[5] == 3:
                        vehicle_count += 1
                        vehicle_type.append('Motorbike')
                        vehicle_prob.append(vpb)

        # remove progress bar and show recognition results
        if progress_bar["value"] == 100:
            progress_bar.destroy()
        # show recognition results
        # Overview: number of vehicles, number of license plates
        # Details: Vehicle type, vehicle prediction accuracy, license plate number, license plate number prediction accuracy; repeat details for each vehicle
        # show overview
        overview_label = tk.Label(output_frame, text="Overview", font=bold, anchor="nw", justify="left")
        overview_label.place(relx=0.09, rely=0.2)
        overview_text = tk.Text(output_frame, width=60, height=3, font=normal, border=2, relief="solid")
        overview_text.place(relx=0.1, rely=0.25)
        overview_text.insert("end", "Number of vehicles: " + str(vehicle_count) + "\n")
        overview_text.insert("end", "Number of license plates: " + str(license_plate_count))
        overview_text.config(state="disabled")

        # show details
        details_label = tk.Label(output_frame, text="Details", font=bold, anchor="nw", justify="left")
        details_label.place(relx=0.09, rely=0.4)
        details_text = tk.Text(output_frame, width=60, height=11, font=normal, border=2, relief="solid")
        details_vsb = tk.Scrollbar(output_frame, orient="vertical", command=details_text.yview)
        details_text.configure(yscrollcommand=details_vsb.set)

        # Fill missing values with None
        max_array_length = max(vehicle_count, license_plate_count)

        # Loop through the lists and fill in missing values
        for image in image_list:
            # get image date and time
            image_datem = os.path.getmtime(image)
            image_tim = time.ctime(image_datem)
            t_obj = time.strptime(image_tim)
            imdate = time.strftime("%Y-%m-%d", t_obj)
            image_date.append(imdate)
            imtime = time.strftime("%H-%M-%S", t_obj)
            image_time.append(imtime)

        # Ensure all lists have the same length
        while len(vehicle_type) < max_array_length:
            vehicle_type.append('Unknown')
        while len(vehicle_prob) < max_array_length:
            vehicle_prob.append('0')
        while len(license_plate_number) < max_array_length:
            license_plate_number.append('Unknown')
        while len(license_plate_prob) < max_array_length:
            license_plate_prob.append('0')
        while len(image_date) < max_array_length:
            # replace missing values with date and time of the image which the vehicle or license plate was detected
            image_date.append(image_date[image_number])
            image_time.append(image_time[image_number])

        for i in range(max_array_length):
            details_text.insert("end", "Vehicle type: " + vehicle_type[i] + "\n")
            details_text.insert("end", "Vehicle prediction accuracy: " + str(vehicle_prob[i]) + "%\n")
            details_text.insert("end", "License plate number: " + license_plate_number[i] + "\n")
            details_text.insert("end", "License plate number prediction accuracy: " + str(license_plate_prob[i]) + "%\n")
            details_text.insert("end", "\n")
        details_text.place(relx=0.1, rely=0.45)
        details_vsb.place(relx=0.9, rely=0.45, relheight=0.35)
            
    print(max_array_length)
    print(image_date)
    print(image_time)
    print(vehicle_type)
    print(vehicle_prob)
    print(license_plate_number)
    print(license_plate_prob)
# export results function
def export_results():
    global image_list, vehicle_count, license_plate_count, vehicle_prob, license_plate_prob, license_plate_number, input, image_date, image_time, vehicle_type
    
    # append results to existing file if csv file already exists, otherwise create new csv file
    if os.path.exists(Path(__file__).with_name("results.csv")):
        pd.DataFrame({"Date": image_date, "Time": image_time, "Vehicle Type": vehicle_type, "Vehicle Prediction Accuracy": vehicle_prob, "License Plate Number": license_plate_number, "License Plate Number Prediction Accuracy": license_plate_prob}).to_csv((Path(__file__).with_name('results.csv')), mode="a", header=False, index=False)
    else:
        pd.DataFrame({"Date": image_date, "Time": image_time, "Vehicle Type": vehicle_type, "Vehicle Prediction Accuracy": vehicle_prob, "License Plate Number": license_plate_number, "License Plate Number Prediction Accuracy": license_plate_prob}).to_csv((Path(__file__).with_name('results.csv')), index=False)

    # show message box
    messagebox.showinfo("Export Results", "Results exported to csv file!")


# make a "Start Recognition" button
start_recognition_button = tk.Button(input_frame, text="Start Recognition!", font=normal, border=2, relief="solid", width=20, height=1, command=start_recognition)
start_recognition_button.pack(side="bottom", padx=10, pady=30)

# output area ------------------------------------------------
output_label = tk.Label(output_frame, text="Output Area", font=bold, anchor="nw", justify="left")
output_label.place(relx=0.09, rely=0.01)

# make a "Export Results" button
export_results_button = tk.Button(output_frame, text="Export to csv!", font=normal, border=2, relief="solid", width=20, height=1, command=export_results)
export_results_button.place(relx=0.4, rely=0.89)

root.mainloop()

