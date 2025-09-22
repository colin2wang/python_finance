# Python Finance Project

This is a project for financial data analysis and trading strategy backtesting using Python. It provides a comprehensive framework for quantitative trading research, allowing users to implement, test, and visualize trading strategies using historical market data.

See Chinese Version (中文版) [README_CN.md](README_CN.md)

## Core Concepts

The project is built around several key components that work together to facilitate quantitative trading research:

- **Data Management**: Efficient loading and preprocessing of financial data from various sources
- **Strategy Development**: Framework for implementing custom trading strategies
- **Backtesting Engine**: Robust system for testing strategies against historical data
- **Risk Management**: Tools for evaluating strategy performance and risk metrics
- **Visualization**: Comprehensive charting capabilities for analyzing results

### Backtesting Engine

The backtesting engine is responsible for simulating trades based on strategy signals and calculating performance metrics. It works by:

1. Generating trading signals from the strategy
2. Executing trades at closing prices (to prevent lookahead bias)
3. Tracking position changes and cash flows
4. Calculating performance metrics

**Trade Execution:**
- Buy signals: Use all available cash to buy shares (rounded down to whole shares)
- Sell signals: Sell all held positions
- Trades are executed at the closing price of the signal day

**Performance Metrics:**
- Total Return: $Total\ Return(\%) = \frac{Final\ Value - Initial\ Capital}{Initial\ Capital} \times 100\%$
- Win Rate: $Win\ Rate(\%) = \frac{Winning\ Trades}{Total\ Trades} \times 100\%$
- Maximum Drawdown: $Max\ Drawdown(\%) = \max(\frac{Peak\ Value - Trough\ Value}{Peak\ Value}) \times 100\%$

This approach provides a realistic simulation of how strategies would perform in live trading, while accounting for factors like transaction costs (through whole share rounding) and market impact (by using closing prices).

## Project Structure

- `data_loader.py`: Data loading module responsible for importing and preprocessing financial data from various sources
- `strategies/`: Trading strategy implementation directory containing modular strategy classes
- `backtester.py`: Backtesting engine that executes strategies against historical data and calculates performance metrics
- `visualizer.py`: Visualization tools for plotting price charts, strategy signals, and performance metrics
- `main.py`: Main program entry point for configuring and running the analysis pipeline
- `sample_test_01.ipynb`: Sample Jupyter Notebook demonstrating project usage and capabilities
- `config.yaml`: Configuration file for setting data sources, strategy parameters, and execution options

## Requirements

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver
- Related dependencies (see `pyproject.toml`)

## Installation

