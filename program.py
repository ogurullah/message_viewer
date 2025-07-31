# program.py

from classes import Chat

if __name__ == "__main__":
    print("Welcome to the Whatsapp Chat Viewer!")
    should_exit = False
    while not should_exit:
        user_input = input("Press 1 to initialize the program. Press 0 to exit.")
        if user_input == "0":
            should_exit = True
        elif user_input != "1":
            print("Invalid input. Please try again.")
            user_input = input()
        elif user_input == "1":
            print("Initializing the program.", end="")
            import time
            print(".", end="")
            chat = Chat()
            print(".",)
            print("Program initialized successfully!")
            print("Please select the .txt file you exported from Whatsapp in the following file explorer window", end="")
            for i in range(3):  #change it so that window appears on user input, not automatically
                time.sleep(1)
                print(".", end="", flush=True)
            file_directory = chat.get_file_directory()
            print("\nFile explorer window opened!") #this shows after the file explorer window is opened, fix it
            if file_directory:
                print(f"Selected file: {file_directory}")
                print("This may take a while depending on the size of your chat file.")
                start = "no"
                while start != "yes":
                    start = input("Do you want to import now? Type 'yes' to start, 'no' to wait or 'exit' to quit: ").lower()
                    if start == "yes":
                        chat.import_from_whatsapp(file_directory)
                    elif start == "no":
                        print("Okay. You can type 'yes' when you're ready or 'exit' to quit.")
                        continue
                    elif start == "exit":
                        print("Exiting the program.")
                        should_exit = True
                        break
                    else:
                        print("Invalid input. Please type 'yes', 'no' or 'exit'.")
                while not should_exit:
                    print("\nWhat would you like to do?")
                    print("1. Display chat messages")
                    print("2. Display user statistics")
                    print("3. Exit the program")
                    choice = input("Enter your choice (1/2/3): ")
                    if choice == "1":
                        show_details = input("Do you want to see message details? (yes/no): ").lower() == "yes"
                        chat.display_chat(show_details)
                    elif choice == "2":
                        chat.statistics.display_statistics()
                    elif choice == "3":
                        should_exit = True
                    else:
                        print("Invalid choice. Please try again.")
    print("Exiting the program. Thank you for using Whatsapp Chat Viewer!")

