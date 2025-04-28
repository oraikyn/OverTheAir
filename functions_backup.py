import os
from PIL import ImageGrab


class ScreenshotCounter:
    COUNT = 1

    @staticmethod
    def take_screenshot():
        filename = f"screenshot{ScreenshotCounter.COUNT}.png"
        ScreenshotCounter.COUNT += 1  # Increment static variable
        return str(filename)  # Return screenshot filename

def take_screenshot():
    name = ScreenshotCounter.take_screenshot()
    screenshot = ImageGrab.grab()
    screenshot.save(name)
    screenshot.close()
    with open(name, "rb") as screenshot_file:
        screenshot_data = screenshot_file.read()
    return screenshot_data, name  # Return the binary screenshot data

def upload_file(data, path):
    if os.path.exists(path):
        return "Error: Path already exists."
    with open(path, "wb") as file:
        file.write(data)
        return f"File was uploaded to {path}"

def download_file(path):
    if not os.path.exists(path):
        return "Error: Path does not exist"
    with open(path, "rb") as file:
        file_data = file.read()
    return file_data  # Return file data for download

def show_dir_content(dir_path):
    if not os.path.exists(dir_path):
        return "Error: Path does not exist"
    files = os.listdir(dir_path)
    return "Directory content: " + ", ".join(files)

def list_functions():
    """ Returns a list of available functions in functions.py. """
    return [
        "take_screenshot() - Takes a screenshot and returns the image file.",
        "upload_file(data, path) - Uploads a file to the specified path.",
        "download_file(path) - Downloads a file from the specified path.",
        "show_dir_content(dir_path) - Lists the contents of a directory."
    ]


def wow(name):
    return "" + name + " is great!"

def wow(name):
    print(name + "is great!")

def wow(name):
    print(name + "is great!")

def wow(name):
    print(name + "is great!")
