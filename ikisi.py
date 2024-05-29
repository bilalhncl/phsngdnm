import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from ttkthemes import ThemedTk

def mse(image1, image2):
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    return err

def compare_images(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_image1, gray_image2, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max(max_val, 0)  # Negatif değerleri sıfır olarak kabul et

def get_screenshots():
    # İlk dosyayı seçme
    image1_path = filedialog.askopenfilename(title="Select First Image",
                                             filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not image1_path:
        label_result.config(text="First image not selected", foreground="red")
        return

    # İkinci dosyayı seçme
    image2_path = filedialog.askopenfilename(title="Select Second Image",
                                             filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not image2_path:
        label_result.config(text="Second image not selected", foreground="red")
        return

    # Resimleri karşılaştır
    similarity = compare_images(image1_path, image2_path)
    similarity_percentage = round(similarity * 100, 2)
    label_result.config(text=f"Similarity: {similarity_percentage}%", foreground="blue")

    # Ekran görüntülerini göster
    image1 = Image.open(image1_path)
    image1.thumbnail((300, 300))
    photo1 = ImageTk.PhotoImage(image1)
    label_image1.config(image=photo1)
    label_image1.image = photo1

    image2 = Image.open(image2_path)
    image2.thumbnail((300, 300))
    photo2 = ImageTk.PhotoImage(image2)
    label_image2.config(image=photo2)
    label_image2.image = photo2

root = ThemedTk(theme="breeze")
root.title("Image Comparison")

button_select = tk.Button(root, text="Select Images and Compare", font=("Arial", 12), command=get_screenshots)
button_select.grid(row=0, column=0, columnspan=2, pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.grid(row=1, column=0, columnspan=2, pady=5)

frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
frame1.grid(row=2, column=0, padx=10, pady=5)
label_image1 = tk.Label(frame1)
label_image1.pack()

frame2 = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
frame2.grid(row=2, column=1, padx=10, pady=5)
label_image2 = tk.Label(frame2)
label_image2.pack()

root.mainloop()
