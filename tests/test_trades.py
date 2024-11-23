from src.trades.trade_manager import TradeManager

def test_execute_trade():
    trade_manager = TradeManager()
    trade = trade_manager.execute_trade("TestStrategy", 100, 110, 10)
    assert trade["profit_loss"] == 100
    assert trade["is_win"] is True
