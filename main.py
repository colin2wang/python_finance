from data_loader import DataLoader
from strategies import MovingAverageStrategy, RSIStrategy, MACDStrategy, LinearRegressionStrategy, PolynomialRegressionStrategy, RandomForestStrategy
from backtester import Backtester
from visualizer import Visualizer
import yaml

def main():
    """
    Main function to run the backtesting process for all trading strategies.
    
    This function loads configuration, data, initializes strategies,
    runs backtesting, and visualizes results.
    """
    # 1. Load configuration
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    initial_capital = config.get('initial_capital', 100000)
    
    # 2. Load data
    print("Loading stock data...")
    data_loader = DataLoader()
    data = data_loader.get_data()
    print(f"Successfully loaded {len(data)} stock data entries")
    
    # 3. Initialize strategies
    strategies = {
        'Moving Average Strategy': MovingAverageStrategy(
            data, 
            params=config['strategies']['moving_average']
        ),
        'RSI Strategy': RSIStrategy(
            data, 
            params=config['strategies']['rsi']
        ),
        'MACD Strategy': MACDStrategy(
            data, 
            params=config['strategies']['macd']
        ),
        'Linear Regression Strategy': LinearRegressionStrategy(
            data, 
            params=config['strategies'].get('ml', {})
        ),
        'Polynomial Regression Strategy': PolynomialRegressionStrategy(
            data, 
            params=config['strategies'].get('ml', {})
        ),
        'Random Forest Strategy': RandomForestStrategy(
            data, 
            params=config['strategies'].get('ml', {})
        )
    }
    
    # 4. Run backtesting and collect results
    results = {}
    metrics = {}
    
    print("Running strategy backtesting...")
    for name, strategy in strategies.items():
        print(f"Running {name}...")
        backtester = Backtester(data, strategy, initial_capital)
        strategy_results = backtester.run()
        strategy_metrics = backtester.get_metrics()
        
        results[name] = strategy_results
        metrics[name] = strategy_metrics
        
        print(f"{name} backtesting completed. Total return: {strategy_metrics['总收益率(%)']}%")
    
    # 5. Visualize results
    print("Generating visualization results...")
    visualizer = Visualizer()
    
    # Plot detailed performance for each strategy
    for name, result in results.items():
        visualizer.plot_strategy_performance(result, name, metrics[name])
    
    # Plot strategy comparison
    visualizer.plot_strategies_comparison(results)
    visualizer.plot_metrics_comparison(metrics)
    
    # Show all charts
    visualizer.show()
    
    # 6. Print strategy comparison summary
    print("\nStrategy Comparison Summary:")
    print("{:<20} {:<15} {:<10} {:<10} {:<15}".format(
        "Strategy Name", "Total Return(%)", "Trades", "Win Rate(%)", "Max Drawdown(%)"))
    print("-" * 75)
    for name, metric in metrics.items():
        print("{:<20} {:<15} {:<10} {:<10} {:<15}".format(
            name,
            metric['总收益率(%)'],
            metric['交易次数'],
            metric['胜率(%)'],
            metric['最大回撤(%)']
        ))

if __name__ == "__main__":
    main()