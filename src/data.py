# Imports
import pandas as pd

def fetchData(_src):
    # Import Data From CSV
    _data = pd.read_csv(
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
    return _data

def cleanData(_rawDF):
    
    # Add DateTime Property from Index
    _rawDF['DateTime']=_rawDF.index.astype(str)

    # Reset Index to unique ints
    _rawDF = _rawDF.reset_index(drop=True) 

    # Fake Time to mantain NY Time
    _rawDF['zDateTime'] = _rawDF['DateTime'].str[:-6] + '+00:00'

    # Convert Fake Time to 'Datetime'
    _rawDF['zUTCDateTime'] = pd.to_datetime(_rawDF['zDateTime'], utc=True)

    # Clean DF 
    _data = {
        'DateTime': _rawDF.zUTCDateTime.copy(),
        'Open': _rawDF.open.copy(),
        'High': _rawDF.high.copy(),
        'Low': _rawDF.low.copy(),
        'Close': _rawDF.close.copy()
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
