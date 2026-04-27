from typing import List, Any
import pandas as pd
from .models import GPSPoint

class DataLoader:
    """
    Responsible for ingesting raw data from a CSV, sanitizing it, 
    and returning a collection of strongly-typed GPSPoint objects.
    """
    NEEDED_COLUMNS = ['lat', 'lon', 'time']
    
    def __init__(self, file_source: Any):
        self.file_source = file_source

    def load_data(self) -> List[GPSPoint]:
        df = self._read_csv()
        self._validate_columns(df)
        df = self._handle_missing_values(df)
        df = self._validate_coordinates(df)
        df = self._sort_by_timestamp(df)
        return self._convert_to_model(df)
    
    def _read_csv(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.file_source)
            if df.empty:
                raise ValueError("CSV file is empty.")
            return df
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")
        
    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing_columns = [col for col in self.NEEDED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise KeyError(f"Missing required columns: {missing_columns}")
        
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'alt' not in df.columns:
            df['alt'] = 0.0
        else:
            df['alt'] = df['alt'].fillna(0.0)
        return df.dropna(subset=self.NEEDED_COLUMNS)
    
    def _validate_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[(df['lat'] >= -90) & (df['lat'] <= 90)]
        df = df[(df['lon'] >= -180) & (df['lon'] <= 180)]
        return df
    
    def _sort_by_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        return df.sort_values(by='time')

    def _convert_to_model(self, df: pd.DataFrame) -> List[GPSPoint]:
        return [
            GPSPoint(
                lat=float(row['lat']),
                lon=float(row['lon']),
                alt=float(row['alt']),
                time=float(row['time'])
            )
            for _, row in df.iterrows()
        ]
