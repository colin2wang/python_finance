import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Set Chinese display
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False  # Correctly display negative signs

class Visualizer:
    """Visualization tool class for displaying strategy results."""
    
    def __init__(self):
        """Initialize the Visualizer."""
        pass

    def plot_strategy_performance(self, data, strategy_name, metrics=None):
        """
        Plot the performance of a single strategy.
        
        Args:
            data (pd.DataFrame): Strategy data with signals and asset values
            strategy_name (str): Name of the strategy to display
            metrics (dict, optional): Strategy performance metrics
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Plot price and trading signals
        ax1.plot(data.index, data['收盘'], label='Closing Price', color='blue')

        # Mark buy and sell signals
        buy_signals = data[data['信号'] == 1]
        sell_signals = data[data['信号'] == -1]

        ax1.scatter(buy_signals.index, buy_signals['收盘'],
                    marker='^', color='g', label='Buy Signal', alpha=1)
        ax1.scatter(sell_signals.index, sell_signals['收盘'],
                    marker='v', color='r', label='Sell Signal', alpha=1)

        ax1.set_title(f'{strategy_name} Strategy Performance')
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)

        # Plot asset curve
        ax2.plot(data.index, data['资产价值'], label='Strategy Assets', color='green')
        ax2.axhline(y=data['资产价值'].iloc[0], color='r', linestyle='--', label='Initial Capital')

        ax2.set_title('Asset Changes')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Asset Value')
        ax2.legend()
        ax2.grid(True)

        # Set date format
        plt.gcf().autofmt_xdate()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # Rotate x-axis labels to prevent overlap
        for ax in [ax1, ax2]:
            ax.tick_params(axis='x', rotation=45)
            for label in ax.get_xticklabels():
                label.set_ha('right')

        # Add metrics information
        if metrics:
            info_text = f"Total Return: {metrics.get('总收益率(%)', 'N/A')}%\nTrade Count: {metrics.get('交易次数', 'N/A')}\nWin Rate: {metrics.get('胜率(%)', 'N/A')}%\nMax Drawdown: {metrics.get('最大回撤(%)', 'N/A')}%"
            ax2.text(0.02, 0.98, info_text, transform=ax2.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        plt.show()

    def plot_strategies_comparison(self, results_dict):
        """
        Plot comparison of strategy performances.
        
        Args:
            results_dict (dict): Dictionary of strategy results
        """
        plt.figure(figsize=(12, 6))

        for name, data in results_dict.items():
            plt.plot(data.index, data['资产价值'], label=name)

        plt.title('Strategy Performance Comparison')
        plt.xlabel('Date')
        plt.ylabel('Asset Value')
        plt.legend()
        plt.grid(True)
        plt.gcf().autofmt_xdate()
        # Rotate x-axis labels and use abbreviations to prevent overlap
        plt.xticks(rotation=45, ha='right')
        plt.show()

    def plot_metrics_comparison(self, metrics_dict):
        """
        Plot comparison of strategy metrics.
        
        Args:
            metrics_dict (dict): Dictionary of strategy metrics
        """
        # Prepare data
        strategies = list(metrics_dict.keys())
        total_returns = [metrics_dict[s]['总收益率(%)'] for s in strategies]
        win_rates = [metrics_dict[s]['胜率(%)'] for s in strategies]
        max_drawdowns = [abs(metrics_dict[s]['最大回撤(%)']) for s in strategies]

        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Total return comparison
        bars1 = ax1.bar(strategies, total_returns, color='skyblue')
        ax1.set_title('Total Return Comparison')
        ax1.set_ylabel('Return (%)')
        # Rotate x-axis labels to prevent overlap
        ax1.tick_params(axis='x', rotation=45)
        for label in ax1.get_xticklabels():
            label.set_ha('right')
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}', ha='center', va='bottom')

        # Win rate comparison
        bars2 = ax2.bar(strategies, win_rates, color='lightgreen')
        ax2.set_title('Win Rate Comparison')
        ax2.set_ylabel('Win Rate (%)')
        # Rotate x-axis labels to prevent overlap
        ax2.tick_params(axis='x', rotation=45)
        for label in ax2.get_xticklabels():
            label.set_ha('right')
        # Add value labels on bars
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}', ha='center', va='bottom')

        # Max drawdown comparison
        bars3 = ax3.bar(strategies, max_drawdowns, color='lightcoral')
        ax3.set_title('Max Drawdown Comparison')
        ax3.set_ylabel('Drawdown (%)')
        # Rotate x-axis labels to prevent overlap
        ax3.tick_params(axis='x', rotation=45)
        for label in ax3.get_xticklabels():
            label.set_ha('right')
        # Add value labels on bars
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.2f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

    def show(self):
        """Show all charts."""
        plt.show()