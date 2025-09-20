from strategies.base_strategy import TradingStrategy

class RSIStrategy(TradingStrategy):
    """RSI Strategy: Buy when oversold (<30), sell when overbought (>70)"""

    def generate_signals(self):
        """
        Generate trading signals based on RSI indicator.
        
        Buy signals are generated when the RSI crosses below the oversold level (default 30).
        Sell signals are generated when the RSI crosses above the overbought level (default 70).
        
        Returns:
            pd.Series: Trading signals (-1 for sell, 0 for hold, 1 for buy)
        """
        # Extract parameters
        period = self.params.get('period', 6)
        overbought = self.params.get('overbought_level', 70)
        oversold = self.params.get('oversold_level', 30)

        # Calculate RSI
        delta = self.data['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # Avoid division by zero
        rs = gain / loss.where(loss != 0, 1e-10)
        rsi = 100 - (100 / (1 + rs))

        self.data['RSI'] = rsi

        # Generate signals
        self.data['信号'] = 0
        # Buy when oversold
        self.data.loc[(self.data['RSI'] < oversold) & (self.data['RSI'].shift(1) >= oversold), '信号'] = 1
        # Sell when overbought
        self.data.loc[(self.data['RSI'] > overbought) & (self.data['RSI'].shift(1) <= overbought), '信号'] = -1

        self.signals = self.data['信号']
        return self.signals