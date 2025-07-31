#classes.py

class User:
    def __init__(self, name):
        self.name = str(name)
        self.next = None

class Message:
    def __init__(self, date, time, sender, content):
        self.date = str(date)
        self.time = str(time)
        self.sender = str(sender)
        self.content = str(content)
        self.next = None

class Chat:
    def __init__(self):
        self.head = None

    def add_message(self, date, time, sender, content):
        new_message = Message(date, time, sender, content)
        if not self.head:
            self.head = new_message
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_message

    def display_chat(self, show_details=True):
        current = self.head
        if show_details == True:
            while current:
                print(f"[{current.date}] [{current.time}] {current.sender}: {current.content}")
                current = current.next
        else:
            while current:
                print(f"{current.sender}: {current.content}")
                current = current.next

    def import_from_whatsapp(self, file_path):
        if not file_path:
            print("No file path provided.")
            return
        
        import re
        pattern = re.compile(r'^\[(\d{1,2}\.\d{1,2}\.\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)')

        with open(file_path, 'r', encoding='utf-8') as file:
            last_message = None
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                match = pattern.match(line)
                if match:
                    date, time, sender, content = match.groups()
                    self.add_message(date, time, sender, content)
                    if "Messages and calls are end-to-end encrypted" in content or "sticker omitted" in content:
                        continue
                    last_message = self.head
                    while last_message.next:
                        last_message = last_message.next
                else:
                    # if it's a continuation of the previous message (multi-line message)
                    if last_message:
                        last_message.content += "\n" + line
    
    def get_file_directory(self):
        
        import tkinter as tk
        import time
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw() # Hide the root window
        file_path = filedialog.askopenfilename(
            title="Select WhatsApp Chat File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            print("No file selected.")
            return None
        else:
            return file_path
        
    def add_user(self, name):
        new_user = User(name)
        if not self.head:
            self.head = new_user
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_user
    
    def check_user(self, name):
        current = self.head
        while current:
            if current.name == name:
                return True
            current = current.next
        return False
