class TradeManager:
    def execute_trade(self, strategy, entry_price, exit_price, volume):
        """Executes a trade and returns trade details."""
        profit_loss = (exit_price - entry_price) * volume
        is_win = profit_loss > 0
        return {
            "entry_price": entry_price,
            "exit_price": exit_price,
            "volume": volume,
            "profit_loss": profit_loss,
            "is_win": is_win,
            "strategy": strategy
        }
