import os

class ReportGenerator:
    def generate(self, trades, metrics):
        """Generates CSV and charts for analysis."""
        # Ensure the directory exists
        os.makedirs("data/reports", exist_ok=True)

        # Write trades to a CSV file
        with open("data/reports/trades.csv", "w") as file:
            file.write("Entry Price,Exit Price,Volume,Profit/Loss,Is Win,Strategy\n")
            for trade in trades:
                file.write(
                    f"{trade['entry_price']},{trade['exit_price']},{trade['volume']},"
                    f"{trade['profit_loss']},{trade['profit_loss'] > 0},{trade['strategy']}\n"
                )
        print("Report generated: data/reports/trades.csv")
