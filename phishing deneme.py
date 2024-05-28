import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
import time
import cv2
import numpy as np
import os
import random
import string
from PIL import Image, ImageTk

def take_screenshot(url):
    driver = webdriver.Chrome()  
    driver.get(url) 
    time.sleep(5)  
    
    screenshot_path = f"screenshot_{generate_random_string(6)}.png"  
    driver.save_screenshot(screenshot_path)
    
    driver.quit()  
    return screenshot_path

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def compare_images(image1, image2):
    # Resimleri yükle
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    
    # Resimleri aynı boyuta yeniden boyutlandır
    image1 = cv2.resize(image1, (300, 300))
    image2 = cv2.resize(image2, (300, 300))
    
    # Resimleri gri tonlamalı olarak yükle
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Piksel piksel karşılaştırma
    difference = cv2.subtract(gray_image1, gray_image2)
    diff_pixels = np.count_nonzero(difference)
    
    # Benzerlik oranını hesapla
    total_pixels = gray_image1.shape[0] * gray_image1.shape[1]
    similarity_ratio = 1 - (diff_pixels / total_pixels)
    
    return similarity_ratio

def get_screenshots():
    url1 = entry1.get()  
    url2 = entry2.get()  
    
    # Ekran görüntülerini al
    screenshot1 = take_screenshot(url1)
    screenshot2 = take_screenshot(url2)
    
    # Resimleri karşılaştır
    similarity = compare_images(screenshot1, screenshot2)
    
    # Benzerlik oranını ekrana yazdır
    label_result.config(text=f"Similarity: {similarity}")
    
    # Ekran görüntülerini göster
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

# Arayüzü oluştur
root = tk.Tk()
root.title("Screenshot Comparison")

label1 = tk.Label(root, text="Enter URL 1:")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="Enter URL 2:")
label2.pack()

entry2 = tk.Entry(root)
entry2.pack()

button_select = tk.Button(root, text="Get Screenshots", command=get_screenshots)
button_select.pack()
    
label_result = tk.Label(root, text="")
label_result.pack()

label_image1 = tk.Label(root)
label_image1.pack()

label_image2 = tk.Label(root)
label_image2.pack()

root.mainloop()