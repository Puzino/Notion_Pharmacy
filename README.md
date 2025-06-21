# 💊 Telegram Pharmacy Notion Bot

Telegram bot that helps manage and structure medical data in Notion. Built using [Aiogram](https://docs.aiogram.dev), integrated with Notion API, and containerized with Docker.

---

## 🚀 Features

- 📦 Add, update, and delete pharmacy items via Telegram
- 🗂 Sync structured data to Notion databases
- 📅 Handle expiration dates and quantity tracking

---

## 📁 Project Structure
```
Notion_Pharmacy/
    ├── aiogram_run.py          # Main bot launcher
    ├── handlers/               # Aiogram handlers
    ├── keyboards/              # Aiogram keyboards
    ├── notion/                 # Communication with Notion API
    ├── utils/                  # Helper functions
    ├── requirements.txt        # Python dependencies
    ├── requirements_flake8.txt # Flake 8 dependencies
    ├── .env                    # Environment variables
    ├── .dockerignore           # Docker ignore
    ├── .flake8                 # Flake 8 Settings
    ├── .env.example            # Example of a .env file (rename to .env to use)
    ├── docker-compose.yaml     # Docker-compose file
    └── Dockerfile              # Docker build instructions
```
---

## 🛠 Get notion API database id and secret token.
To use Notion as a database, you will need to create a [Notion account](https://www.notion.com), create an inline database, specify fields, and then obtain a secret token for your account and database.
1. Create an account
2. Create a database
3. [Create an integration](https://www.notion.so/profile/integrations)
4. Database ID - go to your database page in Notion and copy the part of the link:
<img src="https://files.readme.io/7e8a54d-notion-page-url.png">

#### Links that may help:
- [Build your first integration](https://developers.notion.com/docs/create-a-notion-integration)

## 🛠 Installation

### 🔹 1. Clone the repository

```bash
git clone https://github.com/Puzino/Notion_Pharmacy.git
cd Notion_Pharmacy
```

### 🔹 2. Set up .env
Create a `.env` file with the following variables:

Use `.env.example` to understand which fields you need and rename to `.env`.
```text
TOKEN=          # Telegram bot father token
NOTION_TOKEN=   # Notion secret token
DATABASE_ID=    # Notion database id/page id
TIME_ZONE=      # Your time zone
USERS=          # Which users should be sent a message about the expiration date
```

### 🔹 3. Build and run with Docker
```bash
docker build -t telegram-notion-bot .
docker run --env-file .env telegram-notion-bot
```
#### 🔹 or use docker-compose

```bash
docker-compose up --build
```

### 🧰 Tech Stack
* Python 3.12
* Aiogram
* Notion API - notion-client
* Docker / Docker Compose
* APScheduler


### 🐝 License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it.