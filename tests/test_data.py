import pandas as pd
import numpy as np

# Generate synthetic market data
def generate_market_data(filename="data/historical_data/market_data.csv"):
    np.random.seed(42)  # For reproducibility
    num_days = 500
    dates = pd.date_range(start="2023-01-01", periods=num_days, freq="D")
    prices = 100 + np.cumsum(np.random.randn(num_days))  # Simulate random walk for prices

    # Create a DataFrame
    df = pd.DataFrame({
        "date": dates,
        "price": prices
    })

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Sample market data saved to {filename}")

# Generate the file
generate_market_data()
