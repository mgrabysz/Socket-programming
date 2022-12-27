from messages import Register_message

if __name__ == "__main__":
    message = Register_message(2, 20)
    print(message.to_json())