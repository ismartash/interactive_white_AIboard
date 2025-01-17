from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import os
import sys
from tkinter import simpledialog
from PyPDF2 import PdfReader
from doubt_db import ScreenAnalyzer
from chatbot import TutorChatBot

root = Tk()
root.title("White Board")
# Make window fullscreen by default
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.config(bg="#f2f3f5")
root.resizable(False, False)


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Calculate canvas size based on screen dimensions
canvas_width = int(screen_width * 0.8)  # 80% of screen width
canvas_height = int(screen_height * 0.8)  # 80% of screen height

# Calculate positions for UI elements
sidebar_width = 60
toolbar_height = 50
canvas_x = sidebar_width + 20
canvas_y = 10

current_x = 0
current_y = 0
start_x = None
start_y = None
color = "black"
active_tool = None

def locate_xy(event):
    global start_x, start_y, current_x, current_y
    start_x, start_y = event.x, event.y
    current_x, current_y = event.x, event.y

def addline(event):
    global current_x, current_y
    if active_tool is None:
        canvas.create_line((current_x, current_y, event.x, event.y), width=int(slider.get()),
                           fill=color, capstyle=ROUND, smooth=True)
        current_x, current_y = event.x, event.y

def insertimage():
    global filename, f_img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="select image file",
                                        filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All file","new.txt")])
    f_img = tk.PhotoImage(file=filename)
    my_img = canvas.create_image(180, 50, image=f_img)
    root.bind("<B3-Motion>", my_callback)

def my_callback(event):
    global f_img
    f_img = tk.PhotoImage(file=filename)
    my_img = canvas.create_image(event.x, event.y, image=f_img)

def add_shape(event):
    global start_x, start_y, active_tool
    if active_tool == "rectangle":
        canvas.create_rectangle(start_x, start_y, event.x, event.y,
                                outline=color, width=int(slider.get()))
    elif active_tool == "oval":
        canvas.create_oval(start_x, start_y, event.x, event.y,
                           outline=color, width=int(slider.get()))
    active_tool = None

def show_color(new_color):
    global color
    color = new_color

def new_canvas():
    canvas.delete('all')
    display_pallete()

def set_eraser():
    global color, active_tool
    active_tool = None
    color = "white"

def set_rectangle_tool():
    global active_tool
    active_tool = "rectangle"

def set_oval_tool():
    global active_tool
    active_tool = "oval"

def display_pallete():
    colors_list = ["black", "gray", "brown4", "red", "orange", "yellow", "green", "blue"]
    for i, color_name in enumerate(colors_list):
        id = colors.create_rectangle((10, 10 + i * 30, 30, 30 + i * 30), fill=color_name)
        colors.tag_bind(id, '<Button-1>', lambda x, col=color_name: show_color(col))

def toggle_chatbot():
    if chatbot_frame.winfo_ismapped():
        chatbot_frame.place_forget()
    else:
        chatbot_frame.place(x=canvas_width + canvas_x +6, y=200, width=300, height=600)

def toggle_chatbotvai():  #visionai button
    if chatbotv_frame.winfo_ismapped():
        chatbotv_frame.place_forget()
    else:
        chatbotv_frame.place(x=canvas_width + canvas_x -300, y=200, width=300, height=600)

def minimize_chatbot():
    chatbot_frame.place_forget()

def minimize_chatbotvai():
    chatbotv_frame.place_forget()

def handle_query():
    query = query_entry.get()
    if query:
        bot = TutorChatBot()
        output = bot.respond(query)
        query_output.config(state='normal')
        query_output.delete("1.0", END)
        query_output.insert(END, output.content)
        query_output.config(state='disabled')

def handlevai_query():
    user_input = query_entryv.get()
    if user_input:
        analyzer = ScreenAnalyzer()
        outputvai = analyzer.analyze_screen(user_input)
        queryv_output.config(state='normal')
        queryv_output.delete("1.0", END)
        queryv_output.insert(END, outputvai)
        queryv_output.config(state='disabled')


color_box = PhotoImage(file=resource_path("icons/color_section.png"))
Label(root, image=color_box, bg='#f2f3f5').place(x=10, y=20)

eraser = PhotoImage(file=resource_path("icons/eraser1.png"))
Button(root, image=eraser, bg="#f2f3f5", command=set_eraser).place(x=30, y=canvas_height - 150)

