import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, date
import requests
import threading
import json

class ClockWeatherCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock, Weather & Calendar")
        self.root.geometry("900x600")
        
        # OpenWeatherMap API key - Replace with your actual API key
        self.api_key = "your_api_key_here"  # Get free API key from openweathermap.org
        
        # Set up style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Current date
        self.current_date = datetime.now()
        self.selected_date = None
        
        # Time variables
        self.time_var = tk.StringVar()
        self.date_var = tk.StringVar()
        
        # Weather variables
        self.weather_temp = tk.StringVar()
        self.weather_desc = tk.StringVar()
        self.weather_location = tk.StringVar()
        self.weather_status = tk.StringVar()
        
        # Configure styles
        self.configure_styles()
        
        # Create UI
        self.create_widgets()
        self.update_calendar()
        self.start_clock()
        self.fetch_weather_data()
    
    def configure_styles(self):
        """Configure custom styles for better appearance"""
        # Clock styles
        self.style.configure(
            'Clock.TLabel',
            font=('Courier New', 28, 'bold'),
            foreground="#8dbc7a",
            background="#ddefe2",
            anchor='center'
        )
        
        self.style.configure(
            'Date.TLabel',
            font=('Arial', 16, 'bold'),
            foreground='#ecf0f1',
            background='#2c3e50',
            anchor='center'
        )
        
        # Weather styles
        self.style.configure(
            'WeatherTemp.TLabel',
            font=('Arial', 24, 'bold'),
            foreground='#3498db',
            anchor='center'
        )
        
        self.style.configure(
            'WeatherDesc.TLabel',
            font=('Arial', 14),
            foreground='#2c3e50',
            anchor='center'
        )
        
        self.style.configure(
            'WeatherLocation.TLabel',
            font=('Arial', 12),
            foreground='#7f8c8d',
            anchor='center'
        )
        
        # Header style
        self.style.configure(
            'Header.TLabel',
            font=('Arial', 14, 'bold'),
            foreground='#2c3e50',
            background='#ecf0f1'
        )
        
        # Day header style
        self.style.configure(
            'DayHeader.TLabel',
            font=('Arial', 10, 'bold'),
            foreground='#34495e',
            background='#bdc3c7',
            anchor='center'
        )
        
        # Day number style
        self.style.configure(
            'Day.TLabel',
            font=('Arial', 10),
            foreground='#2c3e50',
            background='#ffffff',
            anchor='center',
            relief='flat',
            borderwidth=1
        )
        
        # Today style
        self.style.configure(
            'Today.TLabel',
            font=('Arial', 10, 'bold'),
            foreground='#ffffff',
            background='#e74c3c',
            anchor='center',
            relief='solid',
            borderwidth=1
        )
        
        # Selected day style
        self.style.configure(
            'Selected.TLabel',
            font=('Arial', 10, 'bold'),
            foreground='#ffffff',
            background='#3498db',
            anchor='center',
            relief='solid',
            borderwidth=2
        )
    
    def create_widgets(self):
        """Create the main UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Clock side
        main_frame.columnconfigure(1, weight=2)  # Calendar side
        main_frame.rowconfigure(0, weight=1)
        
        # Create clock and weather section (left side)
        self.create_clock_weather_section(main_frame)
        
        # Create separator
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=10)
        
        # Create calendar section (right side)
        self.create_calendar_section(main_frame)
    
    def create_clock_weather_section(self, parent):
        """Create the clock and weather section on the left"""
        left_frame = ttk.Frame(parent, padding="20")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        left_frame.columnconfigure(0, weight=1)
        
        # Clock section
        clock_title = ttk.Label(
            left_frame, 
            text="🕐 CLOCK", 
            font=('Arial', 18, 'bold'),
            foreground='#2c3e50'
        )
        clock_title.grid(row=0, column=0, pady=(0, 20))
        
        # Clock display frame
        clock_display_frame = ttk.Frame(left_frame, relief='solid', borderwidth=2, padding="20")
        clock_display_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 30))
        clock_display_frame.columnconfigure(0, weight=1)
        
        # Time display
        time_label = ttk.Label(
            clock_display_frame,
            textvariable=self.time_var,
            style='Clock.TLabel'
        )
        time_label.grid(row=0, column=0, pady=(10, 5))
        
        # Date display
        date_label = ttk.Label(
            clock_display_frame,
            textvariable=self.date_var,
            style='Date.TLabel'
        )
        date_label.grid(row=1, column=0, pady=(5, 10))
        
        # Weather section
        weather_title = ttk.Label(
            left_frame, 
            text="🌤️ WEATHER", 
            font=('Arial', 18, 'bold'),
            foreground='#2c3e50'
        )
        weather_title.grid(row=2, column=0, pady=(0, 15))
        
        # Weather display frame
        weather_frame = ttk.LabelFrame(left_frame, text="Current Weather", padding="20")
        weather_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        weather_frame.columnconfigure(0, weight=1)
        
        # Temperature display
        temp_label = ttk.Label(
            weather_frame,
            textvariable=self.weather_temp,
            style='WeatherTemp.TLabel'
        )
        temp_label.grid(row=0, column=0, pady=(0, 10))
        
        # Weather description
        desc_label = ttk.Label(
            weather_frame,
            textvariable=self.weather_desc,
            style='WeatherDesc.TLabel'
        )
        desc_label.grid(row=1, column=0, pady=(0, 10))
        
        # Location
        location_label = ttk.Label(
            weather_frame,
            textvariable=self.weather_location,
            style='WeatherLocation.TLabel'
        )
        location_label.grid(row=2, column=0, pady=(0, 10))
        
        # Weather status
        status_label = ttk.Label(
            weather_frame,
            textvariable=self.weather_status,
            font=('Arial', 9),
            foreground='#95a5a6'
        )
        status_label.grid(row=3, column=0)
        
        # Refresh weather button
        refresh_btn = ttk.Button(
            left_frame,
            text="🔄 Refresh Weather",
            command=self.fetch_weather_threaded
        )
        refresh_btn.grid(row=4, column=0, pady=(10, 0))
    
    def create_calendar_section(self, parent):
        """Create the calendar section on the right"""
        calendar_main_frame = ttk.Frame(parent, padding="10")
        calendar_main_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        calendar_main_frame.columnconfigure(0, weight=1)
        
        # Calendar title
        cal_title = ttk.Label(
            calendar_main_frame, 
            text="📅 CALENDAR", 
            font=('Arial', 18, 'bold'),
            foreground='#2c3e50'
        )
        cal_title.grid(row=0, column=0, pady=(0, 15))
        
        # Navigation frame
        nav_frame = ttk.Frame(calendar_main_frame)
        nav_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        nav_frame.columnconfigure(1, weight=1)
        
        # Previous month button
        self.prev_btn = ttk.Button(
            nav_frame, 
            text="◀ Previous", 
            command=self.prev_month,
            width=8
        )
        self.prev_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Month/Year label
        self.month_year_label = ttk.Label(
            nav_frame, 
            text="", 
            style='Header.TLabel',
            anchor='center'
        )
        self.month_year_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Next month button
        self.next_btn = ttk.Button(
            nav_frame, 
            text="Next ▶", 
            command=self.next_month,
            width=8
        )
        self.next_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Calendar frame
        self.calendar_frame = ttk.Frame(calendar_main_frame, relief='solid', borderwidth=1)
        self.calendar_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure calendar frame columns to be equal width
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, minsize=60)
        
        # Create day headers
        self.create_day_headers()
        
        # Today button
        today_btn = ttk.Button(
            calendar_main_frame,
            text="Go to Today",
            command=self.go_to_today
        )
        today_btn.grid(row=3, column=0, pady=(10, 0))
    
    def create_day_headers(self):
        """Create the day of week headers"""
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            label = ttk.Label(
                self.calendar_frame, 
                text=day, 
                style='DayHeader.TLabel',
                width=8
            )
            label.grid(row=0, column=i, sticky=(tk.W, tk.E, tk.N, tk.S), padx=1, pady=1)
    
    def start_clock(self):
        """Start the clock updates"""
        self.update_clock()
        self.clock_update_loop()
    
    def update_clock(self):
        """Update clock display"""
        now = datetime.now()
        
        # Format time (24-hour with seconds)
        time_str = now.strftime("%H:%M:%S")
        self.time_var.set(time_str)
        
        # Update date
        date_str = now.strftime("%A, %B %d, %Y")
        self.date_var.set(date_str)
    
    def clock_update_loop(self):
        """Continuous clock update loop"""
        self.update_clock()
        self.root.after(1000, self.clock_update_loop)
    
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
    
    def fetch_weather_data(self):
        """Fetch weather data from OpenWeatherMap"""
        try:
            self.weather_status.set("Getting location...")
            
            # Get location
            city, country, lat, lon = self.get_location_by_ip()
            
            self.weather_status.set("Fetching weather data...")
            
            # Check if we have a valid API key
            if self.api_key == "your_api_key_here" or not self.api_key:
                # Use mock data for demonstration
                self.use_mock_weather_data(city, country)
                return
            
            # Construct API URL
            if lat and lon:
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            else:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            
            # Make API request
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract weather information
                temp = round(data['main']['temp'])
                feels_like = round(data['main']['feels_like'])
                description = data['weather'][0]['description'].title()
                main_weather = data['weather'][0]['main']
                humidity = data['main']['humidity']
                location_name = data['name']
                
                # Update weather display
                self.weather_temp.set(f"{temp}°C")
                
                # Create detailed description
                weather_desc = f"{description}"
                if main_weather.lower() in ['rain', 'drizzle', 'thunderstorm']:
                    weather_desc += " 🌧️"
                elif main_weather.lower() in ['snow']:
                    weather_desc += " ❄️"
                elif main_weather.lower() in ['clear']:
                    weather_desc += " ☀️"
                elif main_weather.lower() in ['clouds']:
                    weather_desc += " ☁️"
                
                self.weather_desc.set(weather_desc)
                self.weather_location.set(f"{location_name}, {country}")
                
                # Additional info
                additional_info = f"Feels like {feels_like}°C • Humidity {humidity}%"
                self.weather_status.set(additional_info)
                
            else:
                self.weather_temp.set("--°C")
                self.weather_desc.set("Weather data unavailable")
                self.weather_location.set(f"{city}, {country}")
                self.weather_status.set(f"API Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.weather_temp.set("--°C")
            self.weather_desc.set("Request timeout")
            self.weather_status.set("Connection timeout")
        except requests.exceptions.RequestException as e:
            self.weather_temp.set("--°C")
            self.weather_desc.set("Connection error")
            self.weather_status.set("Network error")
        except Exception as e:
            self.weather_temp.set("--°C")
            self.weather_desc.set("Error fetching weather")
            self.weather_status.set(f"Error: {str(e)[:30]}...")
    
    def use_mock_weather_data(self, city, country):
        """Use mock weather data when API key is not available"""
        import random
        
        # Mock weather conditions
        conditions = [
            ("Sunny", "☀️", 25),
            ("Partly Cloudy", "⛅", 22),
            ("Cloudy", "☁️", 18),
            ("Light Rain", "🌧️", 16),
            ("Clear Sky", "☀️", 24),
            ("Overcast", "☁️", 19)
        ]
        
        # Select random condition based on city hash for consistency
        condition_index = hash(city) % len(conditions)
        desc, emoji, base_temp = conditions[condition_index]
        
        # Add some randomness
        temp = base_temp + random.randint(-3, 3)
        humidity = random.randint(40, 80)
        
        self.weather_temp.set(f"{temp}°C")
        self.weather_desc.set(f"{desc} {emoji}")
        self.weather_location.set(f"{city}, {country}")
        self.weather_status.set(f"Feels like {temp + random.randint(-2, 2)}°C • Humidity {humidity}%")
    
    def fetch_weather_threaded(self):
        """Fetch weather in a separate thread"""
        thread = threading.Thread(target=self.fetch_weather_data)
        thread.daemon = True
        thread.start()
    
    def update_calendar(self):
        """Update the calendar display"""
        # Clear existing calendar (except headers)
        for widget in self.calendar_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        # Update month/year label
        month_year = self.current_date.strftime("%B %Y")
        self.month_year_label.config(text=month_year)
        
        # Get calendar data
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        today = date.today()
        
        # Fill calendar
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days from other months
                    label = ttk.Label(
                        self.calendar_frame, 
                        text="", 
                        width=8
                    )
                else:
                    # Create date object for this day
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    
                    # Determine style
                    if day_date == today:
                        style = 'Today.TLabel'
                    elif self.selected_date and day_date == self.selected_date:
                        style = 'Selected.TLabel'
                    else:
                        style = 'Day.TLabel'
                    
                    # Create label
                    label = ttk.Label(
                        self.calendar_frame, 
                        text=str(day), 
                        style=style,
                        width=8
                    )
                    
                    # Bind click event
                    label.bind("<Button-1>", lambda e, d=day_date: self.select_date(d))
                    label.bind("<Enter>", lambda e, w=label: self.on_hover_enter(w))
                    label.bind("<Leave>", lambda e, w=label: self.on_hover_leave(w))
                
                label.grid(
                    row=week_num, 
                    column=day_num, 
                    sticky=(tk.W, tk.E, tk.N, tk.S), 
                    padx=1, 
                    pady=1,
                    ipady=6
                )
    
    def select_date(self, selected_date):
        """Handle date selection"""
        self.selected_date = selected_date
        self.update_calendar()
    
    def on_hover_enter(self, widget):
        """Handle mouse hover enter"""
        current_style = str(widget.cget('style'))
        if current_style not in ['Today.TLabel', 'Selected.TLabel']:
            widget.configure(style='Selected.TLabel')
    
    def on_hover_leave(self, widget):
        """Handle mouse hover leave"""
        widget_text = widget.cget('text')
        if widget_text:
            day = int(widget_text)
            day_date = date(self.current_date.year, self.current_date.month, day)
            today = date.today()
            
            if day_date == today:
                widget.configure(style='Today.TLabel')
            elif self.selected_date and day_date == self.selected_date:
                widget.configure(style='Selected.TLabel')
            else:
                widget.configure(style='Day.TLabel')
    
    def prev_month(self):
        """Navigate to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()
    
    def next_month(self):
        """Navigate to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()
    
    def go_to_today(self):
        """Navigate to current month"""
        self.current_date = datetime.now()
        self.update_calendar()

def main():
    root = tk.Tk()
    app = ClockWeatherCalendarApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()