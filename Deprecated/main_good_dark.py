import tkinter as tk
from tkinter import ttk
import calendar
import datetime
import requests
import threading
import time

class WeatherClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock, Weather & Calendar")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Create main frames
        self.create_frames()
        
        # Initialize widgets
        self.create_clock_widgets()
        self.create_weather_widgets()
        self.create_calendar_widget()
        
        # Start update loops
        self.update_clock()
        self.update_weather()
        
    def create_frames(self):
        # Left frame for clock, date, and weather
        self.left_frame = tk.Frame(self.root, bg="#2c3e50", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20)
        self.left_frame.pack_propagate(False)
        
        # Right frame for calendar
        self.right_frame = tk.Frame(self.root, bg="#2c3e50", width=380)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=20)
        self.right_frame.pack_propagate(False)
        
    def create_clock_widgets(self):
        # Clock frame
        clock_frame = tk.Frame(self.left_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        clock_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(clock_frame, text="Current Time", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(pady=5)
        
        self.time_label = tk.Label(clock_frame, font=("Digital-7", 24, "bold"), 
                                  bg="#34495e", fg="#1abc9c")
        self.time_label.pack(pady=5)
        
        self.date_label = tk.Label(clock_frame, font=("Arial", 16), 
                                  bg="#34495e", fg="#ecf0f1")
        self.date_label.pack(pady=(0, 10))
        
    def create_weather_widgets(self):
        # Weather frame
        weather_frame = tk.Frame(self.left_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        weather_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(weather_frame, text="Bangalore Weather", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(pady=5)
        
        self.temp_label = tk.Label(weather_frame, font=("Arial", 20, "bold"), 
                                  bg="#34495e", fg="#e74c3c")
        self.temp_label.pack(pady=5)
        
        self.desc_label = tk.Label(weather_frame, font=("Arial", 12), 
                                  bg="#34495e", fg="#ecf0f1")
        self.desc_label.pack()
        
        self.humidity_label = tk.Label(weather_frame, font=("Arial", 10), 
                                      bg="#34495e", fg="#bdc3c7")
        self.humidity_label.pack()
        
        self.last_update_label = tk.Label(weather_frame, font=("Arial", 8), 
                                         bg="#34495e", fg="#95a5a6")
        self.last_update_label.pack(pady=(5, 10))
        
    def create_calendar_widget(self):
        # Calendar frame
        cal_frame = tk.Frame(self.right_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        cal_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(cal_frame, text="Calendar", font=("Arial", 14, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(pady=5)
        
        # Month/Year navigation
        nav_frame = tk.Frame(cal_frame, bg="#34495e")
        nav_frame.pack(pady=5)
        
        self.prev_btn = tk.Button(nav_frame, text="<", command=self.prev_month,
                                 bg="#3498db", fg="white", font=("Arial", 12, "bold"))
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.month_year_label = tk.Label(nav_frame, font=("Arial", 12, "bold"), 
                                        bg="#34495e", fg="#ecf0f1")
        self.month_year_label.pack(side=tk.LEFT, padx=20)
        
        self.next_btn = tk.Button(nav_frame, text=">", command=self.next_month,
                                 bg="#3498db", fg="white", font=("Arial", 12, "bold"))
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Calendar grid
        self.cal_grid_frame = tk.Frame(cal_frame, bg="#34495e")
        self.cal_grid_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Initialize current date
        now = datetime.datetime.now()
        self.current_month = now.month
        self.current_year = now.year
        self.today = now.day
        
        self.create_calendar_grid()
        
    def create_calendar_grid(self):
        # Clear existing grid
        for widget in self.cal_grid_frame.winfo_children():
            widget.destroy()
            
        # Update month/year label
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        
        # Day headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            label = tk.Label(self.cal_grid_frame, text=day, font=("Arial", 10, "bold"),
                           bg="#2c3e50", fg="#ecf0f1", width=4)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Calendar days
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        current_date = datetime.date.today()
        
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                    
                # Check if it's today
                is_today = (day == current_date.day and 
                           self.current_month == current_date.month and 
                           self.current_year == current_date.year)
                
                bg_color = "#e74c3c" if is_today else "#95a5a6"
                fg_color = "white" if is_today else "#2c3e50"
                
                day_label = tk.Label(self.cal_grid_frame, text=str(day),
                                   font=("Arial", 10, "bold" if is_today else "normal"),
                                   bg=bg_color, fg=fg_color, width=4, height=2)
                day_label.grid(row=week_num, column=day_num, padx=1, pady=1)
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar_grid()
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar_grid()
    
    def update_clock(self):
        now = datetime.datetime.now()
        
        # Update time
        time_str = now.strftime("%H:%M:%S")
        self.time_label.config(text=time_str)
        
        # Update date
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_label.config(text=date_str)
        
        # Schedule next update
        self.root.after(1000, self.update_clock)
    
    def get_weather_data(self):
        try:
            # Using OpenWeatherMap API (you can get a free API key)
            # For demo purposes, using a mock response
            # Replace with actual API call:
            # api_key = "YOUR_API_KEY"
            # url = f"http://api.openweathermap.org/data/2.5/weather?q=Bangalore,IN&appid={api_key}&units=metric"
            # response = requests.get(url, timeout=10)
            # data = response.json()
            
            # Mock data for demonstration
            import random
            temp = random.randint(20, 35)
            descriptions = ["Clear Sky", "Few Clouds", "Scattered Clouds", "Partly Cloudy", "Light Rain"]
            desc = random.choice(descriptions)
            humidity = random.randint(40, 80)
            
            return {
                "temperature": temp,
                "description": desc,
                "humidity": humidity
            }
            
        except Exception as e:
            return None
    
    def update_weather_display(self, weather_data):
        if weather_data:
            temp_text = f"{weather_data['temperature']}°C"
            self.temp_label.config(text=temp_text)
            self.desc_label.config(text=weather_data['description'])
            self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        else:
            self.temp_label.config(text="Weather Unavailable")
            self.desc_label.config(text="Check connection")
            self.humidity_label.config(text="")
        
        # Update last refresh time
        update_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.last_update_label.config(text=f"Last updated: {update_time}")
    
    def update_weather(self):
        def fetch_and_update():
            weather_data = self.get_weather_data()
            self.root.after(0, lambda: self.update_weather_display(weather_data))
        
        # Fetch weather in background thread
        thread = threading.Thread(target=fetch_and_update, daemon=True)
        thread.start()
        
        # Schedule next weather update (60 seconds = 60000 ms)
        self.root.after(60000, self.update_weather)

def main():
    root = tk.Tk()
    app = WeatherClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()