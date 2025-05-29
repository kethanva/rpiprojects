class ClockDisplay:
    def get_time(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
        return current_time
