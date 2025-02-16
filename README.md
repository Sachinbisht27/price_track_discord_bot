# Price Tracking Bot with Discord Alert System

## Overview
This is a Python-based price tracking bot that monitors product prices across various e-commerce websites and sends alerts via Discord when a price drop is detected.

## Features
- Scrapes product prices from e-commerce websites.
- Stores and tracks prices over time using SQLite.
- Sends Discord notifications when a price drop is detected.
- Supports multiple product URLs.
- Handles JavaScript-rendered pages using Selenium.
- Modular design for easy expansion to new websites.

## Requirements
- Python 3.12+
- Google Chrome and ChromeDriver
- SQLite3
- Selenium
- WebDriver Manager
- Requests
- PyYAML

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sachinbisht27/price_track_discord_bot.git
   cd price_track_discord_bot
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update `config.yaml` with product URLs and your Discord webhook.

## Usage
1. Initialize the database:
   ```bash
   python3 main.py
   ```
2. The bot will scrape prices and send alerts to Discord if a price drop is detected.

## Configuration
Edit `config.yaml` to specify:
```yaml
products:
  - url: "https://www.amazon.in/example-product"
discord_webhook: "YOUR_DISCORD_WEBHOOK_URL"
```

## Troubleshooting
- Ensure Chrome and ChromeDriver versions are compatible.
- If running on a server, use a headless browser mode.
- Check `prices.db` to verify stored price history.

## License
MIT License

## Contact
For issues or feature requests, open an issue on GitHub or contact Sachin Bisht.
