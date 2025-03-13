import os
import tkinter as tk
import subprocess
import sys
import shutil
from pathlib import Path
from tkinter import filedialog, simpledialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

MAX_BG_SIZE = (1600, 1000)

def create_preview():
    global preview_label, background_path, font_path
    try: 

        margin_left = int(left_entry.get())
        margin_top = int(top_entry.get())
        margin_right = int(right_entry.get())
        margin_bottom = int(bottom_entry.get())
        line_spacing = int(line_spacing_entry.get())
        font_size = int(font_size_entry.get())
        text = text_input.get("1.0", tk.END).strip()

        if background_path:
            background = Image.open(background_path).copy()
            background.thumbnail(MAX_BG_SIZE, Image.LANCZOS)
        else:
            background = Image.new("RGB", (100, 100), "white")

        draw = ImageDraw.Draw(background)

        if font_path:
            font = ImageFont.truetype(font_path, size=font_size)
            max_width = background.width - (margin_left + margin_right)
            lines = []
            for line in text.split("\n"):
                words = line.split(" ")
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if font.getbbox(test_line)[2] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)

            text_y = margin_top
            for line in lines:
                draw.text((margin_left, text_y), line, font=font, fill="black")
                text_y += font.getbbox(line)[3] + line_spacing

        img_tk = ImageTk.PhotoImage(background)
        preview_label.config(image=img_tk)
        preview_label.image = img_tk
    except Exception as e:
        print("Піздєц знову помилка блять:", e)

def on_input_change(event):
    create_preview()


def select_background():
    global background_path, background_label
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png")])
    if file_path:
        background_path = file_path
        background_label.config(text=f"Обраний фон: {os.path.basename(file_path)}")
        create_preview()
    return file_path

def select_font():
    global font_path, font_label
    file_path = filedialog.askopenfilename(filetypes=[("Fonts", "*.ttf;*.otf")])
    if file_path:
        font_path = file_path
        font_label.config(text=f"Обраний шрифт: {os.path.basename(file_path)}")
        create_preview()
    return file_path


def open_folder_in_default_manager(folder_path=None):
    if folder_path is None:
        folder_path = Path.home()

    if sys.platform == "win32":
        os.startfile(folder_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", folder_path])
    else:
        try:
            if default_file_manager and ".desktop" in default_file_manager:
             file_manager = default_file_manager.replace(".desktop", "")
             if shutil.which(file_manager):
              subprocess.run([file_manager, folder_path])
              return

        except Exception:
            pass
        subprocess.run(["xdg-open", folder_path])

def generate_text_on_image():
    global background_path, font_path
    if not background_path:
        background_path = select_background()
    if not background_path:
        return
    if not font_path:
        font_path = select_font()
    if not font_path:
        return
    output_dir = "output_pages"
    os.makedirs(output_dir,exist_ok=True)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        text = text_input.get("1.0", tk.END).strip()
        margin_left = int(left_entry.get())
        margin_top = int(top_entry.get())
        margin_right = int(right_entry.get())
        margin_bottom = int(bottom_entry.get())
        font_size = int(font_size_entry.get())
        line_spacing = int(line_spacing_entry.get())
        
        background = Image.open(background_path)
        draw = ImageDraw.Draw(background)
        
        # Якщо шрифт обрано, наносимо текст
        if font_path:
            font = ImageFont.truetype(font_path, size=font_size)
            max_width = background.width - (margin_left + margin_right)
            lines = []
            for line in text.split("\n"):
                words = line.split(" ")
                current_line = ""
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if font.getbbox(test_line)[2] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
            
        page_number = 1
        is_flipped = False
        current_image = background.copy()
        current_draw = ImageDraw.Draw(current_image)
        text_y = margin_top
        for line in lines:
            if text_y + font.getbbox(line)[3] > background.height - margin_bottom:
                output_path = f"{output_dir}/output_page_{page_number}.jpg"
                current_image.save(output_path)
                print(f"Файл збережено:{output_path}")
                page_number += 1
                is_flipped = not is_flipped
                current_image = background.transpose(Image.FLIP_LEFT_RIGHT) if is_flipped else background.copy()
                current_draw = ImageDraw.Draw(current_image)
                text_y = margin_top

            current_draw.text((margin_left, text_y), line, font=font, fill="black")
            text_y += font.getbbox(line)[3] + line_spacing

        output_path = f"{output_dir}/output_page_{page_number}.jpg"
        current_image.save(output_path)
        print(f"Файл збережено: {output_path}")
        open_folder_in_default_manager(output_dir)
    except Exception as e:
        print(f"Помилка: {e}")

def create_gui():
    global text_input, left_entry, right_entry, top_entry, bottom_entry, font_size_entry, background_label, font_label, background_path, font_path, line_spacing_entry, preview_label
    background_path = ""
    font_path = ""

    root = tk.Tk()
    root.title("Створення конспетів")
    root.geometry("1920x1080")
    root.resizable(True, True)

    tk.Label(root, text="Введіть текст:").grid(row=0, column=0)
    text_input = tk.Text(root, height=50, width=100)
    text_input.grid(row=1, column=0, rowspan=90, padx=5)
    text_input.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Відступ зліва:").grid(row=0, column=1)
    left_entry = tk.Entry(root)
    left_entry.grid(row=1, column=1)
    left_entry.insert(0, "50")
    left_entry.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Відступ зверху:").grid(row=0, column=2)
    top_entry = tk.Entry(root)
    top_entry.grid(row=1, column=2)
    top_entry.insert(0, "45")
    top_entry.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Відступ справа:").grid(row=2, column=1)
    right_entry = tk.Entry(root)
    right_entry.grid(row=3, column=1)
    right_entry.insert(0, "20")
    right_entry.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Відступ знизу:").grid(row=2, column=2)
    bottom_entry = tk.Entry(root)
    bottom_entry.grid(row=3, column=2)
    bottom_entry.insert(0, "0")
    bottom_entry.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Відстань між рядками:").grid(row=4, column=2) 
    line_spacing_entry = tk.Entry(root)
    line_spacing_entry.grid(row=5, column=2)
    line_spacing_entry.insert(0, "3")
    line_spacing_entry.bind("<KeyRelease>", on_input_change)

    tk.Label(root, text="Розмір шрифту:").grid(row=4, column=1)
    font_size_entry = tk.Entry(root)
    font_size_entry.grid(row=5, column=1)
    font_size_entry.insert(0, "25")
    font_size_entry.bind("<KeyRelease>", on_input_change)

    tk.Button(root, text="Обрати фон", command=select_background).grid(row=6, column=2)
    background_label = tk.Label(root, text="Фон не обрано")
    background_label.grid(row=7, column=2)

    tk.Button(root, text="Обрати шрифт", command=select_font).grid(row=6, column=1)
    font_label = tk.Label(root, text="Шрифт не обрано")
    font_label.grid(row=7, column=1)

    tk.Button(root, text="Створити", command=generate_text_on_image).grid(row=8, column=1, columnspan=2, pady=20, ipadx=30)

    tk.Label(root, text="Попередній перегляд:").grid(row=0, column=3)
     
    preview_label = tk.Label(root)
    preview_label.grid(row=1, column=3, padx=5, rowspan=90)

    create_preview()
    root.mainloop()

create_gui()
