import pandas as pd
from src.trades.strategy import MovingAverageCrossover

class Backtester:
    def __init__(self, metrics):
        """Initialize the Backtester with a MetricCalculator."""
        self.metrics = metrics

    def run(self):
        """Runs backtesting on historical data."""
        # Load the data
        data = pd.read_csv("data/historical_data/market_data.csv")
        
        # Apply the trading strategy
        strategy = MovingAverageCrossover()
        buy_signals, sell_signals = strategy.apply(data["price"])
        
        trades = []
        for i in range(len(data) - 1):  # Stop before the last index
            if buy_signals[i]:
                entry_price = data["price"][i]
                exit_price = data["price"][i + 1]  # Exit at the next price
                volume = 10
                profit_loss = (exit_price - entry_price) * volume  # Calculate profit/loss

                trade = {
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "volume": volume,
                    "profit_loss": profit_loss,
                    "strategy": "MovingAverageCrossover"
                }
                trades.append(trade)

        # Track metrics for the current day
        if trades:  # Only track metrics if trades exist
            self.metrics.track_daily_metrics(trades, day=i)

        return trades
