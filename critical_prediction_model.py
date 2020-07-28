import numpy as np
import pandas as pd


def _shift_date(df, days):
    # shift date index by 'days'
    return pd.Series(df.values, index=[d + pd.Timedelta('{}d'.format(days)) for d in df.index])


def _critical_released_estimate(x):
    # estimate released\deceased each day depending on critical patients additions in last 50 days (weighted by pdf)
    x = x[::-1].values
    p = np.arange(len(x))+1
    p = pd.Series(2 / (1 + np.exp(-0.125*p)) - 1)
    p = p-p.shift(1).fillna(0)
    return (x * p).sum()


def predict_critical_cases(new_daily_critical_history,
                            cases_20_59_history, cases_60_74_history, cases_75_plus_history,
                            total_critical_today):
    """
    Estimate total critical patients next week (+6 days from today)

    Args:
        new_daily_critical_history (pandas Series): Series with date index and containing data of new critical patients. Best to have 50 days history from today
        cases_20_59_history (pandas Series): Series with date index and containing data of new COVID19 cases in ages [20-59]
        cases_60_74_history (pandas Series): Series with date index and containing data of new COVID19 cases in ages [60-74]
        cases_75_plus_history (pandas Series): Series with date index and containing data of new COVID19 cases in ages 75+
        total_critical_today (integer): total critical patients today

    Returns:
       total_critical_next_week (integer): total estimated critical patients next week (+6 days from today)
    """

    # Gather and join all Series inputs in one dataframe with date as index
    df_pred = pd.DataFrame(new_daily_critical_history.rename('new_daily_critical'))
    for name, series in {'cases_20-59':cases_20_59_history, 'cases_60-74':cases_60_74_history, 'cases_75+':cases_75_plus_history}.items():
        df_pred = df_pred.join(series.rename(name))

    # predict critical patients from age-structure of cases 6 days forward
    new_daily_critical_pred = 0.008 * df_pred['cases_20-59'] + 0.07 * df_pred['cases_60-74'] + 0.27 * df_pred['cases_75+']
    # Apply empirical multiplier for change in critical cases definitions starting at July 6th
    new_daily_critical_pred.loc[pd.to_datetime('2020-7-6'):] *= 1.4
    # shift prediction 6 days forward
    df_pred = df_pred.join(_shift_date(new_daily_critical_pred, days=6).rename('new_daily_critical_pred'), how='outer')

    
    # Estimate total released\deceased in future week
    for idx, row in (df_pred.iloc[-6:].iterrows()):
        # append critical patients additions of: 43 days in the past, today, and 6 days predictions in the future
        x = df_pred.loc[(idx-pd.to_timedelta('50 days')):(idx-pd.to_timedelta('7 days')),'new_daily_critical']
        next_week_daily_critical_pred = df_pred.loc[(idx-pd.to_timedelta('6 days')):idx,'new_daily_critical_pred']
        x = x.append(next_week_daily_critical_pred)

        # estimate released\deceased each day depending on critical patients additions in last 50 days (weighted by pdf)
        released = x.rolling(window=50, min_periods=20).apply(lambda x: _critical_released_estimate(x))

        # subtract released\deceased  from predicted critical patients additions
        next_week_added_minus_released = next_week_daily_critical_pred - released.loc[(idx-pd.to_timedelta('6 days')):idx]
        df_pred.loc[idx,'added_minus_released_future_week'] = next_week_added_minus_released.sum()

    # total estimated critical patients next week (+6 days from today)
    total_critical_next_week = total_critical_today + df_pred['added_minus_released_future_week'].iloc[-1]

    return total_critical_next_week