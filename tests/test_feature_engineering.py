import pandas as pd
from stock_keeper.data.feature_engineering import compute_returns, compute_moving_average, compute_volatility, compute_momentum

def test_feature_functions():
    df = pd.DataFrame({"close": [100, 102, 101, 103, 105]})
    returns = compute_returns(df)
    assert abs(returns.iloc[1] - 0.02) < 1e-6
    ma = compute_moving_average(df, window=2)
    assert abs(ma.iloc[-1] - 104) < 1e-6
    vol = compute_volatility(df, window=2)
    assert vol.iloc[-1] >= 0
    mom = compute_momentum(df, window=2)
    assert abs(mom.iloc[-1] - 0.039603960396039604) < 1e-9
