# ChatAchievementsBot

1. pip install -r requirements.txt
2. Install [postgres](https://www.postgresql.org)
3. Create database
4. Create 'config.json' in the project root
```json
{
  "token": "TELEGRAM_BOT_TOKEN",
  "database": "YOUR_DATABASE",
  "user": "POSTGRES_USER",
  "password": "POSTGRES_USER_PASSWORD"
}
```

Now 
```python 
python run_bot.py # to run telegram bot
python run_server.py # to run flask server on localhost:5000
```
