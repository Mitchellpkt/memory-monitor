import time
from tkinter import Tk, Label
from typing import NoReturn

import psutil
from loguru import logger


def popup_error_message(message: str) -> None:
    """
    Displays a popup window with an error message.

    :param message: The error message to display.
    """
    root = Tk()
    root.title("Memory Alert")
    label = Label(root, text=message, padx=50, pady=20)
    label.pack()
    # Center the window on the screen
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
    root.geometry(f"+{position_right}+{position_down}")
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()


def check_memory_threshold(threshold_prct: float = 30.0, check_frequency_sec: float = 60) -> NoReturn:
    """
    Continuously checks the system's free memory percentage and displays a
    popup window with an error message if it falls below a specified threshold.

    :param threshold_prct: The minimum acceptable free memory percentage.
    :param check_frequency_sec: Frequency of memory check in seconds.
    """
    while True:
        memory_used = psutil.virtual_memory().percent
        if memory_used > threshold_prct:
            message: str = f"Memory usage is at {memory_used}% (> {threshold_prct}% threshold)"
            popup_error_message(message)
        logger.info(f"Memory usage is at {memory_used}%")
        time.sleep(check_frequency_sec)


if __name__ == "__main__":
    logger.add("memory_monitor.log", rotation="10 MB")  # Configure logger to write to file
    check_memory_threshold(threshold_prct=75, check_frequency_sec=60)  # Set your desired threshold here
