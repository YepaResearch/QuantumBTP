import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def get_htf_xotx(_df, _tf, _h, _l):
    _xh = _df.groupby(_df['DateTime'].dt.to_period(_tf))['High'].transform('max')
    _xl = _df.groupby(_df['DateTime'].dt.to_period(_tf))['Low'].transform('min')
    
    # Compare each row's H / L to MH / ML
    _df[_h] = (_df['High'] == _xh).astype(int)
    _df[_l] = (_df['Low']  == _xl).astype(int)

    return _df
    
def get_xotw(_df):

    # Group by 'WeekOfYear'
    _weekOfYear = _df.groupby(['Year','WeekOfYear'])
    
    # Calculate the 'HighestHigh' and 'LowestLow' indicators
    _df['WH'] = (_df['High'] == _weekOfYear['High'].transform('max')).astype(int)
    _df['WL'] = (_df['Low']  == _weekOfYear['Low'].transform('min')).astype(int)
    
    return _df

def get_bar_change(_df):
    """

    Clean Raw Format Stats Dataframe.

    Args:
    _df (DataFrame): DataFrame To Get H-L / O-C Delta From.

    Returns:
    _dfData: DataFrame with H-L / O-C Delta Columns

    """
  # Clean DF Data to calculate Bar Change
    _data = {
        'DateTime': _df.DateTime.copy(),
        'DayOfWeek': _df.DayOfWeek.copy(),
        'Hour': _df.HourOfDay.copy(),
        'Minute': _df.Minute.copy(),
        'Day': _df.Day.copy(),
        'Month': _df.Month.copy(),
        'Year': _df.Year.copy(),
        'CloseType': _df.xClose.copy()
    }

    # Create DF
    _df_data = pd.DataFrame(_data)

    # Calculate HL & OC Diff
    _df_data['HL'] = (_df['High'] - _df['Low'])
    _df_data['OC'] = (_df['Close'] - _df['Open'])

    # Calculate HL & OC % Diff
    _df_data['HLP'] = ((_df['High'] - _df['Low']) / _df['High']) * 100
    _df_data['OCP'] = ((_df['Close'] - _df['Open']) / _df['Open']) * 100

    # Get OC Diff & OC % Diff Abs Value
    _df_data['OC'] = _df_data['OC'].abs()
    _df_data['OCP'] = _df_data['OCP'].abs()

    return _df_data

def plot_atr(_df, _filter, _pct, _x_range, _show_grid):
    """

    Plot Average True Range Distribution By Time Range.

    Args:
    _df     (DataFrame): DataFrame To Calculate ATR From.
    _filter       (str): GroupBy() Timeframe Filter.
    _pct         (bool): Get ATR in % Value.
    _x_range      (int): X-Axis Range.
    _show_grid   (bool): Show Grid.

    Returns:
    _dfData: DataFrame with H-L / O-C Delta Columns

    """
    
    _atr_hl = 'HLP' if _pct else 'HL'
    _atr_oc = 'OCP' if _pct else 'OC'
    
    # Group by the hour of the day and calculate the average percentage differences
    _getATR = _df.groupby(_filter)[[_atr_hl, _atr_oc]].mean()
    
    _xTrueRange = range(0, 60, 5) if _filter == 'Minute' else range(_xRange)
    
    plt.figure(figsize=(12, 6))
    # Plot DaysOfWeek Diff
    _getATR[_atr_hl].plot(label='H-L ATR', marker='x')
    _getATR[_atr_oc].plot(label='O-C ATR', marker='o')
    plt.title('ATR  / ' + _filter)
    plt.xlabel(_filter)
    plt.ylabel('ATR')
    plt.legend()
    plt.grid(_showGrid)
    plt.xticks(_xTrueRange)
    plt.show()
    
    
def plot_adr(_dr, _tf, _hl, _oc, _grid):
    _adr_mean = _dr.groupby(_tf)[[_hl, _oc]].mean()
    
    # Plot DaysOfWeek %Diff
    plt.figure(figsize=(12, 6))
    
    _adr_mean[_hl].plot(label=' ATR', marker='x')
    _adr_mean[_oc].plot(label=' ATR', marker='o')
    
    plt.title('ATR % / Day Of Week')
    plt.xlabel('Day Of Week')
    plt.ylabel('ATR %')
    plt.legend()
    plt.grid(_grid)
    plt.xticks(range(7))
    plt.show()
    
def add_binary_targets(_df):
    """Create binary target variables for the highest and lowest prices of the day."""
    
    _df['isHigh'] = _df.groupby(_df.index.date)['High'].transform(lambda _x: _x == _x.max()).astype(int)
    _df['isLow'] = _df.groupby(_df.index.date)['Low'].transform(lambda _x: _x == _x.min()).astype(int)
    return _df


def add_lag_delta(_df, _periods):
    """
    Add Lagged Delta for OHLC Values.
    
    Args:
    _df     (DataFrame): DataFrame To Calculate Lag From.
    _periods      (int): Lag Periods.

    Returns:
    _df: DataFrame with Lag Delta Column

    """
    for _col in ['Open', 'High', 'Low', 'Close']:
        _df[f'{_col}Change'] = _df[_col].diff(periods=_periods)
    return _df

def calculate_binary_variables(df):
    # Calculate the max and min per day using DateTime column
    df['DH'] = df.groupby(df['DateTime'].dt.to_period("D"))['High'].transform('max')
    df['DL'] = df.groupby(df['DateTime'].dt.to_period("D"))['Low'].transform('min')

    # Compare each row's high and low to the daily max and min to set binary flags
    df['DH'] = (df['High'] == df['DH']).astype(int)
    df['DL'] = (df['Low'] == df['DL']).astype(int)

    return df

def get_close_direction(df):
    """
    Calculates a binary indicator for whether the daily close is higher than the daily open.

    Args:
    df (DataFrame): DataFrame containing the OHLC data.

    Returns:
    DataFrame: Updated DataFrame with daily return direction (DR).
    """
    # Calculate first open and last close for each day
    daily_stats = df.groupby(df['DateTime'].dt.to_period("D")).agg({'Open': 'first', 'Close': 'last'})
    
    # Map daily return direction back to the original DataFrame
    daily_return = (daily_stats['Close'] > daily_stats['Open']).astype(int)
    df['DR'] = df['DateTime'].dt.to_period("D").map(daily_return)

    return df
