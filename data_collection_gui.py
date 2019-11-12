from tkinter import ttk, Frame, Label, Entry, Button, Radiobutton, Scrollbar, Listbox, VERTICAL, filedialog, Tk, IntVar, StringVar
from tkinter.filedialog import asksaveasfile, askdirectory
from past.builtins import apply

# *** Defining Attributes ***
# Strings
title = "Biomechatronics Data Collection"
header_title = "Biomechatronics Research Group"
style_txt = "clam"
test_id_txt = "Test ID:"
test_format_txt = "Format: Initials_#Test# > Format Example: PRG_#1"
directory_txt = "Click and Select the Root Directory for this test:"
select_dir_txt = "Select Root Directory"

# Dimensions
dimensions = "800x650"
left_padding = 25

# Fonts
main_font = "Helvetica"
title_font_size = 30
genereal_font_size = 12

# Colors
highlight_bg_color = "gray"
label_bg_color = "lightgreen"
selected_item_color = "green"
# *** End of Attributes Definition ***

# Global Variables

# TODO -> Add functionality of start button...
def start_button():
    print("START WAS PRESSED!")

def init_window():
    # Init program window...
    window = Tk()
    window.title(title)
    window.geometry(dimensions)
    style = ttk.Style()
    style.theme_use(style_txt)

    # Header Section
    header = Frame(window)
    header.pack(side = "top", fill = "x")
    Label(header,  text= header_title, font=(main_font, title_font_size, "bold")).pack()

    # Test ID
    testID = Frame(window)
    testID.pack(side = "top", fill = "x")
    Label(testID, text = test_id_txt, font = (main_font, genereal_font_size, "bold"), 
          padx = left_padding).pack(side = "left")
    Entry(testID, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side = "left")
    Label(testID, text = test_format_txt, padx = left_padding).pack(side = "left")

    # Directory Section
    directory = Frame(window)
    directory.pack(side = "top", fill = "x")
    Label(directory, text = directory_txt, padx = left_padding).pack(side = "left")
    current_dir = StringVar()
    current_dir_label = Label(directory, textvariable = current_dir)

    # Save Directory Button will Select folder and Get Folder's Path
    def mfileopen():
        current_dir.set(askdirectory())
        
    Button(directory, text = select_dir_txt, command = mfileopen).pack(side = "left")
    current_dir_label.pack(side = "left")

#Basic Information
    profile = Frame(window)
    Label(profile, text= "     Basic Information:" , font=(main_font, genereal_font_size, "bold")).pack(side = "left")
    profile.pack(side="top", fill="x")
    profile3 = Frame(window)
    profile3.pack(side="top", fill="x")
    Label(profile3, text="     Gender: ").pack(side="left")
    gender = 0
    Radiobutton(profile3, text="Male", variable=gender, value=1).pack(side="left")
    Radiobutton(profile3, text="Female", variable=gender, value=2).pack(side="left")


#Age
    profile2 = Frame(window)
    profile2.pack(side="top", fill="x")
    Label(profile2, text="     Age:       ").pack(side="left")
    Entry(profile2, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side="left")


#Height
    profile2 = Frame(window)
    profile2.pack(side="top", fill="x")
    Label(profile2, text="     Height:  ").pack(side="left")
    Entry(profile2, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side="left")


#Weight
    profile2 = Frame(window)
    profile2.pack(side="top", fill="x")
    Label(profile2, text="     Weight: ").pack(side="left")
    Entry(profile2, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side="left")

#Test Settings
    settings = Frame(window)
    settings.pack(side="top", fill="x")
    Label(settings, text="    Test Settings: " , font=(main_font, genereal_font_size, "bold")).pack(side="left")


#Left or Right Leg
    legs = Frame(window)
    legs.pack(side="top", fill="x")
    Label(legs, text="     Choose Leg:      ").pack(side="left")


#Intent of Movement
    mov = Frame(window)
    mov.pack(side="top", fill="x")
    Label(mov, text="     Type of Action: ").pack(side="left")


