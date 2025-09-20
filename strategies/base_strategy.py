class TradingStrategy:
    """Base class for trading strategies"""

    def __init__(self, data, params=None):
        """
        Initialize the trading strategy.
        
        Args:
            data (pd.DataFrame): Historical price data
            params (dict, optional): Strategy parameters
        """
        self.data = data.copy()
        self.params = params or {}
        self.signals = None

    def generate_signals(self):
        """
        Generate trading signals. Must be implemented by subclasses.
        
        Returns:
            pd.Series: Trading signals
        """
        raise NotImplementedError("Subclasses must implement the generate_signals method")