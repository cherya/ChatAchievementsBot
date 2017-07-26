# ChatAchievementsBot
### Installation
1. pip install -r requirements.txt
2. Install postgres
3. Create database
4. Create 'config.json' in the project root
```json
{
  "token": "TELEGRAM_BOT_TOKEN",
  "listen_chats": ["CHATS_TO_LISTEN"],
  "log_chat": "CHAT_TO_LOG",
  "database": "YOUR_DATABASE",
  "user": "POSTGRES_USER",
  "password": "POSTGRES_USER_PASSWORD"
}
```
##### Note
- If listen_chats is not specified bot will listen every message from every chat
- If log_chat is not specified log will be printed to stdout

Then
```
python run.py --bot # to run telegram bot
python run.py --server # to run flask server on localhost:5000
```

#### Live demo: http://addmeto.cherya.xyz
