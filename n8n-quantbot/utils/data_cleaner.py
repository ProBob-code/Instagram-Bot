# n8n-quantbot/utils/data_cleaner.py
import json
import sys
# import pandas as pd # Uncomment if you plan to use pandas
# import numpy as np  # Uncomment if you plan to use numpy

def clean_data(raw_data_json):
    """
    Cleans the raw stock price data.
    Input: JSON string of raw stock data (e.g., from Alpha Vantage or Yahoo Finance).
           Example: {"Meta Data": {...}, "Time Series (5min)": {"2023-10-27 15:55:00": {...}}}
    Output: JSON string of cleaned data.
            Example: {"processed_data": [{"timestamp": "2023-10-27 15:55:00", "open": "150.00", ...}]}
    """
    try:
        data = json.loads(raw_data_json)

        # --- Placeholder Cleaning Logic ---
        # This is highly dependent on the actual API response structure.
        # Example: If data is from Alpha Vantage Time Series
        # time_series_key = next(key for key in data if "Time Series" in key)
        # time_series = data[time_series_key]

        # cleaned_entries = []
        # for timestamp, values in time_series.items():
        #     cleaned_entries.append({
        #         "timestamp": timestamp,
        #         "open": values.get("1. open"),
        #         "high": values.get("2. high"),
        #         "low": values.get("3. low"),
        #         "close": values.get("4. close"),
        #         "volume": values.get("5. volume")
        #     })
        # output = {"processed_data": cleaned_entries}
        # --- End Placeholder ---

        # For now, just pass it through or add a simple transformation
        output = {"message": "Data cleaning placeholder", "original_data": data}
        return json.dumps(output)

    except Exception as e:
        error_output = {"error": str(e), "step": "data_cleaning"}
        print(json.dumps(error_output), file=sys.stderr) # Send error to stderr for n8n
        sys.exit(1)

if __name__ == "__main__":
    # n8n Execute Command typically sends input as a single JSON string via stdin
    # or provides data through environment variables / files.
    # This example assumes input comes from stdin.
    if not sys.stdin.isatty():
        input_json = sys.stdin.read()
        cleaned_json_output = clean_data(input_json)
        print(cleaned_json_output) # Output to stdout for n8n
    else:
        # Example usage for local testing:
        # echo '{"Time Series (5min)": {"2023-10-27 15:55:00": {"1. open": "150.00"}}}' | python utils/data_cleaner.py
        sample_input = '{"sample_key": "sample_value"}'
        print(f"Running with sample data: {sample_input}")
        print(clean_data(sample_input))
