## Project Setup
The script sends new job postings to a Telegram chat associated with the bot, so to test the code you will need to set up your own bot.

To create a new bot and obtain its token:
- Contact @BotFather on Telegram.
- Send it the /newbot command.
- Provide a display name and a unique username for your bot when asked.

You will get a token of the form: 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw.

To get the chat ID of your bot:
- Contact @idbot.
- Send it the bot’s username.

Place the token and chat ID inside a .env file:
```env
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```
Next, initialize the virtual environment and install dependencies:
<details>
<summary><b>macOS</b></summary>

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```
</details>

<details>
<summary><b>Windows</b></summary>

```bash
py -m venv venv && .\venv\Scripts\pip install -r requirements.txt
```
</details>

## Running the script
```bash
python scrape.py
```