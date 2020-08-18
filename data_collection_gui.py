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
height_txt = "Height: (foot-inches)"
weight_txt = "Weight: (pounds)"
settings_txt = "Test Settings:"
leg_txt = "Choose Leg:"
leg_act_text = "Type of Motion:"
has_sensor_txt = "Sensor connected:"
start_btn_txt = "Start"
stop_btn_txt = "Stop"  # TODO -> Verify if this will be implemented.
sensor_port_txt = "Select port to Recieve Data From:"
lsl_txt = "Select LSL Stream Name From:"
direction_txt = "Direction of Movement:"
hairlength_txt = "Hair Length:"
environment_txt = "Type of Environment:"
circumference_txt = "Head Circumference: (foot-inches)"
density_txt = "Hair Density:"
position_txt = "Measurement Position:"

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
]

# Choose Type of Movement, Imagery or Actual Movement
movement_selection = [
    ("Imagery", 5),
    ("Intent", 6),
    ("None", 8),
]

# Will the person use a Sensor, yes or no
sensor_selection = [
    ("Yes", 9),
    ("No", 10),
]

# Choose Direction of Movement, Up, Down, Standing...
direction_selection = [
    ("Up", 11),
    ("Down", 12),
    ("Standing", 13),
]
# Choose Hair Length, bald, short,medium, long
hairlength_selection = [
    ("Bald", 14),
    ("Short", 15),
    ("Medium", 16),
    ("Long",17),
]
# Choose Environment, quiet, moderately loud, loud 
environment_selection = [
    ("Quiet", 18),
    ("Moderately Loud", 19),
    ("Loud", 20),
]
# Choose Hair Density, [...expand...]
density_selection = [
    ("Light", 21),
    ("Medium", 22),
    ("Heavy", 23),
]
# Choose Measurement Position
position_selection = [
    ("Standing", 24),
    ("Sitting", 25),
]
#

# 

#
# Gonna add: type of mov (is this different from the one we have?), head circ., hair length, hair density, environment -H[del coemment]
# [add here...]
#
# type of mov (up/down/standing, etc...)-select (not the same)
#head circumference (entry)
#Hair Length Select
#Hair Densiry standby
#Environment - select, loud or whatever. quiet. 



# *** End of Global Mapping ***

# *** Global Variables ***
height = -1
weight = -1
leg = -1
motion_type = -1
sensor_connected = 2
port_name = ""
lsl_stream_name = ""
test_id_entry = None
age_entry = None
var_gender = None
gender = gender_selection[0]
current_dir = None
#add by H
circumference = -1
var_density = -1
direction_sel = -1
environment_sel = -1
hairlength_sel = -1
density_sel = -1
position_sel = -1


# TODO -> Add functionality of start button...
def start_button():
    print("START WAS PRESSED!")
    t_ID = test_id_entry.get()
    c_dir = current_dir.get()
    gend = gender[0]
    age = age_entry.get()
    print(t_ID)
    print(c_dir)
    print(gend)
    print(age)
    # test_params = validate_params()
    # b_stream = BioStream(test_params)  # TODO -> PASS THE RIGHT ARGUMENTS...
    # b_stream.run_data_collection()  # TODO -> PASS SAMPLES#
    #HERBERT ADD HERE: test the inputs by adding as above
    

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
    global age_entry
    age_entry = Entry(age_bar, highlightbackground = highlight_bg_color, bg = label_bg_color)
    age_entry.pack(side = "left")

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

    #added by H
    # Direction of Movement
    direction = Frame(window)
    direction.pack(side = "top", fill = "x")
    Label(direction, text = direction_txt, padx = left_padding).pack(side = "left")

     # Length of Hair
    hairlength = Frame(window)
    hairlength.pack(side = "top", fill = "x")
    Label(hairlength, text = hairlength_txt, padx = left_padding).pack(side = "left")

     # Type of Environment
    environment = Frame(window)
    environment.pack(side = "top", fill = "x")
    Label(environment, text = environment_txt, padx = left_padding).pack(side = "left")

    # Density of Hair
    density = Frame(window)
    density.pack(side = "top", fill = "x")
    Label( density, text = density_txt, padx = left_padding).pack(side = "left")


    # Head Circumference
    circumference_bar = Frame(window)
    circumference_bar.pack(side = "top", fill = "x")
    Label(circumference_bar, text = circumference_txt, padx = left_padding).pack(side = "left")
    Entry(circumference_bar, highlightbackground = highlight_bg_color, bg = label_bg_color).pack(side = "left")

    # Measurement Position
    position = Frame(window)
    position.pack(side = "top", fill = "x")
    Label(position, text = position_txt, padx = left_padding).pack(side = "left")


    # Function to modify the corresponding global variable whenever a user changes a radio button.
    def modify_selection(text, v):
        value = int(v.get())
        # Note -> This presumes each option will remain binary. In case that changes, this must be updated.
        index = (value - 1) % 2
        
        # Calculate the total number of options.
        max_size = len(gender_selection) + len(leg_selection) + len(movement_selection) + len(sensor_selection) + len(direction_selection) + len(hairlength_selection) + len(environment_selection) + len(density_selection) + len(position_selection)
        
        # Since "sensor" is the last option, value is > than total - len(sensor_selection).
        if value > max_size - len(position_selection):
            global position_sel
            position_sel = position_selection[index]
            return

        # Subtract the length of sensor_selection and the remaining is a subproblem 
        # (similar to the original problem, but smaller in size).
        max_size -= len(position_selection)
        if value > max_size - len(density_selection):
            global density_sel
            density_sel = density_selection[index]
            return
        
        max_size -= len(density_selection)
        if value > max_size - len(environment_selection):
            global environment_sel
            environment_sel = environment_selection[index]
            return

        max_size -= len(environment_selection)
        if value > max_size - len(hairlength_selection):
            global hairlength_sel
            hairlength_sel = hairlength_selection[index]
            return
        
        max_size -= len(hairlength_selection)
        if value > max_size - len(direction_selection):
            global direction_sel
            direction_sel = direction_selection[index]
            return

        max_size -= len(direction_selection)
        if value > max_size - len(sensor_selection):
            global sensor_connected
            sensor_connected = sensor_selection[index]
            return

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
#################################################################
        
       
       
        
        


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

    var_dir = IntVar()
    var_dir.set(direction_selection[0][1])
    for txt, val in direction_selection:
        Radiobutton(direction, text = txt, variable = var_dir, value = val,
                    command = lambda t = txt, v = var_dir : modify_selection(t, v)).pack(side = "left")

    var_hairlength = IntVar()
    var_hairlength.set(hairlength_selection[0][1])
    for txt, val in hairlength_selection:
        Radiobutton(hairlength, text = txt, variable = var_hairlength, value = val,
                    command = lambda t = txt, v = var_hairlength : modify_selection(t, v)).pack(side = "left")

    var_env = IntVar()
    var_env.set(environment_selection[0][1])
    for txt, val in environment_selection:
        Radiobutton(environment, text = txt, variable = var_env, value = val,
                    command = lambda t = txt, v = var_env : modify_selection(t, v)).pack(side = "left")     

    var_density = IntVar()
    var_density.set(density_selection[0][1])
    for txt, val in density_selection:
        Radiobutton(density, text = txt, variable = var_density, value = val,
                    command = lambda t = txt, v = var_density : modify_selection(t, v)).pack(side = "left")

    var_position = IntVar()
    var_position.set(position_selection[0][1])
    for txt, val in position_selection:
        Radiobutton(position, text = txt, variable = var_position, value = val,
                    command = lambda t = txt, v = var_position : modify_selection(t, v)).pack(side = "left")

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