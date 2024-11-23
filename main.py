from src.trades.trade_manager import TradeManager
from src.metrics.metric_calculator import MetricCalculator
from src.backtesting.backtester import Backtester
from src.reporting.report_generator import ReportGenerator
from src.reporting.visualizer import Visualizer
from src.database.db_manager import DBManager

def main():
    # Initialize components
    metrics = MetricCalculator()  # Track metrics
    backtester = Backtester(metrics)  # Pass metrics to Backtester
    report_gen = ReportGenerator()
    visualizer = Visualizer()
    db_manager = DBManager()

    # Create database tables
    db_manager.create_tables()

    # Set the initial balance
    initial_balance = 500

    # Run backtest
    print("Running backtest...")
    trades = backtester.run()

    # Store trades in the database
    for trade in trades:
        db_manager.insert_trade(trade)

    # Fetch trades from the database
    stored_trades = db_manager.fetch_all_trades()
    # print("Stored Trades:", stored_trades)

    # Calculate metrics
    print("Calculating metrics...")
    metrics.calculate(trades, initial_balance)

    # Generate reports
    print("Generating reports...")
    report_gen.generate(trades, metrics)

    # Visualize results
    print("Visualizing results...")
    visualizer.plot_profit_loss(trades)
    visualizer.plot_portfolio_value(trades, initial_balance)

    # Visualize tracked metrics over time
    print("Visualizing metrics over time...")
    visualizer.plot_metrics_over_time(metrics.daily_metrics, len(trades))

if __name__ == "__main__":
    # Clear Terminal
    print(chr(27) + "[2J")
    main()
