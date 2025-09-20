from strategies.base_strategy import TradingStrategy

class MovingAverageStrategy(TradingStrategy):
    """Moving Average Strategy: Buy when short-term MA crosses above long-term MA, sell when it crosses below"""

    def generate_signals(self):
        """
        Generate trading signals based on moving average crossovers.
        
        Buy signals are generated when the short-term moving average crosses above
        the long-term moving average (golden cross). Sell signals are generated
        when the short-term moving average crosses below the long-term moving average
        (death cross).
        
        Returns:
            pd.Series: Trading signals (-1 for sell, 0 for hold, 1 for buy)
        """
        # Extract parameters
        short_window = self.params.get('short_window', 3)
        long_window = self.params.get('long_window', 5)

        # Calculate moving averages (using closing prices)
        self.data['short_ma'] = self.data['收盘'].rolling(window=short_window).mean()
        self.data['long_ma'] = self.data['收盘'].rolling(window=long_window).mean()

        # Generate signals: 1=buy, -1=sell, 0=hold
        self.data['信号'] = 0
        # Short MA crosses above long MA (golden cross): buy signal
        self.data.loc[self.data['short_ma'] > self.data['long_ma'], '信号'] = 1
        # Short MA crosses below long MA (death cross): sell signal
        self.data.loc[self.data['short_ma'] < self.data['long_ma'], '信号'] = -1

        # Remove duplicate signals (avoid consecutive signals)
        self.data['信号'] = self.data['信号'].diff().fillna(0)
        # Keep only 1 (buy) and -1 (sell), remove 0 (no change)
        self.data.loc[self.data['信号'] == 2, '信号'] = 1  # 0→1 transition
        self.data.loc[self.data['信号'] == -2, '信号'] = -1  # 0→-1 transition
        self.data.loc[~self.data['信号'].isin([1, -1]), '信号'] = 0

        self.signals = self.data['信号']
        return self.signals