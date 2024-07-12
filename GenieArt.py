import irc.bot
import irc.connection
import ssl
from jaraco.stream import buffer
import requests
import json
import time
import urllib.parse

OPENAI_API_KEY = 'PUT API KEY HERE'

def shorten_url(long_url):
    api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(long_url)}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        short_url = response.text
        print(f"Shortened URL: {short_url}")
        return short_url
    except requests.RequestException as e:
        error_msg = f"Error shortening URL: {e} - Status Code: {e.response.status_code if e.response else 'No response'}"
        print(error_msg)
        return long_url, error_msg

class GhostBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6697):
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, connect_factory=factory)
        self.channel = channel

    def on_welcome(self, c, e):
        print("Connected to IRC and joined channel.")
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        message = e.arguments[0]
        nick = e.source.nick
        print(f"Message received in channel: {message}")
        if message.startswith('!image'):
            prompt = message[len('!image '):].strip()
            print(f"Image prompt received: '{prompt}'")
            c.privmsg(self.channel, f"{nick}, I am generating that right now for you.. please hold..")
            self.generate_and_share_image(c, nick, prompt)

    def generate_and_share_image(self, c, nick, prompt):
        headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
        data = {'prompt': prompt, 'n': 1, 'size': '1024x1024'}

        try:
            response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
            response.raise_for_status()

            image_url = response.json()['data'][0]['url']

            short_url, error_msg = shorten_url(image_url)
            if error_msg:
                c.privmsg(self.channel, error_msg)
            else:
                message = f"{nick}, your image is ready: {short_url}"

        except requests.exceptions.HTTPError as http_err:
            message = f"{nick}, failed to generate image. HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as err:
            message = f"{nick}, failed to generate image. Error: {err}"
        except Exception as e:
            message = f"{nick}, an unexpected error occurred: {str(e)}"

        self.send_split_message(c, message)

    def send_split_message(self, c, message):
        max_length = 450 - len(self.channel) - len(":PRIVMSG :")
        if len(message) > max_length:
            parts = [message[i:i + max_length] for i in range(0, len(message), max_length)]
            for part in parts:
                c.privmsg(self.channel, part)
                time.sleep(1)
        else:
            c.privmsg(self.channel, message)

    def on_nicknameinuse(self, c, e):
        new_nick = c.get_nickname() + "_"
        print(f"Nickname in use, changing to {new_nick}")
        c.nick(new_nick)

    def on_disconnect(self, c, e):
        print("Disconnected from IRC. Attempting to reconnect...")
        time.sleep(5)
        self.jump_server()

def main():
    server = "irc.twistednet.org"
    channel = "#twisted"
    nickname = "I"
    bot = GhostBot(channel, nickname, server)
    bot.start()

if __name__ == "__main__":
    main()
