import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from PIL import ImageTk, Image
import utils

def import_ziku_file():
    ziku_filename_value.set(askopenfilename())
    ziku_display_update()

def ziku_display_update():
    new_filename = ziku_filename_value.get()
    new_page = int(page_control_value.get())
    new_image = ImageTk.PhotoImage(utils.draw_page(new_filename, new_page - 1))
    ziku_display_label.config(image = new_image)
    ziku_display_label.image = new_image

root = tk.Tk()
root.title('字库工具')
root.geometry('800x400')
myFont = Font(size=20)
custom_font = Font(family = 'fonts/kaiti', size = 20)

ziku_import_button = tk.Button(master = root, text = '导入字库', font = custom_font, command = import_ziku_file)
ziku_import_button.grid(row = 0, column = 0)

ziku_filename_value = tk.StringVar(value = '还未导入字库')
ziku_filename_label = tk.Label(master = root, textvariable = ziku_filename_value)
ziku_filename_label.grid(row = 0, column = 1)

page_control_value = tk.StringVar(value = '1')
page_control_spinbox = tk.Spinbox(master = root, from_ = 1, to = 100, increment = 1, textvariable = page_control_value, command = ziku_display_update)
page_control_spinbox.grid(row = 0, column = 2)

ziku_display_image = ImageTk.PhotoImage(Image.new(mode = '1', size = (16 * 50, 16 * 20), color = 255))
ziku_display_label = tk.Label(master = root, image = ziku_display_image)
ziku_display_label.grid(row = 1, column = 0, columnspan = 3)

root.mainloop()