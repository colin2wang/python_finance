import pandas as pd


class Backtester:
    """Class for backtesting trading strategies."""
    
    def __init__(self, data, strategy, initial_capital=100000):
        """
        Initialize the Backtester.
        
        Args:
            data (pd.DataFrame): Historical price data
            strategy (TradingStrategy): Trading strategy to backtest
            initial_capital (float): Initial capital for backtesting
        """
        self.data = data.copy()
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.positions = 0  # Current position (number of shares)
        self.cash = initial_capital  # Current cash
        self.results = None

    def run(self):
        """
        Execute backtesting.
        
        Returns:
            pd.DataFrame: Backtesting results with asset values over time
        """
        # Generate trading signals
        signals = self.strategy.generate_signals()
        self.data['信号'] = signals

        # Initialize asset value columns, explicitly specify data type as float
        self.data['资产价值'] = float(self.initial_capital)
        self.data['持仓数量'] = 0.0
        self.data['现金'] = float(self.initial_capital)

        # Ensure these columns have float data type
        self.data = self.data.astype({'资产价值': 'float64', '持仓数量': 'float64', '现金': 'float64'})

        # Ensure index is datetime type
        if not pd.api.types.is_datetime64_any_dtype(self.data.index):
            self.data.index = pd.to_datetime(self.data.index)

        # Iterate through each trading day to execute trades
        for i, (date, row) in enumerate(self.data.iterrows()):
            current_price = row['收盘']  # Execute trades at closing price
            signal = row['信号']

            # Buy signal: Buy with all cash (excluding transaction fees)
            if signal == 1 and self.cash > 0:
                # Calculate number of shares to buy (round down to avoid fractional shares)
                shares_to_buy = int(self.cash / current_price)
                if shares_to_buy > 0:
                    self.positions += shares_to_buy
                    self.cash -= shares_to_buy * current_price
                    print(
                        f"Buy: {date.date()}, Price: {current_price:.2f}, Shares: {shares_to_buy}, Cash left: {self.cash:.2f}")

            # Sell signal: Sell all positions
            elif signal == -1 and self.positions > 0:
                shares_to_sell = self.positions
                self.cash += shares_to_sell * current_price
                self.positions -= shares_to_sell
                print(f"Sell: {date.date()}, Price: {current_price:.2f}, Shares: {shares_to_sell}, Cash: {self.cash:.2f}")

            # Update daily asset value (cash + position value)
            self.data.at[date, '持仓数量'] = float(self.positions)
            self.data.at[date, '现金'] = float(self.cash)
            self.data.at[date, '资产价值'] = float(self.cash + (self.positions * current_price))

        self.results = self.data
        return self.results

    def get_metrics(self):
        """
        Calculate backtesting metrics.
        
        Returns:
            dict: Dictionary containing various backtesting metrics
        
        Raises:
            Exception: If backtesting has not been run yet
        """
        if self.results is None:
            raise Exception("Please run backtesting first (run method)")

        # Number of trades (buys + sells, each complete trade counts as 2 signals)
        total_signals = len(self.results[self.results['信号'] != 0])
        trade_count = total_signals  # Each buy/sell is counted as one trade

        # Win rate: profitable trades / total trades (requires paired buy-sell signals)
        profits = []
        buy_signals = self.results[self.results['信号'] == 1]
        sell_signals = self.results[self.results['信号'] == -1]

        # Pair buy and sell signals (take the smaller count)
        min_pairs = min(len(buy_signals), len(sell_signals))
        for i in range(min_pairs):
            buy_price = buy_signals.iloc[i]['收盘']
            sell_price = sell_signals.iloc[i]['收盘']
            profit = (sell_price - buy_price) / buy_price
            profits.append(profit)

        winning_trades = len([p for p in profits if p > 0])
        win_rate = (winning_trades / min_pairs) * 100 if min_pairs > 0 else 0

        # Total return
        final_value = self.results.iloc[-1]['资产价值']
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        # Maximum drawdown: maximum decline in asset value from peak to trough
        rolling_max = self.results['资产价值'].cummax()
        daily_drawdown = (self.results['资产价值'] - rolling_max) / rolling_max
        max_drawdown = (daily_drawdown.min() * 100) if len(daily_drawdown) > 0 else 0

        return {
            '初始资金': self.initial_capital,
            '最终资产': final_value,
            '总收益率(%)': round(total_return, 2),
            '交易次数': trade_count,
            '盈利交易次数': winning_trades,
            '总交易对': min_pairs,
            '胜率(%)': round(win_rate, 2),
            '最大回撤(%)': round(max_drawdown, 2)
        }