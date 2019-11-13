from tkinter import ttk, Frame, Label, Entry, Button, Radiobutton, Scrollbar, Listbox, VERTICAL, filedialog, Tk, IntVar, StringVar
from tkinter.filedialog import asksaveasfile, askdirectory
from past.builtins import apply
from serial.tools import list_ports
from pylsl import resolve_stream

# *** Defining Attributes ***
# Strings
title = "Biomechatronics Data Collection"
header_title = "Biomechatronics Research Group"
style_txt = "clam"
test_id_txt = "Test ID:"
test_format_txt = "Format: Initials_#Test# > Format Example: PRG_#1"
directory_txt = "Click and Select the Root Directory for this test:"
select_dir_txt = "Select Root Directory"
test_info_txt = "Basic Information:"
gender_txt = "Gender:"
age_txt = "Age:"
height_txt = "Height:"
weight_txt = "Weight:"
settings_txt = "Test Settings:"
leg_txt = "Choose Leg:"
leg_act_text = "Type of Motion:"
has_sensor_txt = "Sensor connected:"
start_btn_txt = "Start"
sensor_port_txt = "Select port to Recieve Data From:"
lsl_txt = "Select LSL Stream Name From:"

# Dimensions
dimensions = "800x650"
left_padding = 25
start_font_size = 20

# Fonts
main_font = "Helvetica"
title_font_size = 30
genereal_font_size = 12
scroll_item_height = 5

# Colors
highlight_bg_color = "gray"
label_bg_color = "lightgreen"
selected_item_color = "green"
# *** End of Attributes Definition ***

# *** Global Variables ***
test_id = ""
current_directory = ""
gender = 2 # 1 -> Male, 2 -> Female.
age = -1
height = -1
weight = -1
leg = -1
motion_type = -1
sensor_connected = 2
port_name = ""
lsl_stream_name = ""
# *** End of Global Variables ***

# *** Global Mapping (str, int)
# Choose Gender (Male, Female)
gender_selection = [
    ("Male", 1),
    ("Female", 2),
]

# Choose Right or Left
leg_selection = [
    ("Left Leg", 3),
    ("Right Leg", 4),
]

# Choose Type of Movement, Imagery or Actual Movement
movement_selection = [
    ("Imagery", 5),
    ("Intent", 6),
]

