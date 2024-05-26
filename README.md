### This bot is currently abandoned and with no recent contributions, it is a framework for you to create your own and improve them in the near future

# Discord Bot for Capturing Yews.News Screenshots

This project is a Discord bot that periodically generates URLs for the `yews.news` website, captures screenshots of these URLs using Selenium, and sends these screenshots to a specified Discord channel. The bot is set up to generate URLs and take screenshots at specific times throughout the day.

## Features

- Generates URLs for `yews.news` based on the current date and time.
- Uses Selenium to capture screenshots of the generated URLs.
- Sends the screenshots to a specified Discord channel and mentions a target role.
- Runs periodic tasks to ensure URLs are generated and screenshots are taken at the correct times.
- For this bot to work, it has to be active 24/7

## Requirements

- Python 3.7 or higher
- Discord.py
- Selenium
- Requests
- BeautifulSoup
- Pytz
- Chrome WebDriver

## Setup

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
