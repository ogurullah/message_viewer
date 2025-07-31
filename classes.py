#classes.py

class Statistics:
    def __init__(self):
        self.total_messages = 0
        self.users = UserList()

    def add_message(self, sender):
        self.total_messages += 1
        self.users.add_or_increment(sender)

    def display_statistics(self):
        print(f"Total Messages: {self.total_messages}")
        
        current = self.users.head
        while current:
            print(f"    {current.name}: {current.message_count} messages")
            current = current.next

        user_names = []
        current = self.users.head
        while current:
            user_names.append(f"'{current.name}'")
            current = current.next
        print(f"Total Users: {self.users.total_users()}, {', '.join(user_names)}")


class User:
    def __init__(self, name):
        self.name = str(name)
        self.message_count = 0
        self.next = None

class UserList:
    def __init__(self):
        self.head = None

    def add_or_increment(self, sender):
        current = self.head
        while current:
            if current.name == sender:
                current.message_count += 1
                return
            current = current.next
        
        new_user = User(sender)
        new_user.next = self.head
        self.head = new_user

    def total_users(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        current = self.head
        while current:
            print(f"{current.name}: {current.message_count} messages")
            current = current.next

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
        self.statistics = Statistics()

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
                    self.statistics.add_message(sender)
                    self.add_message(date, time, sender, content)
                    if "Messages and calls are end-to-end encrypted" in content or "sticker omitted" in content or "image omitted" in content:
                        continue
                    last_message = self.head
                    while last_message.next:
                        last_message = last_message.next
                else:
                    if last_message:
                        last_message.content += "\n" + line
    
    def get_file_directory(self):
        
        import tkinter as tk
        import time
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select WhatsApp Chat File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not file_path:
            print("No file selected.")
            return None
        else:
            return file_path
        