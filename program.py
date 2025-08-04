from classes import Chat
import time

def main():
    print("Welcome to the Whatsapp Chat Viewer!")

    print("1. Import new .txt file")
    print("2. Load from saved .json")
    choice = input("Enter your choice (1/2): ").strip()

    chat = None
    if choice == "1":
        chat = Chat()
        print("Opening file explorer...")
        file_directory = chat.get_file_directory()
        if not file_directory:
            print("No file selected. Exiting.")
            return

        print(f"Selected file: {file_directory}")
        confirm = input("Do you want to import now? (yes/no): ").lower().strip()
        if confirm == "yes":
            chat.import_from_whatsapp(file_directory)
            print("Chat imported successfully.")
        else:
            print("Import canceled. Exiting.")
            return

    elif choice == "2":
        chat = Chat.from_json()
        if chat:
            print("Chat loaded successfully from file.")
        else:
            print("Failed to load chat. Exiting.")
            return
    else:
        print("Invalid input. Exiting.")
        return

    while True:
        print("\nWhat would you like to do?")
        print("1. Display chat messages")
        print("2. Display user statistics")
        print("3. Export chat to file")
        print("4. Exit the program")
        action = input("Enter your choice (1/2/3/4): ").strip()

        if action == "1":
            show_details = input("Do you want to see message details? (yes/no): ").lower().strip() == "yes"
            chat.display_chat(show_details)
        elif action == "2":
            chat.statistics.display_statistics()
        elif action == "3":
            chat.save_to_file()
        elif action == "4":
            print("Exiting the program. Thank you for using Whatsapp Chat Viewer!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
