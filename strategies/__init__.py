"""Strategies module for financial trading strategies."""
from strategies.base_strategy import TradingStrategy
from strategies.moving_average_strategy import MovingAverageStrategy
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy
from strategies.linear_regression_strategy import LinearRegressionStrategy
from strategies.polynomial_regression_strategy import PolynomialRegressionStrategy

__all__ = [
    'TradingStrategy',
    'MovingAverageStrategy',
    'RSIStrategy',
    'MACDStrategy',
    'LinearRegressionStrategy',
    'PolynomialRegressionStrategy'
]