import subprocess
import sys
import pyttsx3
import asyncio
import threading
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry

def install(package):
    """
    Install a Python package using pip.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def validate_choice(choice, max_value):
    """
    Validate user's choice input.
    """
    try:
        choice = int(choice)
        if choice < 0 or choice >= max_value:
            raise ValueError
        return choice
    except ValueError:
        print("Invalid choice. Please try again.")
        return None

def validate_speed(speed):
    """
    Validate user's speed input.
    """
    try:
        speed = int(speed)
        if speed <= 0:
            raise ValueError
        return speed
    except ValueError:
        print("Invalid speed. Please enter a positive integer.")
        return None

async def speak_text(engine, text, status_label):
    """
    Speak the text entered by the user.
    """
    if text:
        engine.say(text)
        engine.runAndWait()
        status_label.configure(text="Text spoken")
    else:
        status_label.configure(text="Please enter text")

def change_voice(voices, engine):
    """
    Change the voice used for text-to-speech.
    """
    for i, voice in enumerate(voices):
        print(f"{i}. {voice.name}")
    choice = input("Choose a voice: ")
    choice = validate_choice(choice, len(voices))
    if choice is not None:
        engine.setProperty('voice', voices[choice].id)

def change_speed(engine):
    """
    Change the speed of text-to-speech.
    """
    speed = input("Enter new speed (default is 200): ")
    speed = validate_speed(speed)
    if speed is not None:
        engine.setProperty('rate', speed)

class TextToSpeechGUI:
    """
    A GUI application for text-to-speech conversion.
    """

    def __init__(self, master):
        """
        Initialize the TextToSpeechGUI class.
        """
        self.master = master
        master.title("Text-to-Speech")
        master.geometry("500x400")

        self.engine = pyttsx3.init()

        self.text_entry = CTkEntry(master, width=40)
        self.text_entry.pack(pady=10)

        self.speak_button = CTkButton(master, text="Speak", command=self.speak_text)
        self.speak_button.pack(pady=10)

        self.change_voice_button = CTkButton(master, text="Change Voice", command=self.change_voice)
        self.change_voice_button.pack(pady=10)

        self.change_speed_button = CTkButton(master, text="Change Speed", command=self.change_speed)
        self.change_speed_button.pack(pady=10)

        self.exit_button = CTkButton(master, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

        self.status_label = CTkLabel(master, text="Ready")
        self.status_label.pack(pady=10)

    def speak_text(self):
        """
        Start a new thread to speak the text entered by the user.
        """
        text = self.text_entry.get()
        if text:
            threading.Thread(target=self.speak_text_thread, args=(text,)).start()
        else:
            self.status_label.configure(text="Please enter text")

    def speak_text_thread(self, text):
        """
        Thread function to speak the text entered by the user.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speak_text(self.engine, text, self.status_label))
        loop.close()

    def change_voice(self):
        """
        Start a new thread to change the voice used for text-to-speech.
        """
        threading.Thread(target=self.change_voice_thread).start()

    def change_voice_thread(self):
        """
        Thread function to change the voice used for text-to-speech.
        """
        voices = self.engine.getProperty('voices')
        change_voice(voices, self.engine)

    def change_speed(self):
        """
        Start a new thread to change the speed of text-to-speech.
        """
        threading.Thread(target=self.change_speed_thread).start()

    def change_speed_thread(self):
        """
        Thread function to change the speed of text-to-speech.
        """
        change_speed(self.engine)

    def exit_program(self):
        """
        Stop the text-to-speech engine and exit the program.
        """
        self.engine.stop()
        self.master.destroy()

if __name__ == "__main__":
    root = CTk()
    root.configure(theme="dark")
    app = TextToSpeechGUI(root)
    root.mainloop()