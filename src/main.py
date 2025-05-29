import tkinter as tk
from tkinter import ttk
import time
import datetime
import calendar
import requests
import threading
from PIL import Image, ImageTk
import os

class DesktopClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕒 Desktop Clock & Weather")
        self.root.geometry("800x500")
        self.root.configure(bg='white')
        self.root.resizable(False, False)
        
        # Weather API configuration
        self.api_key = os.environ.get("API_KEY")  # Replace with actual API key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        # Get location
        self.city, self.country, self.lat, self.lon = self.get_location_by_ip()
        self.weather_data = {"temp": "Loading...", "desc": "Loading..."}
        
        self.setup_ui()
        self.update_time()
        self.update_weather()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel for clock, date, and weather
        left_frame = tk.Frame(main_frame, bg='white', width=400)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Right panel for calendar
        right_frame = tk.Frame(main_frame, bg='white', width=350)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Clock section
        clock_frame = tk.Frame(left_frame, bg='white', relief='solid', bd=1)
        clock_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(clock_frame, text="🕒 TIME", font=('Arial', 15, 'bold'), 
                bg='white', fg='#333333').pack(pady=(10, 5))
        
        self.time_label = tk.Label(clock_frame, text="", font=('Digital-7', 30, 'bold'), 
                                  bg='white', fg='#2c3e50')
        self.time_label.pack(pady=(0, 10))
        
        # Date section
        date_frame = tk.Frame(left_frame, bg='white', relief='solid', bd=1)
        date_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(date_frame, text="📅 DATE", font=('Arial', 12, 'bold'), bg='white', fg='#333333').pack(pady=(10, 5))
        
        self.date_label = tk.Label(date_frame, text="", font=('Arial', 19, 'bold'), bg='white', fg='#2c3e50')
        self.date_label.pack(pady=(0, 10))
        
        # Weather section
        weather_frame = tk.Frame(left_frame, bg='white', relief='solid', bd=1)
        weather_frame.pack(fill='x')
        
        tk.Label(weather_frame, text="🌤️ BANGALORE WEATHER", font=('Arial', 12, 'bold'), bg='white', fg='#333333').pack(pady=(10, 5))

        self.temp_label = tk.Label(weather_frame, text="", font=('Arial', 30, 'bold'), bg='white', fg='#e74c3c')
        self.temp_label.pack()
        
        self.weather_icon_label = ttk.Label(weather_frame)
        self.weather_icon_label.pack(pady=(0, 0))

        self.weather_desc_label = tk.Label(weather_frame, text="", font=('Arial', 18), bg='white', fg='#7f8c8d')
        self.weather_desc_label.pack(pady=(0, 10))

        self.humidity_wind_label = tk.Label(weather_frame, text="", font=('Arial', 18), bg='white', fg='#95a5a6')
        self.humidity_wind_label.pack(pady=(0, 10))

        self.weather_update_label = tk.Label(weather_frame, text="", font=('Arial', 10), bg='white', fg='#95a5a6')
        self.weather_update_label.pack(pady=(0, 10))
        
        # Calendar section
        calendar_frame = tk.Frame(right_frame, bg='white', relief='solid', bd=1)
        calendar_frame.pack(fill='both', expand=True)
        
        tk.Label(calendar_frame, text="📆 CALENDAR", font=('Arial', 12, 'bold'), bg='white', fg='#333333').pack(pady=(10, 5))
        
        # Month/Year navigation
        nav_frame = tk.Frame(calendar_frame, bg='white')
        nav_frame.pack(pady=(0, 10))
        
        self.prev_button = tk.Button(nav_frame, text="◀", font=('Arial', 12, 'bold'),
                                    bg='#ecf0f1', fg='#2c3e50', bd=1, relief='solid',
                                    command=self.prev_month, cursor='hand2')
        self.prev_button.pack(side='left', padx=5)
        
        self.month_year_label = tk.Label(nav_frame, text="", font=('Arial', 14, 'bold'),
                                        bg='white', fg='#2c3e50')
        self.month_year_label.pack(side='left', padx=20)
        
        self.next_button = tk.Button(nav_frame, text="▶", font=('Arial', 12, 'bold'),
                                    bg='#ecf0f1', fg='#2c3e50', bd=1, relief='solid',
                                    command=self.next_month, cursor='hand2')
        self.next_button.pack(side='left', padx=5)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(calendar_frame, bg='white')
        self.calendar_frame.pack(padx=10, pady=(0, 10))
        
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        self.create_calendar()
        
    def create_calendar(self):
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
            
        # Update month/year label
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        
        # Days of week headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            label = tk.Label(self.calendar_frame, text=day, font=('Arial', 10, 'bold'),
                           bg='#34495e', fg='white', width=4, height=2)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Calendar days
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        today = datetime.date.today()
        
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    label = tk.Label(self.calendar_frame, text="", bg='white', width=4, height=2)
                else:
                    # Highlight today
                    if (day == today.day and self.current_month == today.month 
                        and self.current_year == today.year):
                        bg_color = '#3498db'
                        fg_color = 'white'
                        font_weight = 'bold'
                    else:
                        bg_color = '#ecf0f1'
                        fg_color = '#2c3e50'
                        font_weight = 'normal'
                    
                    label = tk.Label(self.calendar_frame, text=str(day), 
                                   font=('Arial', 10, font_weight),
                                   bg=bg_color, fg=fg_color, width=4, height=2,
                                   relief='solid', bd=1)
                
                label.grid(row=week_num, column=day_num, padx=1, pady=1)
        
        # Configure grid weights to prevent uneven sizing
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="col")
        for i in range(len(cal) + 1):  # +1 for header row
            self.calendar_frame.rowconfigure(i, weight=1, uniform="row")
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar()
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar()
    
    def update_time(self):
        #current_time = time.strftime("%H:%M:%S")
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%A, %B %d, %Y")
        
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        
        # Update every second
        self.root.after(1000, self.update_time)
    
    def fetch_weather(self):
        try:
            # Using OpenWeatherMap API (free tier)
            # You need to register at openweathermap.org and get an API key
            # if self.api_key == "your_api_key_here":
            #     # Demo data when no API key is provided
            #     import random
            #     temp = random.randint(20, 35)
            #     descriptions = ["Clear Sky", "Few Clouds", "Scattered Clouds", "Light Rain"]
            #     desc = random.choice(descriptions)
            #     self.weather_data = {
            #         "temp": f"{temp}°C",
            #         "desc": desc
            #     }
            # else:
                # url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric"
                # response = requests.get(url, timeout=5)
                # data = response.json()
                
                # temp = round(data['main']['temp'])
                # desc = data['weather'][0]['description'].title()
                
                # self.weather_data = {
                #     "temp": f"{temp}°C",
                #     "desc": desc
                # }
                weather_info = self.fetch_openweathermap()
                if weather_info:
                    icon_code = weather_info['current']['weather'][0]['icon']
                    photo = self.load_weather_icon(icon_code)

                    temp = round(weather_info['current']['temp'])
                    temp_feels_like = round(weather_info['current']['feels_like'])
                    desc = f"{weather_info['current']['weather'][0]['description']} with cloud {weather_info['current']['clouds']}%"
                    windandhumidity= f"{weather_info['current']['wind_speed']} m/s wind, {weather_info['current']['humidity']}% humidity"
                    self.weather_data = {
                        "temp": f"{temp}°C",
                        "temp_feels_like": f"{temp_feels_like}°C",
                        "icon": photo,
                        "desc": desc,
                        "windandhumidity": windandhumidity
                    }
                else:
                    self.weather_data = {
                        "temp": "N/A",
                        "desc": "Unable to fetch weather"
                    }
        except Exception as e:
            self.weather_data = {
                "temp": "N/A",
                "desc": "Unable to fetch weather"
            }
    def fetch_openweathermap(self):
        #self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        #self.lat = "12.9406"
        #self.lon = "77.5738"
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    def load_weather_icon(self, icon_code):
        try:
            image_path = os.path.join('images', f'{icon_code}_w.png')
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Could not load weather icon: {e}")
            return None

    def update_weather_display(self):
        self.temp_label.config(text=self.weather_data["temp"])
        self.weather_desc_label.config(text=self.weather_data["desc"])
        self.humidity_wind_label.config(text=self.weather_data["windandhumidity"])
        self.weather_icon_label.config(image=self.weather_data.get("icon", ""))
        #self.weather_icon_label.image = photo  # Keep a reference!

        update_time = time.strftime("%H:%M:%S")
        self.weather_update_label.config(text=f"Last updated: {update_time}")
    
    def get_location_by_ip(self):
        """Get approximate location using IP geolocation"""
        try:
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            if data['status'] == 'success':
                return data['city'], data['country'], data['lat'], data['lon']
        except Exception as e:
            print(f"Location error: {e}")
        return "Unknown", "Location", None, None

    def update_weather(self):
        # Fetch weather in a separate thread to avoid blocking UI
        def weather_thread():
            self.fetch_weather()
            self.root.after(0, self.update_weather_display)
        
        threading.Thread(target=weather_thread, daemon=True).start()
        
        # Update every minute (60000 ms)
        self.root.after(60000, self.update_weather)

def main():
    root = tk.Tk()
    app = DesktopClockApp(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_reqwidth() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_reqheight() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()