#Sensor
    sensor = Frame(window)
    sensor.pack(side="top", fill="x")
    Label(sensor, text="     Sensor or Not:   ").pack(side="left")

    #Choose Right or Left
    legSelection = [
        ("Right Leg   ", 1),
        ("Left Leg   ", 2),
    ]

    #Choose Type of Movement, Imagery or Actual Movement
    movementSelection = [
        ("Movement", 3),
        ("Intent   ", 4),
    ]

    #Will the person use a Sensor, yes or no
    sensorSelection = [
        ("WithSensor", 5),
        ("WithoutSensor", 6),
    ]


#Creation of various radio buttons for the options above
    def ShowChoice(text, v):
        print(text, v.get())

    gender = IntVar()
    gender.set(legSelection[0][1])

    for txt, val in legSelection:
        Radiobutton(legs, text=txt, variable=gender, value=val,
                       command=lambda t=txt, v=gender: ShowChoice(t, v)).pack(side="left")

    vartest = IntVar()
    vartest.set(movementSelection[0][1])

    for txt, val in movementSelection:
        Radiobutton(mov, text=txt, variable=vartest, value=val,
                       command=lambda t=txt, v=vartest: ShowChoice(t, v)).pack(side="left")

    varSensor = IntVar()
    varSensor.set(sensorSelection[0][1])

    for txt, val in sensorSelection:
        Radiobutton(sensor, text=txt, variable=varSensor, value=val,
                       command=lambda t=txt, v=varSensor: ShowChoice(t, v)).pack(side="left")


#List of Possible Ports
    listBoxSide = Frame(window)
    listBoxSide.pack(side="top", fill="x")
    listBoxSide2 = Frame(window)
    listBoxSide2.pack(side="top", fill="x")
    Label(listBoxSide, text= '\n' + "     Select port to Recieve Data From: ").pack(side="left")
    Label(listBoxSide2, text= "     " ).pack(side="left")
    Label(listBoxSide2, text="                            ").pack(side="right")
    scrollbar = Scrollbar(listBoxSide2, orient=VERTICAL)
    Lb1 = Listbox(listBoxSide2, bg = label_bg_color, height = 5, highlightcolor = selected_item_color,
                  selectbackground = selected_item_color, selectmode = "SINGLE", yscrollcommand = 1)
    Lb1.insert(1, "PORT1")
    Lb1.insert(2, "PORT2")
    Lb1.insert(3, "PORT3")
    Lb1.insert(4, "PORT4")
    Lb1.insert(5, "PORT5")
    Lb1.insert(6, "PORT6")
    Lb1.insert(7, "PORT7")
    Lb1.insert(8, "PORT8")
    Lb1.pack(side = "left")
    scrollbar.config(command=Lb1.yview)
    scrollbar.pack(side="left", fill="y")



    # List of LSL Stream Names???
    listBoxSide3 = Frame(window)
    listBoxSide3.pack(side="top", fill="x")
    listBoxSide4 = Frame(window)
    listBoxSide4.pack(side="top", fill="x")
    Label(listBoxSide3, text= '\n' + "     LSL Stream Name From: ").pack(side="left")
    Label(listBoxSide4, text= "     " ).pack(side="left")
    scrollbar = Scrollbar(listBoxSide4, orient=VERTICAL)
    Lb2 = Listbox(listBoxSide4, bg = label_bg_color, height = 5, highlightcolor = selected_item_color,
                  selectbackground = selected_item_color, selectmode = "SINGLE", yscrollcommand = 1)
    Lb2.insert(1, "STREAM_NAME_1")
    Lb2.insert(2, "STREAM_NAME_2")
    Lb2.insert(3, "STREAM_NAME_3")
    Lb2.insert(4, "STREAM_NAME_4")
    Lb2.insert(5, "STREAM_NAME_5")
    Lb2.insert(6, "STREAM_NAME_6")
    Lb2.insert(7, "STREAM_NAME_7")
    Lb2.insert(8, "STREAM_NAME_8")
    Lb2.pack(side = "left")
    scrollbar.config(command=Lb2.yview)
    scrollbar.pack(side="left", fill="y")

    # Start Button
    Button(listBoxSide2, text="Start", font=(main_font, 20, "bold") , bg=label_bg_color,fg="white", 
        padx = 20, pady = 20, command = start_button).pack()

    # Start GUI loop...
    window.mainloop()

init_window()