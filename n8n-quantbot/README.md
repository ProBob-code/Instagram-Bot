# n8n-QuantBot

🧠 **Project Name**: n8n-QuantBot
🎯 **Objective**: To build a modular, fully automated algorithmic trading bot using n8n that fetches stock data and news, prepares & analyzes the data, predicts future stock prices, assesses news sentiment, combines insights for a trading decision, sends a summary to the user, executes trades via broker API (conceptual), and monitors stock prices for sell decisions.

## Architecture Overview

The bot is designed as a series of interconnected agents (n8n nodes) that form a trading pipeline:

1.  **Cron Trigger / Webhook (Start)**: Initiates the workflow.
2.  **Data Fetch Agent**: Fetches stock price data.
3.  **Data Clean Agent**: Preprocesses raw data using a Python script.
4.  **Forecasting Agent**: Predicts price movement using a Python ML model.
5.  **News Fetch Agent**: Fetches relevant company news.
6.  **Sentiment Analysis Agent**: Performs NLP on news using a Python script.
7.  **Strategy Combiner Agent**: Merges forecast and sentiment for a decision.
8.  **Notification Agent**: Sends a summary to Slack/WhatsApp.
9.  **Manual Approval Agent (Optional)**: Waits for user confirmation before trading.
10. **Trade Execution Agent**: Places orders via broker API (conceptual).
11. **Sell Signal Monitoring Agent (Separate Workflow)**: Monitors for sell conditions.

## 📁 Directory Structure

```
n8n-quantbot/
├── docker-compose.yml        # Docker configuration for n8n
├── models/                   # Python ML/NLP models
│   ├── price_forecast.py     # Placeholder for price forecasting model
│   └── sentiment_model.py    # Placeholder for sentiment analysis model
├── utils/                    # Utility scripts
│   ├── data_cleaner.py       # Placeholder for data cleaning script
│   └── broker_api_conceptual.md # Conceptual design for broker API interaction
├── workflows/                # n8n workflow JSON and conceptual designs
│   ├── trading_pipeline.json # Main n8n trading workflow
│   ├── sell_signal_monitoring_conceptual.md # Conceptual design for sell signal workflow
│   └── notification_flow_conceptual.md    # Conceptual design for notification flows
├── .env                      # Environment variables (API keys, secrets - create from .env.example if provided)
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites
*   Docker and Docker Compose
*   n8n instance (can be run via the provided `docker-compose.yml`)
*   API Keys for:
    *   Stock data provider (e.g., Alpha Vantage, Yahoo Finance)
    *   News API provider (e.g., NewsAPI)
    *   Broker API (e.g., Zerodha, Upstox) - for actual trading
    *   Slack Webhook URL (for Slack notifications)
    *   Twilio or similar for WhatsApp (Account SID, Auth Token, From Number)
*   Python environment with necessary libraries (`pandas`, `numpy`, `requests`, ML/NLP libraries like `statsmodels`, `pmdarima`, `prophet`, `vaderSentiment`, `textblob`) if you intend to run and develop the Python scripts locally or build custom Docker images for n8n's Execute Command node.

### Setup
1.  **Clone the Repository (or create files locally based on this structure)**:
    ```bash
    # If this were a git repo:
    # git clone <repository_url>
    # cd n8n-quantbot
    ```
    For now, ensure you have the directory structure and files as listed above.

2.  **Configure Environment Variables**:
    *   Create a `.env` file in the `n8n-quantbot/` root directory.
    *   Add your API keys and other configurations. Example:
        ```env
        # n8n Environment
        GENERIC_TIMEZONE=America/New_York
        TZ=America/New_York

        # API Keys
        STOCK_API_KEY=your_stock_api_key
        NEWS_API_KEY=your_news_api_key
        ZERODHA_API_KEY=your_zerodha_api_key # Conceptual
        ZERODHA_SECRET=your_zerodha_secret   # Conceptual

        # Notification Services
        SLACK_WEBHOOK_URL=your_slack_webhook_url
        TWILIO_ACCOUNT_SID=your_twilio_account_sid
        TWILIO_AUTH_TOKEN=your_twilio_auth_token
        TWILIO_WHATSAPP_FROM_NUMBER=whatsapp:+14155238886 # Example Twilio sandbox number
        USER_PHONE_NUMBER=+12345678900 # Your WhatsApp number for receiving messages

        # Add any other necessary environment variables for your Python scripts or n8n nodes
        ```

3.  **Run n8n via Docker Compose**:
    ```bash
    cd n8n-quantbot
    docker-compose up -d
    ```
    This will start an n8n instance accessible at `http://localhost:5678`.

