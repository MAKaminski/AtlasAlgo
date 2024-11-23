class MovingAverageCrossover:
    def apply(self, historical_data):
        """Applies the moving average crossover strategy."""
        short_ma = historical_data.rolling(window=5).mean()
        long_ma = historical_data.rolling(window=20).mean()

        buy_signals = short_ma > long_ma
        sell_signals = short_ma < long_ma
        return buy_signals, sell_signals
