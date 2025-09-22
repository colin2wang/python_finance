import pandas as pd
from sklearn.linear_model import LinearRegression

from strategies.base_strategy import TradingStrategy


class LinearRegressionStrategy(TradingStrategy):
    """Machine Learning Strategy: Uses linear regression to predict price movements"""

    def generate_signals(self):
        """
        Generate trading signals using a linear regression model.
        
        The method creates lagged features from historical closing prices,
        trains a linear regression model to predict future price changes,
        and generates buy/sell signals based on the predictions.
        
        Returns:
            pd.Series: Trading signals (-1 for sell, 0 for hold, 1 for buy)
        """
        # Extract parameters
        window = self.params.get('window', 5)
        
        # Prepare feature data
        self.data['close_shifted'] = self.data['收盘'].shift(-1)  # Next day closing price
        self.data['price_change'] = self.data['close_shifted'] - self.data['收盘']  # Price change
        
        # Create features
        for i in range(1, window+1):
            self.data[f'lag_{i}'] = self.data['收盘'].shift(i)
        
        # Remove rows with NaN values
        self.data.dropna(inplace=True)
        
        # Prepare training data
        feature_cols = [f'lag_{i}' for i in range(1, window+1)]
        X = self.data[feature_cols]
        y = self.data['price_change']
        
        # Train the model
        model = LinearRegression()
        model.fit(X, y)
        
        # Make predictions
        predictions = model.predict(X)
        
        # Generate signals: buy when price is predicted to rise, sell when predicted to fall
        self.data['信号'] = 0
        self.data.loc[predictions > 0, '信号'] = 1   # Predicted rise, buy
        self.data.loc[predictions < 0, '信号'] = -1  # Predicted fall, sell
        
        # Keep only the last signal (as previous data was used for training)
        self.signals = self.data['信号']
        return self.signals