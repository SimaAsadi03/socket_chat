def process_message(message: str) -> str:
    # بررسی پیام خاص "hello server!" و پاسخ خاص "Hello client!"
    if message.lower().strip() == "hello server":
        return "Hello client!"
    
    # در غیر این صورت، پیام عمومی می‌دهیم
    return "Message received: " + message
