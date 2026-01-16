# Order-Akun-TeleBot

A Telegram bot for managing and restocking user accounts with role-based access control.

## Features

- **Account Management**: Store and organize accounts by username
- **Role-Based Access**: Owner and selected users can restock accounts
- **Stock Tracking**: View total stocked accounts per username
- **Command Help**: Dynamic help command showing available commands based on user permissions

## Prerequisites

- Python 3.8+
- python-telegram-bot library
- python-dotenv library

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Order-Akun-TeleBot
```

2. Install dependencies:
```bash
pip install python-telegram-bot python-dotenv
```

3. Create a `.env` file in the project root:
```env
TELEGRAM_TOKEN=your_bot_token_here
OWNER_ID=your_telegram_user_id
ALLOWED_USERS=user_id_1,user_id_2,user_id_3
```

4. Run the bot:
```bash
python bot.py
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Telegram bot API token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `OWNER_ID` | Telegram user ID of the owner | `123456789` |
| `ALLOWED_USERS` | Comma-separated list of user IDs with restock access | `987654321,111111111,222222222` |

## Commands

### `/start`
Displays a welcome message to start using the bot.

**Usage**: `/start`

### `/help`
Shows all available commands based on user permissions. Owner and allowed users will see the `/restock` command, while other users won't.

**Usage**: `/help`

### `/restock` *(Owner & Allowed Users Only)*
Adds a new account to the database.

**Usage**: `/restock <email> <username> <password>`

**Example**: `/restock user@example.com john123 pass123`

**Permissions**: Only the owner and users in `ALLOWED_USERS` can use this command.

### `/accounts`
Lists all stocked accounts grouped by username with total account count.

**Usage**: `/accounts`

**Output**: Shows username and total number of accounts for each user.

## Project Structure

```
Order-Akun-TeleBot/
├── bot.py                 # Main bot application
├── config.py              # Configuration and environment variables
├── db.py                  # Database operations (SQLite)
├── commands/              # Command handlers
│   ├── __init__.py
│   ├── start.py          # /start command
│   ├── help.py           # /help command
│   ├── restock.py        # /restock command
│   └── accounts.py       # /accounts command
├── .env                   # Environment variables (not in git)
├── .gitignore             # Git ignore file
├── accounts.db            # SQLite database (auto-created)
└── README.md              # This file
```

## Database

The bot uses SQLite for account storage. The database is automatically created on first run.

### Database Schema

**Table: `accounts`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| email | TEXT | Account email |
| username | TEXT | Account username |
| password | TEXT | Account password |

## How It Works

1. **Command Loading**: The `bot.py` scans the `commands/` directory and dynamically loads all command handlers.
2. **Permission Check**: The `/restock` command checks if the user is in the `RESTOCK_ALLOWED` list before executing.
3. **Dynamic Help**: The `/help` command filters commands based on user permissions.
4. **Account Grouping**: The `/accounts` command groups accounts by username and displays the count.

## Configuration

### Adding New Users with Restock Access

Edit your `.env` file and add user IDs to `ALLOWED_USERS`:

```env
ALLOWED_USERS=987654321,111111111,222222222
```

Then restart the bot.

## Error Handling

- Missing arguments in commands will show usage instructions
- Unauthorized users trying to use `/restock` will receive a permission denied message
- Database errors are caught and reported to the user
- Invalid environment variables default to empty values

## Security Considerations

- Never commit `.env` file to version control
- Use environment variables for sensitive data (tokens, IDs)
- Passwords are stored in plain text (consider encryption for production)
- Validate and sanitize user inputs

## Troubleshooting

### Bot not responding
- Check if `TELEGRAM_TOKEN` is correct
- Ensure the bot is polling: `python bot.py`
- Check internet connection

### Command not working
- Verify user ID is in `ALLOWED_USERS` for `/restock`
- Check correct command syntax
- Review `.env` file configuration

### Database errors
- Ensure `accounts.db` file is not locked by another process
- Check write permissions in the project directory
- Delete `accounts.db` to reset the database

## Contributing

Feel free to modify and extend the bot functionality by adding new commands in the `commands/` directory.

## License

Add your license information here.
