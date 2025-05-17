# Instagram Engagement AI Bot

An AI-powered Instagram engagement bot that automates interactions with targeted users in your niche to grow your account organically.

## Features

- 🔍 **Smart Hashtag Scraping**: Find relevant content using your target hashtags
- 👥 **User Analysis**: Identify and filter potential followers based on engagement patterns
- 💬 **AI Comment Generation**: Create contextual, personalized comments using GPT-4
- 📊 **Engagement Dashboard**: Track all activities and growth metrics
- ⏱️ **Scheduled Interactions**: Automated likes, comments, and follows at optimal times
- 🗄️ **Persistent Storage**: All data saved in Supabase for analysis and tracking

## System Requirements

- Python 3.8+
- Node.js 16+
- MongoDB
- Supabase account
- OpenAI API key
- Instagram account

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/instagram-engagement-bot.git
cd instagram-engagement-bot
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## Configuration

### 1. Backend Configuration

Create a `.env` file in the `backend` directory with the following content:

```
MONGO_URL="mongodb://localhost:27017"
DB_NAME="instagram_bot_db"

# Instagram Credentials
INSTAGRAM_USERNAME="your_instagram_username"
INSTAGRAM_PASSWORD="your_instagram_password"

# OpenAI API Key
OPENAI_API_KEY="your_openai_api_key"

# Supabase Configuration
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_key"

# Bot Configuration
MAX_POSTS_PER_HASHTAG=10
MAX_USERS_PER_DAY=10
MIN_FOLLOWER_COUNT_REGULAR=100
MIN_FOLLOWER_COUNT_INFLUENCER=500
TARGET_HASHTAGS="#facts,#motivation,#brainfacts,#brain,#braincoach,#brainnourishment,#hacks,#motivationhacks"
```

### 2. Frontend Configuration

Create a `.env` file in the `frontend` directory with the following content:

```
REACT_APP_BACKEND_URL="http://localhost:8001"
```

## Running the Application

### 1. Start MongoDB

Make sure MongoDB is running on your local machine (default port 27017).

```bash
# Example for starting MongoDB on Linux/Mac
mongod --dbpath=/path/to/your/data/directory
```

### 2. Start the Backend

```bash
# Navigate to backend directory
cd backend

# Activate the virtual environment if not already activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the server
python server.py
```

The backend will be running at http://localhost:8001

### 3. Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Start the development server
npm start
```

The frontend will be available at http://localhost:3000

## Usage

### 1. Configure Your Bot

1. Log in to the dashboard at http://localhost:3000
2. Go to the Settings page to enter your Instagram credentials, OpenAI API key, and Supabase details
3. Customize your target hashtags and engagement parameters

### 2. Start Scraping

1. On the Dashboard, click "Start Scraping" to begin collecting posts and users from your target hashtags
2. The bot will run in the background and populate your database with potential engagement targets

### 3. Enable Scheduler

1. Click "Start Scheduler" to begin the automated engagement process
2. The bot will now automatically like, comment, and follow users according to your settings
3. Monitor the activity on the Dashboard and Engagement History pages

### 4. Analyze and Refine

1. Use the analytics to identify which hashtags and engagement strategies are most effective
2. Adjust your target hashtags and parameters as needed to optimize results

## Important Notes

- **Instagram Rate Limits**: Be careful not to exceed Instagram's rate limits (approximately 100-150 actions per day for new accounts)
- **Start Small**: Begin with lower engagement numbers (5-10 per day) and gradually increase
- **Authenticity**: Ensure your comments sound natural and relevant to avoid being flagged as spam
- **Use a VPN**: Consider using a VPN that matches your account's usual location
- **Regular Monitoring**: Check the dashboard regularly to ensure the bot is functioning correctly

## Security Considerations

- Store your credentials securely and never share your `.env` files
- Regularly update your Instagram password
- Monitor your account for any unusual activity
- Consider using a dedicated Instagram account for testing before using your main account

## Troubleshooting

- **Instagram Login Issues**: If you encounter login problems, try logging in manually first or check if Instagram is requiring additional verification
- **API Rate Limits**: If you hit OpenAI rate limits, consider upgrading your API plan or adjusting the bot's scheduling
- **Database Connection**: Ensure MongoDB is running before starting the backend

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed for educational purposes and legitimate marketing automation. Users are responsible for ensuring they comply with Instagram's Terms of Service. Excessive automation may result in account limitations or bans.