4.  **Import the Workflow**:
    *   Open your n8n instance in a web browser.
    *   Go to "Workflows" and click "Import from File".
    *   Upload the `n8n-quantbot/workflows/trading_pipeline.json` file.

5.  **Configure n8n Nodes**:
    *   Open the imported "n8n-QuantBot Trading Pipeline" workflow.
    *   **API Keys & URLs**: Many nodes (HTTP Request, Slack, etc.) are configured to use environment variables (e.g., `{{$env.STOCK_API_KEY}}`). Ensure these are correctly set in your `.env` file and picked up by Docker Compose.
    *   **Execute Command Nodes**:
        *   These nodes are placeholders to run the Python scripts (`data_cleaner.py`, `price_forecast.py`, `sentiment_model.py`).
        *   **Important**: For the `Execute Command` nodes to run Python scripts, n8n needs access to a Python environment with the necessary libraries.
            *   You can achieve this by building a custom Docker image for n8n that includes Python and your libraries, then referencing that image in `docker-compose.yml`.
            *   Alternatively, for simpler cases, if the n8n base image has Python, you might be able to install libraries into the running container's `~/.n8n/custom` directory or mount a volume with a pre-prepared virtual environment. The provided `docker-compose.yml` includes commented-out volume mounts for `models` and `utils` which could be a starting point if your n8n image can execute Python scripts directly from mounted paths.
        *   Update the commands in these nodes if your script paths or execution methods differ.

## Component Details

### 1. Workflows
*   **`workflows/trading_pipeline.json`**: The main n8n workflow.
    *   See the JSON file for node details and connections.
    *   This workflow orchestrates the entire process from data fetching to (conceptual) trade execution.
*   **`workflows/sell_signal_monitoring_conceptual.md`**:
    *   A conceptual outline for a separate workflow to monitor owned stocks and generate sell signals. This is not an executable workflow but a design document.
*   **`workflows/notification_flow_conceptual.md`**:
    *   Details on setting up Slack and WhatsApp notifications within n8n.

### 2. Python Scripts
*   **`utils/data_cleaner.py`**:
    *   Placeholder script to clean raw stock data.
    *   Input: Raw JSON data from stock API.
    *   Output: Cleaned JSON data.
    *   *Needs customization based on your chosen stock API's data format.*
*   **`models/price_forecast.py`**:
    *   Placeholder script for price forecasting.
    *   Input: Cleaned JSON data.
    *   Output: Forecasted prices.
    *   *Requires a trained ML model (e.g., ARIMA, Prophet, LSTM) and logic to load/run it.*
*   **`models/sentiment_model.py`**:
    *   Placeholder script for news sentiment analysis.
    *   Input: JSON data containing news articles.
    *   Output: Sentiment score(s).
    *   *Requires an NLP model/library (e.g., VADER, TextBlob, HuggingFace Transformers).*
*   **`utils/broker_api_conceptual.md`**:
    *   A design document for interacting with broker APIs. This is not runnable code but provides a structural guideline for building out trade execution capabilities.

### 3. Configuration
*   **`docker-compose.yml`**: Defines the n8n service, port mappings, and environment variable passthrough.
*   **`.env`**: Stores all your sensitive API keys and configurations. **Do not commit this file if it contains real secrets.** Use `.env.example` as a template if sharing the project.

## Next Steps & Customization
1.  **Flesh out Python Scripts**:
    *   Implement actual data cleaning logic in `data_cleaner.py` specific to your data source.
    *   Develop/integrate your price forecasting model in `price_forecast.py`.
    *   Develop/integrate your sentiment analysis model in `sentiment_model.py`.
2.  **Broker API Integration**:
    *   Based on `broker_api_conceptual.md`, develop Python scripts to interact with your chosen broker's API.
    *   Securely manage authentication (this is often the most complex part).
3.  **Refine n8n Workflow**:
    *   Update HTTP Request nodes with actual API endpoints.
    *   Adjust parameters and logic in all nodes to fit your strategy.
    *   Implement robust error handling within the workflow.
4.  **Build Custom Docker Image for n8n (Recommended for Python)**:
    *   Create a `Dockerfile` that starts from an n8n base image and installs Python, your required libraries (from a `requirements.txt`), and copies your scripts into the image.
    *   Update `docker-compose.yml` to build and use this custom image.
5.  **Implement the Sell Signal Monitoring Workflow**:
    *   Translate `sell_signal_monitoring_conceptual.md` into an actual n8n workflow.
6.  **Backtesting**: Thoroughly backtest your trading strategy before deploying with real money.

## Disclaimer
This project is for educational and illustrative purposes. Algorithmic trading involves significant risk, including the potential loss of capital. Any actions taken based on this project are at your own risk. Ensure you understand the risks involved and comply with all applicable financial regulations.
