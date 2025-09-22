import pandas as pd
import yaml


class DataLoader:
    """Class for loading and preprocessing stock data from CSV files."""
    
    def __init__(self):
        """
        Initialize the DataLoader by loading the data file path from config.
        """
        # Load configuration to get data file path and column names
        with open('data_loader.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.data_file = config.get('data_file', '600016.csv')
        self.column_names = config.get('column_names', {})
        self.numeric_columns = config.get('numeric_columns', ['收盘', '开盘', '高', '低', '涨跌幅'])
        self.volume_column = config.get('volume_column', '交易量')
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
            # Print the name of the file being read
            print(f"Reading data from file: {self.data_file}")
            # Read CSV file with utf-8 encoding
            self.data = pd.read_csv(self.data_file, encoding='utf-8')

            # Get column names from config
            date_col = self.column_names.get('date', '日期')
            close_col = self.column_names.get('close', '收盘')
            open_col = self.column_names.get('open', '开盘')
            high_col = self.column_names.get('high', '高')
            low_col = self.column_names.get('low', '低')
            change_col = self.column_names.get('change_percent', '涨跌幅')
            volume_col = self.column_names.get('volume', '交易量')

            # Convert date column
            self.data[date_col] = pd.to_datetime(self.data[date_col])

            # Sort by date (ensure data is in chronological order)
            self.data = self.data.sort_values(date_col)
            
            # Set date column as index
            self.data.set_index(date_col, inplace=True)

            # Convert numeric columns, remove percentage signs and convert to float
            for col in self.numeric_columns:
                if col == change_col:
                    # Process the change percentage column, remove % sign and convert to float
                    self.data[col] = self.data[col].str.replace('%', '').astype(float) / 100
                else:
                    # Process other numeric columns
                    self.data[col] = self.data[col].astype(float)

            # Process volume column, supporting both M (million) and B (billion) units
            volume_series = self.data[volume_col].copy()

            # Handle million units
            mask_m = volume_series.str.contains('M', na=False)
            if mask_m.any():
                volume_series.loc[mask_m] = volume_series.loc[mask_m].str.replace('M', '').astype(float) * 1e6

            # Handle billion units
            mask_b = volume_series.str.contains('B', na=False)
            if mask_b.any():
                volume_series.loc[mask_b] = volume_series.loc[mask_b].str.replace('B', '').astype(float) * 1e9

            # Convert to float
            self.data[volume_col] = volume_series.astype(float)

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