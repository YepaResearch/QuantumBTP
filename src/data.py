import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

def fetch_data(_src):
    """
    Load the dataset from a CSV file.

    Args:
    _src (Filepath): Import CSV File Path.

    Returns:
    _dfRaw: DataFrame with Raw Stats

    """
    # Import Data From CSV
    _rawDF = pd.read_csv(
        _src, 
        dtype={
            'time' : object,
            'open' : float, 
            'high' : float, 
            'low'  : float, 
            'close': float  
        },
        index_col=[0],
    )
    return _rawDF

def clean_data(_df):
    """

    Clean Raw Format Stats Dataframe.

    Args:
    _df (DataFrame): Raw Stats DataFrame To Clean.

    Returns:
    _cleanDF: DataFrame with Clean Stats

    """
    # Add DateTime Property from Index
    _df['DateTime']=_df.index.astype(str)

    # Reset Index to unique ints
    _df = _df.reset_index(drop=True) 

    # Fake Time to mantain NY Time
    _df['zDateTime'] = _df['DateTime'].str[:-6] + '+00:00'

    # Convert Fake Time to 'Datetime'
    _df['zUTCDateTime'] = pd.to_datetime(_df['zDateTime'], utc=True)

    # Clean DF 
    _data = {
        'DateTime': _df.zUTCDateTime.copy(),
        'Open': _df.open.copy(),
        'High': _df.high.copy(),
        'Low': _df.low.copy(),
        'Close': _df.close.copy()
    }
    
    # Create Clean DF
    _cleanDF = pd.DataFrame(_data)

    # Add Time Variables
    _cleanDF['HourOfDay'] = _cleanDF['DateTime'].dt.hour.astype(int)
    _cleanDF['Minute'] = _cleanDF['DateTime'].dt.minute.astype(int)
    _cleanDF['DayOfWeek'] = _cleanDF['DateTime'].dt.dayofweek.astype(int)
    _cleanDF['Day'] = _cleanDF['DateTime'].dt.day.astype(int)
    _cleanDF['Month'] = _cleanDF['DateTime'].dt.month.astype(int)
    _cleanDF['Year'] = _cleanDF['DateTime'].dt.year.astype(int)
    _cleanDF['WeekOfYear'] = _cleanDF['DateTime'].dt.isocalendar().week

    # Calculate Up (1) vs Down (0) Close
    _cleanDF['xClose'] = (_cleanDF['Open'] < _cleanDF['Close']).astype(int)
    
    return _cleanDF


def normalize_data(_df):
    """
    Apply Z-score normalization to the OHLC columns.
    
    Args:
    _df (DataFrame): DataFrame To Normalize

    Returns:
    _df (DataFrame): Input DataFrame with Normalized Stats
    
    """
    
    _scaler = StandardScaler()
    _ohlcColumns = ['Open', 'High', 'Low', 'Close']
    _df[_ohlcColumns] = _scaler.fit_transform(_df[_ohlcColumns])
    
    return _df


def robust_normalize_data(_df):
    """Apply robust normalization to the OHLC columns."""
    _scaler = RobustScaler()
    _ohlcColumns = ['Open', 'High', 'Low', 'Close']
    _df[_ohlcColumns] = _scaler.fit_transform(_df[_ohlcColumns])
    return _df
