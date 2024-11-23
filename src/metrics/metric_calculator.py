import numpy as np
from colorama import Fore, Style

class MetricCalculator:
    def __init__(self):
        self.daily_metrics = {
            "Sharpe Ratio": [],
            "Max Drawdown": [],
            "Win/Loss Ratio": [],
            "Profit Factor": [],
            "Volatility": [],
            "Portfolio Returns (%)": [],
            "Hit Rate": [],
            "Risk-Reward Ratio": [],
            "Alpha": [],
            "Beta": [],
            "Exposure": [],
            "Slippage": [],
            "Transaction Costs": [],
            "Liquidity Impact": []
        }

    def track_daily_metrics(self, trades, day):
        """Track metrics for a specific day."""
        if not trades:  # No trades executed yet
            self._append_empty_metrics()
            return

        profits = np.array([trade["profit_loss"] for trade in trades])

        if profits.size == 0:  # No profit/loss data
            self._append_empty_metrics()
            return

        sharpe_ratio = (profits.mean() - 0.02) / profits.std() if profits.std() != 0 else np.nan
        max_drawdown = self.calculate_max_drawdown(profits, initial_balance=500) if profits.size > 0 else np.nan
        win_loss_ratio = (
            len([p for p in profits if p > 0]) / len([p for p in profits if p <= 0])
            if len([p for p in profits if p <= 0]) > 0 else np.nan
        )
        profit_factor = (
            profits[profits > 0].sum() / abs(profits[profits <= 0].sum())
            if profits[profits <= 0].sum() != 0 else np.nan
        )
        volatility = profits.std() / 500  # Assuming initial balance of $500
        portfolio_returns = profits.sum() / 500 * 100
        hit_rate = len([p for p in profits if p > 0]) / len(profits) if len(profits) > 0 else np.nan
        avg_profit = profits[profits > 0].mean() if len(profits[profits > 0]) > 0 else 0
        avg_loss = abs(profits[profits <= 0].mean()) if len(profits[profits <= 0]) > 0 else 0
        risk_reward_ratio = avg_profit / avg_loss if avg_loss > 0 else np.nan

        # Append metrics for the current day
        self.daily_metrics["Sharpe Ratio"].append(sharpe_ratio)
        self.daily_metrics["Max Drawdown"].append(max_drawdown)
        self.daily_metrics["Win/Loss Ratio"].append(win_loss_ratio)
        self.daily_metrics["Profit Factor"].append(profit_factor)
        self.daily_metrics["Volatility"].append(volatility)
        self.daily_metrics["Portfolio Returns (%)"].append(portfolio_returns)
        self.daily_metrics["Hit Rate"].append(hit_rate)
        self.daily_metrics["Risk-Reward Ratio"].append(risk_reward_ratio)
        self.daily_metrics["Alpha"].append(np.nan)  # Placeholder
        self.daily_metrics["Beta"].append(np.nan)  # Placeholder
        self.daily_metrics["Exposure"].append(1.0)  # Placeholder
        self.daily_metrics["Slippage"].append(0.0)  # Placeholder
        self.daily_metrics["Transaction Costs"].append(0.0)  # Placeholder
        self.daily_metrics["Liquidity Impact"].append(0.0)  # Placeholder

    def _append_empty_metrics(self):
        """Append NaN or defaults for empty metrics."""
        for key in self.daily_metrics:
            self.daily_metrics[key].append(np.nan)
    
    def calculate(self, trades, initial_balance=500, benchmark_returns=None, trade_fees=0):
        """Calculates and prints all trading metrics with benchmarks."""
        
        # Define benchmarks for comparison
        benchmarks = {
            "Sharpe Ratio": 2.0,
            "Max Drawdown": -0.1,
            "Win/Loss Ratio": 0.7,
            "Profit Factor": 1.5,
            "Volatility": 0.1,
            "Portfolio Returns (%)": 15,
            "Hit Rate": 0.5,
            "Risk-Reward Ratio": 2.0,
            "Alpha": 0.0,
            "Beta": 1.0,
            "Exposure": "Optimize",
            "Slippage": "Minimize",
            "Transaction Costs": "Minimize",
            "Liquidity Impact": "Minimize",
        }

        # Extract profits and categorize trades
        profits = np.array([trade["profit_loss"] for trade in trades])
        winning_trades = profits[profits > 0]
        losing_trades = profits[profits <= 0]
        num_trades = len(trades)

        # Calculate primary metrics
        sharpe_ratio = (profits.mean() - 0.02) / profits.std() if profits.std() != 0 else np.nan
        max_drawdown = self.calculate_max_drawdown(profits, initial_balance)
        win_loss_ratio = len(winning_trades) / len(losing_trades) if len(losing_trades) > 0 else np.nan
        profit_factor = winning_trades.sum() / abs(losing_trades.sum()) if losing_trades.sum() != 0 else np.nan
        volatility = profits.std() / initial_balance
        portfolio_returns = profits.sum() / initial_balance * 100
        hit_rate = len(winning_trades) / num_trades if num_trades > 0 else 0

        # Calculate secondary metrics
        avg_profit = winning_trades.mean() if len(winning_trades) > 0 else 0
        avg_loss = abs(losing_trades.mean()) if len(losing_trades) > 0 else 0
        risk_reward_ratio = avg_profit / avg_loss if avg_loss != 0 else np.nan

        # Alpha and Beta calculations (requires benchmark returns)
        alpha, beta = self.calculate_alpha_beta(profits, benchmark_returns)

        # Operational metrics
        slippage = (np.array([trade.get("entry_price", 0) for trade in trades]) - 
                    np.array([trade.get("exit_price", 0) for trade in trades])).mean()
        transaction_costs = trade_fees / initial_balance * 100 if initial_balance > 0 else 0
        liquidity_impact = (np.array([trade.get("size", 1) for trade in trades]) / 
                            np.array([trade.get("exit_price", 1) for trade in trades])).mean()
        exposure = 1.0  # Placeholder for actual exposure metric (if implemented)

        # Prepare results
        results = {
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Win/Loss Ratio": win_loss_ratio,
            "Profit Factor": profit_factor,
            "Volatility": volatility,
            "Portfolio Returns (%)": portfolio_returns,
            "Hit Rate": hit_rate,
            "Risk-Reward Ratio": risk_reward_ratio,
            "Alpha": alpha,
            "Beta": beta,
            "Exposure": exposure,
            "Slippage": slippage,
            "Transaction Costs": transaction_costs,
            "Liquidity Impact": liquidity_impact,
        }

        # Print metrics with benchmarks
        print("\nPerformance Metrics (vs. Benchmarks):\n")
        print(f"{'Metric':<25}{'Our Value':<15}{'Benchmark':<15}{'Variance':<15}")
        print("-" * 75)

        for metric, value in results.items():
            benchmark = benchmarks.get(metric, "N/A")
            variance = value - benchmark if isinstance(benchmark, (int, float)) else "N/A"
            # Handle formatting for floats with 4 decimals or other types
            value_str = f"{value:.4f}" if isinstance(value, float) else str(value)
            benchmark_str = f"{benchmark:.4f}" if isinstance(benchmark, float) else str(benchmark)
            variance_str = f"{variance:.4f}" if isinstance(variance, float) else str(variance)

            # Add color to variance
            variance_color = Fore.GREEN if isinstance(variance, float) and variance > 0 else Fore.RED
            print(f"{metric:<25}{value_str:<15}{benchmark_str:<15}{variance_color}{variance_str}{Style.RESET_ALL}")

        print("\n")

    @staticmethod
    def calculate_max_drawdown(profits, initial_balance):
        """Calculate max drawdown based on profits."""
        if profits.size == 0:
            return np.nan

        cumulative_returns = np.cumsum(profits) + initial_balance
        peak = np.maximum.accumulate(cumulative_returns)
        drawdowns = (cumulative_returns - peak) / peak
        return drawdowns.min()

    @staticmethod
    def calculate_alpha_beta(portfolio_returns, benchmark_returns):
        """Calculates alpha and beta based on benchmark returns."""
        if benchmark_returns is None or len(portfolio_returns) != len(benchmark_returns):
            return np.nan, np.nan
        covariance = np.cov(portfolio_returns, benchmark_returns)
        beta = covariance[0, 1] / np.var(benchmark_returns) if np.var(benchmark_returns) != 0 else np.nan
        alpha = portfolio_returns.mean() - beta * benchmark_returns.mean()
        return alpha, beta
