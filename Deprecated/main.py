import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
from PIL import Image, ImageTk
import os
import io

from calen.calendar_display import CalendarDisplay
from weatherV3.weather_service import WeatherService
from clock.clock_display import ClockDisplay
import utils.config as util

class DockDisplay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Raspberry Pi Dock")
        #self.attributes('-fullscreen', True)  # Enable fullscreen
        # Add escape key binding to exit fullscreen
        #self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
        # Adjust resolution based on your Pi display
        self.geometry("800x480")  # Common resolution for 7" Pi display
        self.configure(bg="#2E3440")

        # Define color scheme (Nord Theme)
        self.colors = {
            'bg': "#2E3440",
            'fg': "#D8DEE9",
            'accent1': "#88C0D0",  # Clock
            'accent2': "#A3BE8C",  # Calendar
            'accent3': "#B48EAD",  # Temperature
            'accent4': "#EBCB8B",  # Weather
            'accent5': "#D08770",  # Wind
            'accent6': "#BF616A"   # Humidity
        }

        # Enhanced style configuration
        self.style = ttk.Style()
        self.style.configure("Clock.TLabel",
                           background=self.colors['bg'],
                           foreground=self.colors['accent1'],
                           font=("DejaVu Sans", 48, "bold"))  # System font on Raspberry Pi
        
        self.style.configure("Calendar.TLabel",
                           background=self.colors['bg'],
                           foreground=self.colors['accent2'],
                           font=("DejaVu Sans", 18, "bold"))
        
        self.style.configure("Weather.TLabel",
                           background=self.colors['bg'],
                           foreground=self.colors['accent4'],
                           font=("DejaVu Sans", 18))
        
        self.style.configure("TFrame",
                           background=self.colors['bg'])

        # Initialize displays
        self.calendar_display = CalendarDisplay()
        self.weather_service = WeatherService(api_key=util.WEATHER_API_KEY)
        self.clock_display = ClockDisplay()

        # Create main container with grid
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create frames with grid layout
        self.create_layout()
        self.update_display()

    def create_layout(self):
        # Clock section (top)
        clock_frame = ttk.Frame(self.main_frame)
        clock_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.time_label = ttk.Label(clock_frame, style="Clock.TLabel")
        self.time_label.pack(anchor="center")

        # Create two columns for weather and calendar
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Weather column (left)
        weather_frame = ttk.Frame(content_frame)
        weather_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Weather icon and description
        self.weather_icon_label = ttk.Label(weather_frame, style="Weather.TLabel")
        self.weather_icon_label.pack(pady=(0, 10))
        
        self.weatherdesc_label = ttk.Label(weather_frame, style="Weather.TLabel", compound="top")
        self.weatherdesc_label.pack(pady=(0, 20))
        
        # Weather details in a grid
        details_frame = ttk.Frame(weather_frame)
        details_frame.pack(fill=tk.X, pady=10)
        
        self.temperature_label = ttk.Label(details_frame, style="Weather.TLabel")
        self.temperature_label.pack(pady=5)
        
        self.windspeed_label = ttk.Label(details_frame, style="Weather.TLabel")
        self.windspeed_label.pack(pady=5)
        
        self.humidity_label = ttk.Label(details_frame, style="Weather.TLabel")
        self.humidity_label.pack(pady=5)

        # Calendar column (right)
        calendar_frame = ttk.Frame(content_frame)
        calendar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.calendar_label = ttk.Label(calendar_frame, style="Calendar.TLabel", 
                                      justify=tk.LEFT, anchor="w")
        self.calendar_label.pack(fill=tk.BOTH, expand=True)

    def load_weather_icon(self, icon_code):
        try:
            image_path = os.path.join('images', f'{icon_code}_t.png')
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print(f"Could not load weather icon: {e}")
            return None

    def update_display(self):
        try:
            # Update time with larger font
            current_time = self.clock_display.get_time()
            self.time_label.config(text=current_time)

            # Update calendar with better formatting
            calendar_text = self.calendar_display.get_calendar()
            self.calendar_label.config(text=calendar_text)

            # Update weather with enhanced layout
            try:
                weather_info = self.weather_service.fetch_weather()
                icon_code = weather_info['current']['weather'][0]['icon']
                weather_description = weather_info['current']['weather'][0]['description'].title()

                photo = self.load_weather_icon(icon_code)
                
                # Clear any unused images
                if hasattr(self, '_last_photo'):
                    del self._last_photo
            
                if photo:
                    self._last_photo = photo  # Keep reference to current photo
                    self.weather_icon_label.config(image=photo)
                    self.weather_icon_label.image = photo
                    self.weatherdesc_label.config(
                        text=f"{weather_description}",
                        compound="top"
                    )

                # Format weather information with symbols
                self.temperature_label.config(
                    text=f"🌡️ {weather_info['current']['temp']}°C (Feels like {weather_info['current']['feels_like']}°C)")
                self.windspeed_label.config(
                    text=f"💨 Wind: {weather_info['current']['wind_speed']} m/s")
                self.humidity_label.config(
                    text=f"💧 Humidity: {weather_info['current']['humidity']}%")

            except Exception as e:
                print(f"Error updating weather: {e}")
        except Exception as e:
            print(f"Error updating display: {e}")
        
        # Increase update interval to reduce CPU usage
        self.after(30000, self.update_display)  # Update every 30 seconds

def main():
    app = DockDisplay()
    app.mainloop()

if __name__ == "__main__":
    main()