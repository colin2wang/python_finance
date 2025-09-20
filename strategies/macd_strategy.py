from strategies.base_strategy import TradingStrategy

class MACDStrategy(TradingStrategy):
    """MACD Strategy: Buy when MACD line crosses above signal line, sell when it crosses below"""

    def generate_signals(self):
        """
        Generate trading signals based on MACD indicator.
        
        Buy signals are generated when the MACD line crosses above the signal line.
        Sell signals are generated when the MACD line crosses below the signal line.
        
        Returns:
            pd.Series: Trading signals (-1 for sell, 0 for hold, 1 for buy)
        """
        # Extract parameters
        fast_period = self.params.get('fast_period', 4)
        slow_period = self.params.get('slow_period', 8)
        signal_period = self.params.get('signal_period', 2)

        # Calculate MACD
        ema_fast = self.data['收盘'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = self.data['收盘'].ewm(span=slow_period, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        self.data['MACD_line'] = macd_line
        self.data['signal_line'] = signal_line
        self.data['MACD_histogram'] = histogram

        # Generate signals
        self.data['信号'] = 0
        # MACD line crosses above signal line: buy
        self.data.loc[(macd_line > signal_line) & (macd_line.shift(1) <= signal_line), '信号'] = 1
        # MACD line crosses below signal line: sell
        self.data.loc[(macd_line < signal_line) & (macd_line.shift(1) >= signal_line), '信号'] = -1

        self.signals = self.data['信号']
        return self.signals