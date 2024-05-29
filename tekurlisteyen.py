import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import cv2
import numpy as np
import os
import random
import string
from ttkthemes import ThemedTk

def take_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Tarayıcıyı başlıksız çalıştır (isteğe bağlı)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # Sayfanın tamamen yüklenmesini beklemek için bekleme süresi

    screenshot_path = f"screenshot_{generate_random_string(6)}.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    return screenshot_path

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

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
    url = entry.get()
    screenshot1 = "y.png"
    if not os.path.exists(screenshot1):
        label_result.config(text="x.png not found in directory", foreground="red")
        return
    
    screenshot2 = take_screenshot(url)

    similarity = compare_images(screenshot1, screenshot2)
    similarity_percentage = round(similarity * 100, 2)
    label_result.config(text=f"Similarity: {similarity_percentage}%", foreground="blue")

    image1 = Image.open(screenshot1)
    image1.thumbnail((300, 300))
    photo1 = ImageTk.PhotoImage(image1)
    label_image1.config(image=photo1)
    label_image1.image = photo1

    image2 = Image.open(screenshot2)
    image2.thumbnail((300, 300))
    photo2 = ImageTk.PhotoImage(image2)
    label_image2.config(image=photo2)
    label_image2.image = photo2

root = ThemedTk(theme="breeze")
root.title("Screenshot Comparison")

label = tk.Label(root, text="Enter URL:", font=("Arial", 12))
label.grid(row=0, column=0, padx=10, pady=5)
entry = tk.Entry(root, font=("Arial", 12), width=50)
entry.grid(row=0, column=1, padx=10, pady=5)

button_select = tk.Button(root, text="Get Screenshot and Compare", font=("Arial", 12), command=get_screenshots)
button_select.grid(row=1, column=1, pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.grid(row=2, column=0, columnspan=2, pady=5)

frame1 = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
frame1.grid(row=3, column=0, padx=10, pady=5)
label_image1 = tk.Label(frame1)
label_image1.pack()

frame2 = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
frame2.grid(row=3, column=1, padx=10, pady=5)
label_image2 = tk.Label(frame2)
label_image2.pack()

root.mainloop()
