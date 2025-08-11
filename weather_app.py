import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

API_KEY = "12c26e94b5510c3f4ca37ddf7a0d29b2"  
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def fetch_weather():
    city = city_entry.get()
    if not city.strip():
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    try:
        url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", data.get("message", "Unknown error"))
            return

        name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        city_label.config(text=f"📍 {name}")
        temp_label.config(text=f"🌡 {temp}°C")
        humidity_label.config(text=f"💧 {humidity}%")
        condition_label.config(text=f"☁ {condition.capitalize()}")

        # Weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = icon_response.content
        img = Image.open(io.BytesIO(icon_data))
        img = ImageTk.PhotoImage(img)
        icon_label.config(image=img)
        icon_label.image = img

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("320x420")
root.configure(bg="#a8edea")

title_label = tk.Label(root, text="🌍 Weather App", font=("Segoe UI", 18, "bold"), bg="#a8edea")
title_label.pack(pady=10)

city_entry = tk.Entry(root, font=("Segoe UI", 14), relief="solid", bd=1)
city_entry.pack(pady=10, padx=20, fill=tk.X)

search_btn = tk.Button(root, text="Get Weather", command=fetch_weather,
                       bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"), relief="flat")
search_btn.pack(pady=5)

city_label = tk.Label(root, text="", font=("Segoe UI", 16, "bold"), bg="#a8edea")
city_label.pack(pady=5)

icon_label = tk.Label(root, bg="#a8edea")
icon_label.pack()

temp_label = tk.Label(root, text="", font=("Segoe UI", 14), bg="#a8edea")
temp_label.pack()

humidity_label = tk.Label(root, text="", font=("Segoe UI", 14), bg="#a8edea")
humidity_label.pack()

condition_label = tk.Label(root, text="", font=("Segoe UI", 14), bg="#a8edea")
condition_label.pack()

root.mainloop()