import_image = PhotoImage(file=resource_path("icons/add_image.png"))
Button(root, image=import_image, bg="white", command=insertimage).place(x=30, y=canvas_height - 100)

colors = Canvas(root, bg="#fff", width=37, height=300, bd=0)
colors.place(x=30, y=60)
display_pallete()

# main Canvas
canvas = Canvas(root, width=canvas_width, height=canvas_height, background="white", cursor="hand2")
canvas.place(x=canvas_x, y=canvas_y)
canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', addline)
canvas.bind('<ButtonRelease-1>', add_shape)

# slider setup
current_value = tk.DoubleVar()

def get_current_value():
    return '{: .2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text=get_current_value())

slider = ttk.Scale(root, from_=1, to=10, orient="horizontal", command=slider_changed, variable=current_value)
slider.place(x=30, y=canvas_height - 40)

value_label = ttk.Label(root, text=get_current_value())
value_label.place(x=27, y=canvas_height - 20)

# chatbot setup
chatbot_icon = PhotoImage(file=resource_path("icons/chatbot.png"))
chatbot_button = Button(
    root,
    image=chatbot_icon,
    command=toggle_chatbot,
    bg="#f2f3f5",
    activebackground="#e1e3e6",
    borderwidth=0,
    cursor="hand2"
)
chatbot_button.place(x=canvas_width + canvas_x - 50, y=canvas_height - 50)


chatbot_frame = Frame(
    root,
    bg="white",
    bd=0,
    highlightthickness=1,
    highlightbackground="#e0e0e0"
)


header_frame = Frame(chatbot_frame, bg="#4a90e2", height=40)
header_frame.pack(fill="x", pady=(0, 10))

Label(
    header_frame,
    text="Chat Assistant",
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 12, "bold")
).pack(side="left", padx=10, pady=8)


Label(
    chatbot_frame,
    text="How can I help you?",
    bg="white",
    fg="#2c3e50",
    font=("Helvetica", 10)
).pack(anchor=W, padx=12, pady=(0, 5))


query_entry = Entry(
    chatbot_frame,
    width=30,
    font=("Helvetica", 11),
    bd=1,
    relief="solid",
    bg="#f8f9fa"
)
query_entry.pack(padx=12, pady=(0, 10))


Button(
    chatbot_frame,
    text="Send Message",
    command=handle_query,
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(pady=(0, 10))

# chat output area with frame
output_frame = Frame(chatbot_frame, bg="#f8f9fa", padx=2, pady=2)
output_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

query_output = Text(
    output_frame,
    height=25,
    width=35,
    font=("Helvetica", 10),
    state='disabled',
    bg="#f8f9fa",
    relief="flat",
    padx=8,
    pady=8
)
query_output.pack(fill="both", expand=True)

# added scrollbar
scrollbar = Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")
query_output.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=query_output.yview)

#minimize button
minimize_button = Button(
    header_frame,
    text="−",
    command=minimize_chatbot,
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 16),
    relief="flat",
    bd=0,
    cursor="hand2"
)
minimize_button.pack(side="right", padx=10)

# Hover effects
def on_enter(e):
    e.widget['background'] = '#357abd'

def on_leave(e):
    e.widget['background'] = '#4a90e2'

# add hover effects to buttons
for button in chatbot_frame.winfo_children():
    if isinstance(button, Button) and button['bg'] == '#4a90e2':
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

# document upload setup
document_icon = PhotoImage(file=resource_path("icons/document_icon.png"))
document_button = Button(root, image=document_icon, bg="#f2f3f5", borderwidth=0)
document_button.place(x=canvas_width + canvas_x - 300, y=canvas_height - 50)

# ask doubt part
# Create a modern-looking Ask Doubt button
doubt_button = Button(root, 
    text="Ask doubt ✋", 
    command=toggle_chatbotvai,
    font=("Helvetica", 11, "bold"),
    bg="#4a90e2",  # Modern blue color
    fg="white",
    relief="flat",
    padx=15,
    pady=8,
    cursor="hand2"
).place(x=canvas_width + canvas_x - 500, y=canvas_height - 50)

chatbotv_frame = Frame(
    root, 
    bg="#ffffff",
    bd=0,
    highlightthickness=1,
    highlightbackground="#e0e0e0"
)


header_frame = Frame(chatbotv_frame, bg="#4a90e2", height=40)
header_frame.pack(fill="x", pady=(0, 10))

Label(
    header_frame, 
    text="Visual Query Assistant",
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 12, "bold")
).pack(side="left", padx=10, pady=8)


