import pandas as pd
import numpy as np

def getHTFXOTX(_df, _tf, _h, _l):
    _XH = _df.groupby(_df['DateTime'].dt.to_period(_tf))['High'].transform('max')
    _XL = _df.groupby(_df['DateTime'].dt.to_period(_tf))['Low'].transform('min')
    
    # Compare each row's H / L to MH / ML
    _df[_h] = (_df['High'] == _XH).astype(int)
    _df[_l] = (_df['Low']  == _XL).astype(int)

    return _df
    
def getXOTW(_df):

    # Group by 'WeekOfYear'
    _weekOfYear = _df.groupby(['Year','WeekOfYear'])
    
    # Calculate the 'HighestHigh' and 'LowestLow' indicators
    _df['WH'] = (_df['High'] == _weekOfYear['High'].transform('max')).astype(int)
    _df['WL'] = (_df['Low']  == _weekOfYear['Low'].transform('min')).astype(int)
    
    return _df