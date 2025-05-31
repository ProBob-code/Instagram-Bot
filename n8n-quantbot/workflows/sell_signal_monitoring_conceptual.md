# Sell Signal Monitoring Agent - Conceptual Workflow

This document outlines the conceptual structure for a separate n8n workflow dedicated to monitoring stock prices and triggering sell decisions.

## Objective
Periodically check the current price of owned stocks, apply a model or logic to decide if a sell is warranted, and notify the user or execute a sell order.

## Trigger
*   **Node Type**: `n8n-nodes-base.cron`
*   **Purpose**: Schedule the monitoring check (e.g., every 5 minutes, every hour during trading hours).

## Steps

1.  **Fetch Owned Stocks List (Source: TBD)**
    *   **Node Type**: `n8n-nodes-base.httpRequest` or `n8n-nodes-base.readDatabase` (depending on where this list is stored)
    *   **Purpose**: Get the list of stocks currently held that need monitoring. This might come from a database, a Google Sheet, or even a static list within n8n if the portfolio is fixed.
    *   **Output**: JSON list of owned stock tickers and potentially purchase price/quantity.

2.  **Loop Through Owned Stocks**
    *   **Node Type**: `n8n-nodes-base.splitInBatches` (if processing multiple stocks) or a loop within a Code node if more complex iteration logic is needed.
    *   **Purpose**: Process each owned stock individually for price checking and decision making.

3.  **Fetch Current Price Data (per stock)**
    *   **Node Type**: `n8n-nodes-base.httpRequest`
    *   **Parameters**:
        *   URL: Pointing to your chosen stock API (e.g., Alpha Vantage, Yahoo Finance).
        *   Query Parameters: Stock ticker from the current loop iteration.
        *   API Key: `{{$env.STOCK_API_KEY}}` (example).
    *   **Output**: JSON data with current price for the stock.

4.  **Apply Sell Logic/Model (per stock)**
    *   **Node Type**: `n8n-nodes-base.executeCommand` or `n8n-nodes-base.code`
    *   **Purpose**:
        *   If using a Python script: `python models/sell_decision_model.py` (this script would need to be created). The script would take current price, potentially historical data, and purchase price as input.
        *   If using a Code node: Implement JavaScript logic directly (e.g., check against stop-loss percentage, take-profit target, or a technical indicator).
    *   **Input**: Current price data, potentially purchase price/details.
    *   **Output**: Decision: "SELL", "HOLD".

5.  **IF "SELL" Decision**
    *   **Node Type**: `n8n-nodes-base.if`
    *   **Condition**: Based on the output of the Sell Logic/Model step.

6.  **Notification Agent (if SELL)**
    *   **Node Type**: `n8n-nodes-base.slack` or `n8n-nodes-base.httpRequest` (for other services like WhatsApp via Twilio)
    *   **Parameters**:
        *   Message: "SELL Signal for [Stock Ticker]: Current Price [Price]. Reason: [Reason from model/logic]."
        *   Slack Webhook URL: `{{$env.SLACK_WEBHOOK_URL}}`
    *   **Purpose**: Notify the user about the sell signal.

7.  **(Optional) Trade Execution Agent (if SELL and auto-trade enabled)**
    *   **Node Type**: `n8n-nodes-base.httpRequest`
    *   **Parameters**:
        *   URL: Broker API endpoint for placing a sell order.
        *   Body/Query Parameters: Stock symbol, quantity, order type (market/limit).
        *   Authentication: Broker API Key/Secret from environment variables `{{$env.BROKER_API_KEY}}`, `{{$env.BROKER_API_SECRET}}`.
    *   **Purpose**: Automatically execute the sell trade. *Caution: Implement with thorough testing.*

## Considerations
*   **State Management**: How are owned stocks tracked? This workflow needs a reliable source.
*   **Error Handling**: Implement robust error handling for API calls and script executions.
*   **Throttling/Rate Limits**: Be mindful of API rate limits for both stock data and broker APIs.
*   **Backtesting**: This workflow should ideally be based on a strategy that has been backtested.