Label(
    chatbotv_frame,
    text="ask query about visual",
    bg="white",
    fg="#2c3e50",
    font=("Helvetica", 10)
).pack(anchor=W, padx=12, pady=(0, 5))

query_entryv = Entry(
    chatbotv_frame,
    width=30,
    font=("Helvetica", 11),
    bd=1,
    relief="solid",
    bg="#f8f9fa"
)
query_entryv.pack(padx=12, pady=(0, 10))
Button(
    chatbotv_frame,
    text="Submit Query",
    command=handlevai_query,
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5,
    cursor="hand2"
).pack(pady=(0, 10))


output_frame = Frame(chatbotv_frame, bg="#f8f9fa", padx=2, pady=2)
output_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

queryv_output = Text(
    output_frame,
    height=25,
    width=30,
    font=("Helvetica", 10),
    state='disabled',
    bg="#f8f9fa",
    relief="flat",
    padx=8,
    pady=8
)
queryv_output.pack(fill="both", expand=True)

#scrollbar for output
scrollbar = Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")
queryv_output.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=queryv_output.yview)

# modern minimize button
minimize_buttonv = Button(
    header_frame,
    text="−",
    command=minimize_chatbotvai,
    bg="#4a90e2",
    fg="white",
    font=("Helvetica", 16),
    relief="flat",
    bd=0,
    cursor="hand2"
)
minimize_buttonv.pack(side="right", padx=10)

# add hover effects for buttons
def on_enter(e):
    e.widget['background'] = '#357abd'

def on_leave(e):
    e.widget['background'] = '#4a90e2'

# Bind hover events to all blue buttons
for button in chatbotv_frame.winfo_children():
    if isinstance(button, Button) and button['bg'] == '#4a90e2':
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

def on_canvas_click(event):
    global active_tool
    if active_tool == "text":
        text = simpledialog.askstring("Input", "Enter text:")
        if text:
            canvas.create_text(event.x, event.y, text=text, fill=color, font=("Arial", int(slider.get()) * 5))
        active_tool = None

def set_text_tool():
    global active_tool
    active_tool = "text"

# slides handling
slides = []
current_slide = 0

def insert_document():
    global slides, current_slide
    file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select Document",
        filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not file_path:
        return
    
    slides = []
    current_slide = 0

    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        slides = [page.extract_text() for page in reader.pages]
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            slides = file.read().split('\n\n')
    
    if slides:
        display_slide()

def display_slide():
    global slides, current_slide
    if 0 <= current_slide < len(slides):
        canvas.delete('all')
        display_pallete()
        
        slide_text = slides[current_slide]
        canvas.create_text(
            10, 10,
            anchor=NW,
            text=slide_text,
            font=("Arial", 12),
            fill="black",
            width=canvas_width - 20
        )

def next_slide():
    global current_slide
    if current_slide < len(slides) - 1:
        current_slide += 1
        display_slide()

def previous_slide():
    global current_slide
    if current_slide > 0:
        current_slide -= 1
        display_slide()

document_button.config(command=insert_document)

# Bottom toolbar buttons
toolbar_y = canvas_height - 50
Button(root, text="Previous", command=previous_slide, font=("Arial", 10), bg="#f2f3f5").place(x=canvas_x + canvas_width - 700, y=toolbar_y)
Button(root, text="Next", command=next_slide, font=("Arial", 10), bg="#f2f3f5").place(x=canvas_x + canvas_width - 625, y=toolbar_y)
Button(root, text="Text", bg="#f2f3f5", command=set_text_tool, font=("Arial", 10), width=10).place(x=canvas_x + 300, y=toolbar_y)
Button(root, text="Rectangle", bg="#f2f3f5", command=set_rectangle_tool, font=("Arial", 10), width=10).place(x=canvas_x + 100, y=toolbar_y)
Button(root, text="Oval", bg="#f2f3f5", command=set_oval_tool, font=("Arial", 10), width=10).place(x=canvas_x + 200, y=toolbar_y)
Button(root, text="Clear Screen", bg="#f2f3f5", command=new_canvas, font=("Arial", 10), width=15).place(x=canvas_x + 400, y=toolbar_y)

canvas.bind('<Button-1>', lambda event: on_canvas_click(event) if active_tool == "text" else locate_xy(event))
canvas.bind('<ButtonRelease-1>', add_shape)

root.mainloop()