# Will the person use a Sensor, yes or no
sensor_selection = [
    ("Yes", 7),
    ("No", 8),
]
# *** End of Global Mapping ***

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

    # Basic Information
    profile_bar = Frame(window)
    Label(profile_bar, text = test_info_txt , font = (main_font, genereal_font_size, "bold"), 
          padx = left_padding).pack(side = "left")
    profile_bar.pack(side = "top", fill = "x")
    gender_bar = Frame(window)
    gender_bar.pack(side = "top", fill = "x")
    Label(gender_bar, text = gender_txt, padx = left_padding).pack(side = "left")
    var_gender = StringVar()
    var_gender.set(gender_selection[0][1])
    for txt, val in gender_selection:
        Radiobutton(gender_bar, text = txt, variable = var_gender, value = val,
                    command = lambda t = txt, v = var_gender : modify_selection(t, v)).pack(side = "left")

    # Age
    age_bar = Frame(window)
    age_bar.pack(side = "top", fill = "x")
    Label(age_bar, text = age_txt, padx = left_padding).pack(side = "left")
    Entry(age_bar, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side = "left")

    # Height
    height_bar = Frame(window)
    height_bar.pack(side = "top", fill = "x")
    Label(height_bar, text = height_txt, padx = left_padding).pack(side = "left")
    Entry(height_bar, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side = "left")

    # Weight
    weight_bar = Frame(window)
    weight_bar.pack(side = "top", fill = "x")
    Label(weight_bar, text = weight_txt, padx = left_padding).pack(side = "left")
    Entry(weight_bar, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side = "left")

    # Test Settings
    settings = Frame(window)
    settings.pack(side = "top", fill = "x")
    Label(settings, text = settings_txt , font = (main_font, genereal_font_size, "bold"), 
          padx = left_padding).pack(side = "left")

    # Left or Right Leg
    legs = Frame(window)
    legs.pack(side = "top", fill = "x")
    Label(legs, text = leg_txt, padx = left_padding).pack(side = "left")


    # Intent of Movement
    mov = Frame(window)
    mov.pack(side = "top", fill = "x")
    Label(mov, text = leg_act_text, padx = left_padding).pack(side = "left")


    # Sensor
    sensor = Frame(window)
    sensor.pack(side = "top", fill = "x")
    Label(sensor, text = has_sensor_txt, padx = left_padding).pack(side = "left")


    # Function to modify the corresponding global variable whenever a user changes a radio button.
    def modify_selection(text, v):
        value = int(v.get())
        # Note -> This presumes each option will remain binary. In case that changes, this must be updated.
        index = (value - 1) % 2
        
        # Calculate the total number of options.
        max_size = len(gender_selection) + len(leg_selection) + len(movement_selection) + len(sensor_selection)
        
        # Since "sensor" is the last option, value is > than total - len(sensor_selection).
        if value > max_size - len(sensor_selection):
            global sensor_connected
            sensor_connected = sensor_selection[index]
            return

        # Subtract the length of sensor_selection and the remaining is a subproblem 
        # (similar to the original problem, but smaller in size).
        max_size -= len(sensor_selection)
        if value > max_size - len(movement_selection):
            global motion_type
            motion_type = movement_selection[index]
            return
        
        max_size -= len(movement_selection)
        if value > max_size - len(leg_selection):
            global leg
            leg = leg_selection[index]
            return

        max_size -= len(leg_selection)
        if value > max_size - len(gender_selection):
            global gender
            gender = gender_selection[index]
            return

    # Creation of various radio buttons for the options above
    var_leg = IntVar()
    var_leg.set(leg_selection[0][1])
    for txt, val in leg_selection:
        Radiobutton(legs, text = txt, variable = var_leg, value = val,
                    command = lambda t = txt, v = var_leg : modify_selection(t, v)).pack(side = "left")

    var_test = IntVar()
    var_test.set(movement_selection[0][1])
    for txt, val in movement_selection:
        Radiobutton(mov, text = txt, variable = var_test, value = val,
                    command = lambda t = txt, v=var_test : modify_selection(t, v)).pack(side = "left")

    var_sensor = IntVar()
    var_sensor.set(sensor_selection[0][1])
    for txt, val in sensor_selection:
        Radiobutton(sensor, text = txt, variable = var_sensor, value = val,
                    command = lambda t = txt, v = var_sensor : modify_selection(t, v)).pack(side = "left")


    # List of Possible Ports
    port_bar = Frame(window)
    port_bar.pack(side = "top", fill = "x")
    Label(port_bar, text = sensor_port_txt, padx = left_padding).pack(side = "left")
    p_scroll_frame = Frame(window)
    p_scroll_frame.pack(side = "top", fill = "x", padx = left_padding)
    scrollbar = Scrollbar(p_scroll_frame, orient = VERTICAL)
    ports_list = Listbox(p_scroll_frame, bg = label_bg_color, height = scroll_item_height, highlightcolor = selected_item_color,
                  selectbackground = selected_item_color, selectmode = "SINGLE", yscrollcommand = 1)
    
    # TODO -> Add the refresh button and dynamically re-populate the ports_list.
    ports = list(list_ports.comports())
    for i in range(0, len(ports)):
        ports_list.insert(i + 1, ports[i])

    ports_list.pack(side = "left")
    scrollbar.config(command = ports_list.yview)
    scrollbar.pack(side = "left", fill = "y")

    # List of LSL Stream Names
    lsl_bar = Frame(window)
    lsl_bar.pack(side = "top", fill = "x")
    lsl_scroll_frame = Frame(window)
    lsl_scroll_frame.pack(side = "top", fill = "x", padx = left_padding)
    Label(lsl_bar, text = lsl_txt, padx = left_padding).pack(side = "left")
    scrollbar = Scrollbar(lsl_scroll_frame, orient = VERTICAL)

    lsl_list = Listbox(lsl_scroll_frame, bg = label_bg_color, height = scroll_item_height, highlightcolor = selected_item_color,
                  selectbackground = selected_item_color, selectmode = "SINGLE", yscrollcommand = 1)
    
    # TODO -> Add the refresh button and dynamically re-populate the ports_list.
    # TODO -> Make sure the app launches even when there's no LSL stream running.
    lsl_streams = resolve_stream('type', 'EEG')
    for i in range(0, len(lsl_streams)):
        lsl_list.insert(i + 1, lsl_streams[i].name())

    lsl_list.pack(side = "left")
    scrollbar.config(command = lsl_list.yview)
    scrollbar.pack(side = "left", fill = "y")

    # Start Button
    Button(p_scroll_frame, text = start_btn_txt, font = (main_font, start_font_size, "bold"), 
           bg = label_bg_color,fg = "white", padx = left_padding, pady = left_padding, 
           command = start_button).pack()

    # Start GUI loop...
    window.mainloop()

init_window()