1. Clone the repository locally:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd python_finance
   ```

3. Install dependencies using uv:
   ```
   uv sync
   ```
   This will automatically create and manage a virtual environment, and install all dependencies from `pyproject.toml`.

## Usage

Before running any commands, activate the virtual environment created by uv:

```
uv run
```

### Running the main program

```
uv run python main.py
```

### Running Jupyter Notebook

```
uv run jupyter notebook sample_test_01.ipynb
```

### Running Backtesting

After configuring parameters in `main.py`, run:

```
uv run python main.py --mode=backtest
```

## Configuration

Project configuration is in the `config.yaml` file, where you can configure data sources, trading strategy parameters, etc.

Data loading configuration is in the `data_loader.yml` file, where you can configure CSV file paths and column names. This makes it easier to adapt the project to different data sources without modifying the code.

## Strategy Development

The project provides a flexible framework for developing custom trading strategies. Each strategy is implemented as a separate class in the `strategies/` directory, following a consistent interface that allows seamless integration with the backtesting engine.

To create a new strategy:
1. Create a new Python file in the `strategies/` directory
2. Implement a class that inherits from the base strategy interface
3. Define your trading logic in the required methods
4. Register the strategy in `main.py` to make it available for backtesting

Strategies can incorporate various technical indicators, risk management rules, and position sizing algorithms to suit different trading approaches.

### Implemented Strategies

The project includes several pre-implemented trading strategies, each based on different technical analysis principles:

#### 1. Moving Average Strategy

The Moving Average Strategy generates trading signals based on moving average crossovers. It uses two moving averages with different periods:
- Short-term Moving Average (MA_short)
- Long-term Moving Average (MA_long)

**Principle:**
- Buy signal: When MA_short crosses above MA_long (golden cross)
- Sell signal: When MA_short crosses below MA_long (death cross)

**Calculation Formula:**
- $MA_t(n) = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}$

Where:
- $MA_t(n)$ is the moving average of period n at time t
- $P_{t-i}$ is the closing price at time t-i

**Advantages:**
- Simple and intuitive
- Works well in trending markets
- Less sensitive to short-term price fluctuations

**Disadvantages:**
- Lagging indicator
- May generate false signals in sideways markets
- Requires parameter tuning

#### 2. RSI Strategy

The RSI (Relative Strength Index) Strategy generates signals based on overbought and oversold conditions:

**Principle:**
- Buy signal: When RSI crosses above the oversold level (typically 30)
- Sell signal: When RSI crosses below the overbought level (typically 70)

**Calculation Formula:**
- $RSI = 100 - \frac{100}{1 + RS}$
- $RS = \frac{	ext{Average of n-period gains}}{	ext{Average of n-period losses}}$

Where:
- RS is the relative strength
- Gain is the positive price change
- Loss is the absolute value of negative price change

**Advantages:**
- Good for identifying overbought/oversold conditions
- Works well in mean-reverting markets
- Can identify potential reversal points

**Disadvantages:**
- May remain in overbought/oversold territory during strong trends
- Can generate false signals
- Requires careful parameter tuning

#### 3. MACD Strategy

The MACD (Moving Average Convergence Divergence) Strategy generates signals based on the relationship between MACD line and signal line:

**Principle:**
- Buy signal: When MACD line crosses above the signal line
- Sell signal: When MACD line crosses below the signal line

**Calculation Formula:**
- $EMA_{fast} = EMA(	ext{Close}, n_{fast})$
- $EMA_{slow} = EMA(	ext{Close}, n_{slow})$
- $MACD_{line} = EMA_{fast} - EMA_{slow}$
- $Signal_{line} = EMA(MACD_{line}, n_{signal})$
- $Histogram = MACD_{line} - Signal_{line}$

Where:
- $EMA$ is the Exponential Moving Average
- $n_{fast}$, $n_{slow}$, $n_{signal}$ are the periods for fast EMA, slow EMA, and signal line respectively

**Advantages:**
- Combines trend-following and momentum indicators
- Can identify changes in market momentum
- Works well in trending markets

**Disadvantages:**
- Can generate false signals in sideways markets
- Lagging indicator due to moving averages
- Requires parameter tuning

#### 4. Linear Regression Strategy

The Linear Regression Strategy uses linear regression to predict future price movements based on historical data:

**Principle:**
- Uses historical closing prices as features
- Trains a linear regression model to predict future price changes
- Generates buy signal when predicted change is positive
- Generates sell signal when predicted change is negative

**Calculation Formula:**
- $y = eta_0 + eta_1 x_1 + eta_2 x_2 + ... + eta_n x_n + \epsilon$

Where:
- $y$ is the predicted price change
- $x_i$ are the lagged closing prices (features)
- $eta_i$ are the regression coefficients
- $\epsilon$ is the error term

**Advantages:**
- Can capture complex patterns in data
- Adaptable to changing market conditions
- Objective decision-making based on data

**Disadvantages:**
- Requires sufficient historical data for training
- May overfit to historical data
- Black box nature makes it difficult to interpret
- Requires expertise in machine learning

This strategy demonstrates how machine learning techniques can be applied to financial markets for predictive modeling.

#### 5. Polynomial Regression Strategy

The Polynomial Regression Strategy extends the linear regression approach by using polynomial features to capture non-linear relationships in the data:

**Principle:**
- Uses historical closing prices as base features
- Transforms features into polynomial terms to model non-linear patterns
- Trains a polynomial regression model to predict future price changes
- Generates buy signal when predicted change is positive
- Generates sell signal when predicted change is negative

**Calculation Formula:**
- $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n + \beta_{n+1} x_1^2 + \beta_{n+2} x_1x_2 + ... + \beta_m x_n^2 + \epsilon$

Where:
- $y$ is the predicted price change
- $x_i$ are the lagged closing prices (features)
- $\beta_i$ are the regression coefficients
- $\epsilon$ is the error term

**Advantages:**
- Can capture non-linear patterns in data
- More flexible than linear regression
- Adaptable to changing market conditions
- Objective decision-making based on data

**Disadvantages:**
- Requires sufficient historical data for training
- May overfit to historical data, especially with higher degree polynomials
- Black box nature makes it difficult to interpret
- Requires expertise in machine learning and parameter tuning

This strategy demonstrates how polynomial regression can be used to model more complex relationships in financial data.

#### 6. Random Forest Strategy

The Random Forest Strategy uses an ensemble of decision trees to predict future price movements based on historical data:

**Principle:**
- Uses historical closing prices as features
- Trains a random forest regression model to predict future price changes
- Generates buy signal when predicted change is positive
- Generates sell signal when predicted change is negative

**Calculation Formula:**
- $y = \frac{1}{n} \sum_{i=1}^{n} T_i(x)$

Where:
- $y$ is the predicted price change
- $T_i$ is the prediction of the $i$-th tree
- $x$ are the lagged closing prices (features)
- $n$ is the number of trees in the forest

**Advantages:**
- Can capture complex non-linear patterns in data
- Less prone to overfitting compared to individual decision trees
- Handles outliers well
- Provides feature importance rankings
- Adaptable to changing market conditions
- Objective decision-making based on data

**Disadvantages:**
- Requires sufficient historical data for training
- Black box nature makes it difficult to interpret
- Requires expertise in machine learning and parameter tuning
- Computationally more expensive than linear models

This strategy demonstrates how ensemble methods can be applied to financial markets for predictive modeling.

### Strategy Comparison

When choosing a trading strategy, it's important to consider the market conditions and your trading objectives:

1. **Moving Average Strategy**: Best suited for trending markets where clear directional moves occur.
2. **RSI Strategy**: Most effective in mean-reverting markets where prices tend to return to average levels.
3. **MACD Strategy**: Useful for identifying changes in market momentum and works well in trending markets.
4. **Linear Regression Strategy**: Offers potential for capturing complex patterns but requires careful validation to avoid overfitting.
5. **Polynomial Regression Strategy**: Can capture non-linear relationships in data, making it suitable for more complex market dynamics, but requires careful parameter tuning to prevent overfitting.
6. **Random Forest Strategy**: Offers robust predictions by combining multiple decision trees, reducing overfitting risk, but requires careful parameter tuning and is computationally more expensive.

In practice, combining multiple strategies or using different strategies for different market conditions often yields better results than relying on a single approach. The project's modular design makes it easy to experiment with different combinations and evaluate their performance through backtesting.

#### Backtesting Results Summary

The following table summarizes the backtesting results for each implemented strategy:

| Strategy Name | Total Return(%) | Trades | Win Rate(%) | Max Drawdown(%) |
|---------------|-----------------|--------|-------------|-----------------|
| Moving Average Strategy | -11.98 | 318 | 35.85 | -41.54 |
| RSI Strategy | -31.0 | 209 | 42.55 | -34.77 |
| MACD Strategy | -14.53 | 1163 | 39.02 | -38.33 |
| Linear Regression Strategy | 35.65 | 1388 | 74.2 | -13.13 |
| Polynomial Regression Strategy | N/A | N/A | N/A | N/A |
| Random Forest Strategy | N/A | N/A | N/A | N/A |

Note: The Polynomial Regression Strategy results are not yet available as it is a newly implemented strategy. Users are encouraged to run their own backtesting to evaluate its performance.

## Data

The project supports flexible data management through the `data_loader.py` module, which can handle various financial data formats and sources.

- **Supported Formats**: CSV files with standard OHLCV (Open, High, Low, Close, Volume) format
- **Data Location**: Project data is stored in the `stock_data/` directory
- **Extensibility**: The data loading system can be extended to support additional data sources such as databases or real-time feeds

The data loader provides preprocessing capabilities including:
- Data cleaning and validation
- Timezone handling and date alignment
- Resampling to different timeframes
- Technical indicator calculations

This modular approach allows researchers to focus on strategy development rather than data management complexities.

### Technical Indicator Calculations

The project's data loader and strategy modules work together to calculate various technical indicators used in the implemented strategies:

1. **Moving Averages**
   - Simple Moving Average (SMA): $MA_t(n) = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}$
   - Exponential Moving Average (EMA): $EMA_t = \alpha \times P_t + (1 - \alpha) \times EMA_{t-1}$, where $\alpha = \frac{2}{n+1}$

2. **RSI (Relative Strength Index)**
   - Gain calculation: $Gain_t = \max(0, P_t - P_{t-1})$
   - Loss calculation: $Loss_t = \max(0, P_{t-1} - P_t)$
   - Average gain: $AvgGain_t = \frac{\sum_{i=1}^{n} Gain_{t-i+1}}{n}$
   - Average loss: $AvgLoss_t = \frac{\sum_{i=1}^{n} Loss_{t-i+1}}{n}$
   - RSI: $RSI = 100 - \frac{100}{1 + \frac{AvgGain}{AvgLoss}}$

3. **MACD (Moving Average Convergence Divergence)**
   - Fast EMA: $EMA_{fast,t} = EMA(\text{Close}, n_{fast})$
   - Slow EMA: $EMA_{slow,t} = EMA(\text{Close}, n_{slow})$
   - MACD line: $MACD_{line,t} = EMA_{fast,t} - EMA_{slow,t}$
   - Signal line: $Signal_{line,t} = EMA(MACD_{line}, n_{signal})$
   - Histogram: $Histogram_t = MACD_{line,t} - Signal_{line,t}$

These calculations are performed automatically when using the respective strategies, ensuring consistent and accurate technical analysis.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.