import json
import hashlib
import base64

DELIMITER = "<END>"

def encode_message(data):
    json_data = json.dumps(data)
    hash_value = hashlib.sha256(json_data.encode()).hexdigest()
    full_message = json.dumps({"hash": hash_value, "data": data})
    return base64.b64encode(full_message.encode()).decode() + DELIMITER


def decode_message(encoded_message):
    try:
        message = base64.b64decode(encoded_message).decode()
        message_dict = json.loads(message)
        received_hash = message_dict.get("hash")
        data = message_dict.get("data")

        # Verify integrity
        if hashlib.sha256(json.dumps(data).encode()).hexdigest() != received_hash:
            print("Error: Message integrity check failed.")
            return None

        return data
    except Exception as e:
        print(f"Error decoding message: {e}")
        return None


def receive_full_message(client_socket):
    message = ""
    while True:
        chunk = client_socket.recv(1024).decode()
        message += chunk
        if DELIMITER in message:
            break
    return message.replace(DELIMITER, "")
