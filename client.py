import socket
import protocol
import os

SERVER_ADDR = ("127.0.0.1", 9090)
DOWNLOAD_DIR = ".venv/downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


def send_request(command, **kwargs):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDR)

    request_data = {"command": command, **kwargs}
    encoded_request = protocol.encode_message(request_data)
    client.send(encoded_request.encode())

    response = protocol.receive_full_message(client)
    decoded_response = protocol.decode_message(response)

    if decoded_response:
        return(decoded_response)
    else:
        print("\nResponse: Integrity check failed")

    client.close()

def upload_python_file():
    filepath = input("Enter the path of the Python file to upload: ").strip()

    if not os.path.exists(filepath):
        print("Error: File not found!")
        return

    filename = os.path.basename(filepath)
    with open(filepath, "r") as f:
        file_content = f.read()

    response = send_request("upload_file", filename=filename, file_content=file_content)
    print(response)

def upload_any_file():
    filepath = input("Enter the path of the file to upload: ").strip()

    if not os.path.exists(filepath):
        print("Error: File not found!")
        return

    with open(filepath, "rb") as f:
        file_content = f.read()

    response = send_request("upload_any_file", path=filepath, file_content=file_content)
    print(response)

def download_file():
    try:
        path = input("Enter the file path to download: ").strip()
        response = send_request("download_file", path=path)
        print(response["result"])
        decoded_file = base64.decode(response["result"])
        print(decoded_file)
        path = "downloads/"+response["file_name"]
        with open(path, "wb") as file:
            file.write(decoded_file)
            print(f"File was uploaded to {path}")
    except Exception as e:
        print(f"Error: {e}")


def execute_function():
    func_name = input("Enter function name to execute: ").strip()
    args_input = input("Enter arguments (comma-separated): ").strip()

    args = [arg.strip() for arg in args_input.split(",")] if args_input else []

    send_request("execute_function", function=func_name, args=args)

def show_directory_contents():
    dir_path = input("Enter directory path to list contents: ").strip()
    send_request("show_dir_content", dir_path=dir_path)

def take_screenshot():
    send_request("take_screenshot")

def show_help():
    send_request("help")

def interactive_menu():
    while True:
        print("\n================= Remote Client =================")
        print("1. Help (Show available functions)")
        print("2. Upload Python File to Add Function")
        print("3. Execute a Function")
        print("4. Upload Any File")
        print("5. Download a File")
        print("6. Show Directory Content")
        print("7. Take a Screenshot")
        print("8. Exit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            show_help()
        elif choice == "2":
            upload_python_file()
        elif choice == "3":
            execute_function()
        elif choice == "4":
            upload_any_file()
        elif choice == "5":
            download_file()
        elif choice == "6":
            show_directory_contents()
        elif choice == "7":
            take_screenshot()
        elif choice == "8":
            print("Exiting client.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    interactive_menu()
