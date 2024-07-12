# GenieArt README

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Support](#support)

## Introduction

GenieArt is an IRC bot that generates images based on user prompts using the OpenAI API.

## Features

- Connects to IRC servers using SSL.
- Listens for `!image` commands in the channel.
- Generates images using OpenAI API.
- Shortens URLs for easier sharing.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/genieart.git
   cd genieart
   ```

2. Install the required dependencies:
   ```bash
   pip3 install irc
   pip3 install requests
   pip3 install jaraco.stream
   ```

## Configuration

1. Open the `genieart.py` file.
2. Replace `'PUT API KEY HERE'` with your OpenAI API key.
3. To change the IRC network and channel, modify the following lines in the `main` function:
   ```python
   server = "irc.twistednet.org"  # Change to your desired IRC server
   channel = "#twisted"           # Change to your desired channel
   nickname = "I"                 # Change to your desired nickname
   ```

## Usage

1. Run the bot:
   ```bash
   python3 genieart.py
   ```

2. To keep the bot running in the background using `screen`:
   ```bash
   screen -S genieart
   python3 genieart.py
   ```

   To detach from the screen session, press `Ctrl + A` then `D`.

   To reattach to the screen session:
   ```bash
   screen -r genieart
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

Visit us at [irc.twistednet.org](irc://irc.twistednet.org) channel [#dev](irc://irc.twistednet.org/#dev) for help or to say hello.
