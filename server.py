import base64
import socket
import threading
import importlib
import os
import shutil
import protocol
from functions import *

SERVER_ADDR = ("0.0.0.0", 9090)
FUNCTIONS_FILE = "functions.py"
BACKUP_FILE = "functions_backup.py"
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def backup_functions():
    if os.path.exists(FUNCTIONS_FILE):
        shutil.copy(FUNCTIONS_FILE, BACKUP_FILE)


def restore_backup():
    if os.path.exists(BACKUP_FILE):
        shutil.copy(BACKUP_FILE, FUNCTIONS_FILE)
        importlib.invalidate_caches()


def load_functions():
    try:
        import functions
        importlib.reload(functions)
        backup_functions()
        return functions
    except Exception as e:
        print(f"Error loading functions.py: {e}")
        restore_backup()
        import functions
        importlib.reload(functions)
        return functions


def add_function_from_file(filepath):
    try:
        with open(filepath, "r") as f:
            code = f.read()

        compile(code, FUNCTIONS_FILE, 'exec')

        with open(FUNCTIONS_FILE, "a") as f:
            f.write("\n" + code + "\n")

        load_functions()
        return True
    except SyntaxError as e:
        print(f"Syntax error in provided file: {e}")
        return False


def handle_client(client_socket):
    while True:
        try:
            message = protocol.receive_full_message(client_socket)
            if not message:
                break

            data = protocol.decode_message(message)
            if data is None:
                client_socket.send(protocol.encode_message({"error": "Message integrity check failed"}).encode())
                break

            command = data.get("command")

            if command == "help":
                response = {"result": list_functions()}

            elif command == "upload_file":
                filename = data.get("filename")
                file_content = data.get("file_content")
                if filename and file_content:
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    with open(FUNCTIONS_FILE, "w") as f:
                        f.write(file_content)

                    success = add_function_from_file(filepath)
                    response = {"result": "Function added successfully"} if success else {"error": "Failed to add function"}
                else:
                    response = {"error": "Invalid file data"}

            elif command == "execute_function":
                func_name = data.get("function")
                args = data.get("args", [])
                functions = load_functions()

                if functions is None:
                    response = {"error": "functions module not found"}
                else:
                    func = getattr(functions, func_name, None)
                    if func:
                        result = func(*args)
                        response = {"result": result}
                    else:
                        response = {"error": "Function not found"}

            elif command == "upload_any_file":
                path = data.get("path")
                file_content = data.get("file_content")
                response = {"result": upload_file(file_content, path)}

            elif command == "download_file":
                path = data.get("path")
                file_data = download_file(path)
                response = {"result": base64.encode(file_data.decode()), "file_name": os.path.basename(path)}

            elif command == "show_dir_content":
                dir_path = data.get("dir_path")
                response = {"result": show_dir_content(dir_path)}

            elif command == "take_screenshot":
                screenshot_data, name = take_screenshot()
                response = {"result": "Screenshot saved as " + name}

            else:
                response = {"error": "Unknown command"}

            client_socket.send(protocol.encode_message(response).encode())

        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.send(protocol.encode_message({"error": "Error executing function"}).encode())
            break

    client_socket.close()


def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDR)
    server.listen(5)
    print("Server listening on port 9090")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    backup_functions()
    server_loop()
