import requests
import os
import time
import re
from telegram import Bot
from telegram.error import TelegramError

# Telegram Bot setup
TOKEN = '5521602743:AAHC6uMihsTOhay7-gFepx16srEyxi0LNEc'  # Replace with your Bot API Token
CHANNEL_ID = '@ssconlinee'  # Replace with your Telegram Channel ID

# Path to the TXT file containing the links
TXT_FILE_PATH = 'Course.txt'  # Path to the .txt file with links

# Initialize Telegram bot
bot = Bot(token=TOKEN)

def download_file(url, file_name):
    """Downloads a file from a given URL and saves it with the specified file name."""
    try:
        print(f"Downloading: {file_name}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {file_name}")
        return file_name
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {file_name}: {e}")
        return None

def upload_to_telegram(file_path, title):
    """Uploads the downloaded file to Telegram channel."""
    try:
        print(f"Uploading {title} to Telegram channel...")
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=CHANNEL_ID, document=file,
                              caption=f"╭━━━━━━━━━━━╮\n💫 𝐕ɪᴅᴇᴏ 𝐈𝐃 : 078\n╰━━━━━━━━━━━╯\n"
                                      f"📁𝐓ɪᴛ𝗅𝗘 : {title}\n\n"
                                      f"📚𝐂ᴏᴜʀꜱᴇ : Champions 19.0 Maths Special LIVE Batch\n"
                                      f"📥𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗱 𝗕𝘆 : ShieldedSaver❤️")
        print(f"Uploaded: {title}")
    except TelegramError as e:
        print(f"Error uploading {title}: {e}")

def parse_links_from_txt(txt_file_path):
    """Reads the links from the TXT file and returns a list of dictionaries with title and URL."""
    links = []
    with open(txt_file_path, 'r') as file:
        for line in file:
            match = re.match(r"(.*?)\s(.*?):\s(https?://[^\s]+)", line.strip())
            if match:
                title, desc, url = match.groups()
                links.append({"title": f"{desc} ({title.strip('[]')})", "url": url, "type": "video" if url.endswith(('.mp4', '.mkv')) else "pdf"})
    return links

def main():
    links = parse_links_from_txt(TXT_FILE_PATH)
    for content in links:
        title = content["title"]
        url = content["url"]
        file_type = content["type"]

        # Create file name based on content type
        file_name = f"{title}.{file_type}"

        # Download the file
        downloaded_file = download_file(url, file_name)

        if downloaded_file:
            # Upload the file to Telegram
            upload_to_telegram(downloaded_file, title)

            # Remove the downloaded file after upload
            os.remove(downloaded_file)
            print(f"Deleted the file: {downloaded_file}")

            # Wait before proceeding to the next item
            time.sleep(2)

if __name__ == "__main__":
    main()