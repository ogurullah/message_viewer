# program.py

from classes import Chat

if __name__ == "__main__":
    chat = Chat()
    file_directory = chat.get_file_directory()

    if file_directory:
        chat.import_from_whatsapp(file_directory)
        chat.display_chat(show_details=False)
