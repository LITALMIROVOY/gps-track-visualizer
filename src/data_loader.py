from typing import List, Any
import pandas as pd
from .models import GPSPoint

class DataLoader:
    """
    Handles the ingestion, sanitization, and transformation of raw GPS data.
    
    This class reads a CSV source, validates that essential GPS columns are present,
    cleanses invalid or missing data, and converts the resulting rows into 
    strongly-typed GPSPoint objects.

    Attributes:
        file_source (Any): The path to the CSV file or a file-like object (e.g., from Streamlit).
        NEEDED_COLUMNS (list): Constant defining the required columns for processing.
    """
    
    NEEDED_COLUMNS = ['lat', 'lon', 'time']
    
    def __init__(self, file_source: Any):
        """Initializes the DataLoader with a data source."""
        self.file_source = file_source

    def load_data(self) -> List[GPSPoint]:
        """
        Executes the full data processing pipeline.
        
        Sequence: Read -> Validate -> Clean -> Sort -> Model Conversion.
        
        Returns:
            List[GPSPoint]: A chronologically sorted list of validated GPS points.
        """
        df = self.read_csv()
        self.validate_columns(df)
        df = self.handle_missing_values(df)
        df = self.validate_coordinates(df)
        df = self.sort_by_timestamp(df)
        return self.convert_to_model(df)
    
    def read_csv(self) -> pd.DataFrame:
        """Reads the CSV file into a pandas DataFrame with basic error handling."""
        try:
            df = pd.read_csv(self.file_source)
            if df.empty:
                raise ValueError("CSV file is empty.")
            return df
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")
        
    def validate_columns(self, df: pd.DataFrame) -> None:
        """Checks for the existence of mandatory GPS columns."""
        missing_columns = [col for col in self.NEEDED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing required columns: {missing_columns}")
        
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the dataset by handling missing entries.
        
        - If 'alt' is missing, it is initialized to 0.0.
        - Rows missing core GPS data (lat, lon, time) are dropped.
        """
        if 'alt' not in df.columns:
            df['alt'] = 0.0
        else:
            df['alt'] = df['alt'].fillna(0.0)
        return df.dropna(subset=self.NEEDED_COLUMNS)
    
    def validate_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filters out rows with geographically impossible coordinates."""
        df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
        df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
        return df
    
    def sort_by_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensures the data is processed in chronological order.
        Converts time column to numeric and sorts the DataFrame.
        """
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        return df.sort_values(by='time')

    def convert_to_model(self, df: pd.DataFrame) -> List[GPSPoint]:
        """
        Maps DataFrame rows to GPSPoint dataclass objects.
        This provides Type Safety for the Business Logic and Visualization layers.
        """
        return [
            GPSPoint(
                lat=float(row['lat']),
                lon=float(row['lon']),
                alt=float(row['alt']),
                time=float(row['time'])
            )
            for _, row in df.iterrows()
        ]
