import pandas as pd
import yaml


class DataLoader:
    """Class for loading and preprocessing stock data from CSV files."""
    
    def __init__(self):
        """
        Initialize the DataLoader by loading the data file path from config.
        """
        # Load configuration to get data file path
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.data_file = config.get('data_file', '600016.csv')
        self.data = None

    def load_data(self):
        """
        Load and preprocess stock data from CSV file.
        
        Returns:
            pd.DataFrame: Processed stock data
        
        Raises:
            Exception: If file is not found or data processing fails
        """
        try:
            # Read CSV file with utf-8 encoding
            self.data = pd.read_csv(self.data_file, encoding='utf-8')

            # Convert date column
            self.data['日期'] = pd.to_datetime(self.data['日期'])

            # Sort by date (ensure data is in chronological order)
            self.data = self.data.sort_values('日期')

            # Convert numeric columns, remove percentage signs and convert to float
            numeric_columns = ['收盘', '开盘', '高', '低', '涨跌幅']
            for col in numeric_columns:
                if col == '涨跌幅':
                    # Process the change percentage column, remove % sign and convert to float
                    self.data[col] = self.data[col].str.replace('%', '').astype(float) / 100
                else:
                    # Process other numeric columns
                    self.data[col] = self.data[col].astype(float)

            # Process volume column, supporting both M (million) and B (billion) units
            volume_series = self.data['交易量'].copy()

            # Handle million units
            mask_m = volume_series.str.contains('M', na=False)
            if mask_m.any():
                volume_series.loc[mask_m] = volume_series.loc[mask_m].str.replace('M', '').astype(float) * 1e6

            # Handle billion units
            mask_b = volume_series.str.contains('B', na=False)
            if mask_b.any():
                volume_series.loc[mask_b] = volume_series.loc[mask_b].str.replace('B', '').astype(float) * 1e9

            # Convert to float
            self.data['交易量'] = volume_series.astype(float)

            return self.data

        except FileNotFoundError:
            raise Exception(f"Data file {self.data_file} not found, please check if the file path is correct")
        except Exception as e:
            raise Exception(f"Error occurred while loading data: {str(e)}")

    def get_data(self):
        """
        Get the processed stock data.
        
        Returns:
            pd.DataFrame: Processed stock data
        """
        if self.data is None:
            self.load_data()
        return self.data