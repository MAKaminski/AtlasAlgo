import matplotlib.pyplot as plt

class Visualizer:
    def plot_profit_loss(self, trades):
        """Plots profit/loss for each trade."""
        profits = [trade["profit_loss"] for trade in trades]
        plt.figure(figsize=(10, 6))
        plt.plot(profits, marker="o", linestyle="-")
        plt.title("Profit/Loss per Trade")
        plt.xlabel("Trade Index")
        plt.ylabel("Profit/Loss ($)")
        plt.grid()
        plt.show()

    def plot_portfolio_value(self, trades, initial_balance=500):
        """Plots cumulative portfolio value over time."""
        cumulative_value = initial_balance
        portfolio_values = [initial_balance]

        for trade in trades:
            cumulative_value += trade["profit_loss"]
            portfolio_values.append(cumulative_value)

        plt.figure(figsize=(10, 6))
        plt.plot(portfolio_values, marker="o", linestyle="-")
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Trade Index")
        plt.ylabel("Portfolio Value ($)")
        plt.grid()
        plt.show()

    def plot_trade_distribution(self, trades):
        """Plots the distribution of trade profits/losses."""
        profits = [trade["profit_loss"] for trade in trades]
        plt.figure(figsize=(10, 6))
        plt.hist(profits, bins=20, color="blue", alpha=0.7)
        plt.title("Trade Profit/Loss Distribution")
        plt.xlabel("Profit/Loss ($)")
        plt.ylabel("Frequency")
        plt.grid()
        plt.show()

    def plot_cumulative_returns(self, trades, initial_balance=500):
        """Plots cumulative returns as a percentage over time."""
        cumulative_value = initial_balance
        cumulative_returns = [0]  # Starts at 0% returns

        for trade in trades:
            cumulative_value += trade["profit_loss"]
            cumulative_returns.append((cumulative_value - initial_balance) / initial_balance * 100)

        plt.figure(figsize=(10, 6))
        plt.plot(cumulative_returns, marker="o", linestyle="-")
        plt.title("Cumulative Returns Over Time")
        plt.xlabel("Trade Index")
        plt.ylabel("Cumulative Returns (%)")
        plt.grid()
        plt.show()

    def plot_metrics_over_time(self, metrics, num_days):
            """Plot all metrics over a year with daily ticks."""
            plt.figure(figsize=(15, 10))
            
            # Plot each metric
            for metric, values in metrics.items():
                plt.plot(range(num_days), values, label=metric, linestyle="-", marker="o")

            # Configure plot
            plt.title("Performance Metrics Over Time")
            plt.xlabel("Day")
            plt.ylabel("Metric Value")
            plt.xticks(ticks=range(0, num_days, max(1, num_days // 10)), labels=[f"Day {i}" for i in range(0, num_days, max(1, num_days // 10))])
            plt.legend()
            plt.grid()
            plt.show()