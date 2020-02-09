from tkinter import ttk, Frame, Label, Entry, Button, Radiobutton, Scrollbar, Listbox, VERTICAL, filedialog, Tk, IntVar, StringVar
from tkinter.filedialog import asksaveasfile, askdirectory
from past.builtins import apply
from serial.tools import list_ports
from pylsl import resolve_stream
from biostream import BioStream

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
age_txt = "Age: (years)"
height_txt = "Height: (feet'inches: 5'11 or 4'8)"
weight_txt = "Weight: (poinds)"
settings_txt = "Test Settings:"
leg_txt = "Choose Leg:"
leg_act_text = "Type of Motion:"
has_sensor_txt = "Sensor connected:"
start_btn_txt = "Start"
stop_btn_txt = "Stop"  # TODO -> Verify if this will be implemented.
sensor_port_txt = "Select port to Recieve Data From:"
lsl_txt = "Select LSL Stream Name From:"

# Dimensions
dimensions = "800x650"
left_padding = 25
start_font_size = 20
scroll_item_height = 5

# Fonts
main_font = "Helvetica"
title_font_size = 30
genereal_font_size = 12

# Colors
highlight_bg_color = "gray"
label_bg_color = "lightgreen"
selected_item_color = "green"

# Validation Constants
MAX_AGE_LENGTH = 2
MAX_HEIGHT_LENGTH = 4
MAX_WEIGHT_LENGTH = 3
height_proto = "n'nn"
NUMERIC = 'n'
SLASH = '\''

# *** End of Attributes Definition ***

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
    ("None", 5)
]

# Choose Type of Movement, Imagery or Actual Movement
movement_selection = [
    ("Imagery", 6),
    ("Intent", 7),
    ("None", 8),
]

# Will the person use a Sensor, yes or no
sensor_selection = [
    ("Yes", 9),
    ("No", 10),
]
# *** End of Global Mapping ***

# *** Global Variables ***
leg = -1
motion_type = -1
sensor_connected = 2
port_name = ""
lsl_stream_name = ""
test_id_entry = None
age_entry = None
height_entry = None
weight_entry = None
var_gender = None
gender = gender_selection[0]
current_dir = None

# TODO -> Add functionality of start button...
def start_button():
    print("START WAS PRESSED!")
    t_ID = test_id_entry.get()
    c_dir = current_dir.get()
    gend = gender[0]
    age = age_entry.get()
    height = height_entry.get()
    weight = weight_entry.get()
    print(t_ID)
    print(c_dir)
    print(gend)
    print(age)
    print(height)
    print(weight)
    # test_params = validate_params()
    # b_stream = BioStream(test_params)  # TODO -> PASS THE RIGHT ARGUMENTS...
    # b_stream.run_data_collection()  # TODO -> PASS SAMPLES#

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
    global test_id_entry
    test_id_entry = Entry(testID, highlightbackground = highlight_bg_color, bg = label_bg_color)
    test_id_entry.pack(side = "left")
    Label(testID, text = test_format_txt, padx = left_padding).pack(side = "left")

    # Directory Section
    directory = Frame(window)
    directory.pack(side = "top", fill = "x")
    Label(directory, text = directory_txt, padx = left_padding).pack(side = "left")
    global current_dir
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
    global var_gender
    var_gender = StringVar()
    var_gender.set(gender_selection[0][1])
    for txt, val in gender_selection:
        Radiobutton(gender_bar, text = txt, variable = var_gender, value = val,
                    command = lambda t = txt, v = var_gender : modify_selection(t, v)).pack(side = "left")

    # Age
    age_bar = Frame(window)
    age_bar.pack(side = "top", fill = "x")
    Label(age_bar, text = age_txt, padx = left_padding).pack(side = "left")
    
    # Make sure the value of the age entry is a number less than 100.
    def validate_age_input(age_in):
        return len(age_in) == 0 or (age_in.isdigit() and len(age_in) <= MAX_AGE_LENGTH)
    
    validate_age = window.register(validate_age_input)
    global age_entry
    age_entry = Entry(age_bar, validate = "key", validatecommand = (validate_age, "%P"), highlightbackground = highlight_bg_color, bg = label_bg_color)
    age_entry.pack(side = "left")

    # Height
    height_bar = Frame(window)
    height_bar.pack(side = "top", fill = "x")
    Label(height_bar, text = height_txt, padx = left_padding).pack(side = "left")
    
    # Validate if given height input follows the pattern defined above (REFER TO CONSTANTS SECTION).
    def validate_height_input(height_in):
        
        if len(height_in) > MAX_HEIGHT_LENGTH:
            return False
 
        for i in range(0, len(height_in)):
            
            if height_proto[i] == NUMERIC and not height_in[i].isnumeric():
                return False
            
            if height_proto[i] == SLASH and not (height_in[i] == height_proto[i]):
                return False
        
        return True

    validate_height = window.register(validate_height_input)
    global height_entry
    height_entry = Entry(height_bar, validate = "key", validatecommand = (validate_height, "%P"), highlightbackground = highlight_bg_color, bg = label_bg_color)
    height_entry.pack(side = "left")

    # Weight
    weight_bar = Frame(window)
    weight_bar.pack(side = "top", fill = "x")
    Label(weight_bar, text = weight_txt, padx = left_padding).pack(side = "left")
    
    def validate_weight_input(weight_input):
        return len(weight_input) == 0 or (weight_input.isdigit() and len(weight_input) <= MAX_WEIGHT_LENGTH)

    validate_weight = window.register(validate_weight_input)
    global weight_entry
    weight_entry = Entry(weight_bar, validate = "key", validatecommand = (validate_weight, "%P"), highlightbackground = highlight_bg_color, bg = label_bg_color)
    weight_entry.pack(side = "left")

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