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
        import re
        import sys
        import time

        if not file_path:
            print("No file path provided.")
            return

        pattern = re.compile(r'^\[(\d{1,2}\.\d{1,2}\.\d{4}), (\d{2}:\d{2}:\d{2})\] ([^:]+): (.*)')

        try:
            # First, get total line count (to create a loading bar based on %)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            total = len(lines)
            progress = 0
            bar_length = 50  # length of the bar in characters
            last_message = None

            print("Importing chat:")

            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue

                match = pattern.match(line)
                if match:
                    date, time_str, sender, content = match.groups()
                    self.statistics.add_message(sender)
                    self.add_message(date, time_str, sender, content)
                    #sticker, image, video falan countlarını da sayıp onları da göstermek lazım user başına
                    if "Messages and calls are end-to-end encrypted" in content or \
                    "sticker omitted" in content or \
                    "image omitted" in content or \
                    "video omitted" in content or \
                    "audio omitted" in content or \
                    "document omitted" in content:
                        continue
                    last_message = self.head
                    while last_message.next:
                        last_message = last_message.next
                else:
                    if last_message:
                        last_message.content += "\n" + line

                # Update loading bar
                progress = int((i + 1) / total * bar_length)
                bar = "[" + "#" * progress + "-" * (bar_length - progress) + "]"
                sys.stdout.write(f"\r{bar} {int((i + 1) / total * 100)}%")
                sys.stdout.flush()

            print("\nImport complete.")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
    
    def save_to_file(self):
        import json
        import re

        if not json:
            print("JSON module is not available.")
            return

        messages = []
        current = self.head
        first_sender = None

        # Collect messages and get the first sender name
        while current:
            messages.append({
                "date": current.date,
                "time": current.time,
                "sender": current.sender,
                "content": current.content
            })

            if first_sender is None:
                first_sender = current.sender

            current = current.next

        # Sanitize the first sender's name for filename
        def sanitize(name):
            return re.sub(r'[^a-zA-Z0-9_-]', '_', name.strip())[:20] if name else "user"

        sender_name = sanitize(first_sender)
        filename = f"chat_{sender_name}.json"

        users = []
        current = self.statistics.users.head
        while current:
            users.append({
                "name": current.name,
                "message_count": current.message_count
            })
            current = current.next

        data = {
            "messages": messages,
            "statistics": {
                "total_messages": self.statistics.total_messages,
                "users": users
            }
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Chat data saved to '{filename}'")
        except Exception as e:
            print(f"Error saving chat data: {e}")


    
    @classmethod
    def from_json(cls, filename="chat_data.json"):
        import json
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

        chat = cls()

        for msg in data.get("messages", []):
            chat.add_message(msg["date"], msg["time"], msg["sender"], msg["content"])

        for user in data.get("statistics", {}).get("users", []):
            chat.statistics.users.add_or_increment(user["name"])
            current = chat.statistics.users.head
            if current.name == user["name"]:
                current.message_count = user["message_count"]

        chat.statistics.total_messages = data.get("statistics", {}).get("total_messages", 0)

        return chat
    
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
        