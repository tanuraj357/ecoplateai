import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train(sales, menu):
    """Train a basic demand model. Sales needs item, date, and portions_sold columns."""
    data = sales.copy()
    target = next((c for c in ["portions_sold", "quantity", "sales", "demand"] if c in data.columns), None)
    if target is None:
        raise ValueError(f"Sales data needs a demand column such as portions_sold. Found: {list(data.columns)}")
    if "item" not in data.columns:
        raise ValueError("Sales data must contain an 'item' column.")
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data["day_of_week"] = data["date"].dt.dayofweek.fillna(0)
        data["month"] = data["date"].dt.month.fillna(1)
        data["day_of_month"] = data["date"].dt.day.fillna(1)
    else:
        data["day_of_week"], data["month"], data["day_of_month"] = 0, 1, 1
    for col, default in [("temperature", 25), ("event_attendees", 0), ("is_holiday", 0)]:
        if col not in data.columns:
            data[col] = default
    item_names = sorted(data["item"].astype(str).unique())
    item_codes = {name: i for i, name in enumerate(item_names)}
    data["item_code"] = data["item"].astype(str).map(item_codes)
    features = ["item_code", "day_of_week", "month", "day_of_month", "temperature", "event_attendees", "is_holiday"]
    X = data[features].apply(pd.to_numeric, errors="coerce").fillna(0)
    y = pd.to_numeric(data[target], errors="coerce").fillna(0).clip(lower=0)
    model = RandomForestRegressor(n_estimators=150, random_state=42, min_samples_leaf=2)
    model.fit(X, y)
    model.eco_item_codes = item_codes
    model.eco_feature_cols = features
    return model

def forecast(model, sales, menu, target_date, temperature=25, event_attendees=0, is_holiday=False):
    """Return a DataFrame with item and predicted_demand columns."""
    items = menu["item"].dropna().astype(str).unique().tolist() if "item" in menu.columns else []
    if not items and "item" in sales.columns:
        items = sales["item"].dropna().astype(str).unique().tolist()
    date = pd.to_datetime(target_date)
    codes = getattr(model, "eco_item_codes", {})
    rows = []
    for item in items:
        x = pd.DataFrame([{
            "item_code": codes.get(item, 0),
            "day_of_week": date.dayofweek,
            "month": date.month,
            "day_of_month": date.day,
            "temperature": float(temperature),
            "event_attendees": float(event_attendees),
            "is_holiday": int(bool(is_holiday)),
        }])
        rows.append({"item": item, "predicted_demand": max(0, int(round(float(model.predict(x)[0]))))})
    return pd.DataFrame(rows)

def recommend(forecast_df, menu, kitchen_capacity=None, goodwill=1.05):
    """Suggest prep quantities from forecast demand, optionally respecting total kitchen capacity."""
    result = forecast_df.merge(menu, on="item", how="left", suffixes=("", "_menu")).copy()
    demand_col = "predicted_demand" if "predicted_demand" in result.columns else "forecast"
    if demand_col not in result.columns:
        raise ValueError("Forecast dataframe needs a predicted_demand column.")
    result["recommended_prep"] = np.ceil(pd.to_numeric(result[demand_col], errors="coerce").fillna(0) * float(goodwill)).astype(int)
    if kitchen_capacity is not None:
        capacity = max(0, int(kitchen_capacity))
        total = int(result["recommended_prep"].sum())
        if total > capacity and total > 0:
            scaled = result["recommended_prep"] * capacity / total
            result["recommended_prep"] = np.floor(scaled).astype(int)
            left = capacity - int(result["recommended_prep"].sum())
            fractions = (scaled - np.floor(scaled)).sort_values(ascending=False)
            for idx in fractions.index[:left]:
                result.loc[idx, "recommended_prep"] += 1
    result["expected_surplus"] = (result["recommended_prep"] - pd.to_numeric(result[demand_col], errors="coerce").fillna(0)).clip(lower=0).round().astype(int)
    return result

def backtest(sales, menu, test_size=0.2):
    """Evaluate demand predictions on a held-out tail of the sales data."""
    data = sales.copy()
    target = next((c for c in ["portions_sold", "quantity", "sales", "demand"] if c in data.columns), None)
    if target is None or "item" not in data.columns or len(data) < 5:
        return {"mae": None, "waste_rate": None, "predictions": pd.DataFrame()}
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        data = data.sort_values("date")
        data["day_of_week"] = data["date"].dt.dayofweek.fillna(0)
        data["month"] = data["date"].dt.month.fillna(1)
        data["day_of_month"] = data["date"].dt.day.fillna(1)
    else:
        data["day_of_week"], data["month"], data["day_of_month"] = 0, 1, 1
    for col, default in [("temperature", 25), ("event_attendees", 0), ("is_holiday", 0)]:
        if col not in data.columns:
            data[col] = default
    data["item_code"] = data["item"].astype(str).astype("category").cat.codes
    features = ["item_code", "day_of_week", "month", "day_of_month", "temperature", "event_attendees", "is_holiday"]
    X = data[features].apply(pd.to_numeric, errors="coerce").fillna(0)
    y = pd.to_numeric(data[target], errors="coerce").fillna(0).clip(lower=0)
    split = max(1, min(len(data)-1, int(len(data) * (1-test_size))))
    model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=2)
    model.fit(X.iloc[:split], y.iloc[:split])
    pred = np.maximum(0, model.predict(X.iloc[split:]))
    actual = y.iloc[split:].to_numpy()
    surplus = np.maximum(0, pred - actual)
    predictions = data.iloc[split:][["item"]].copy()
    predictions["actual"] = actual
    predictions["predicted"] = np.rint(pred).astype(int)
    predictions["surplus"] = np.rint(surplus).astype(int)
    return {"mae": float(mean_absolute_error(actual, pred)), "waste_rate": float(surplus.sum()/max(1, pred.sum())), "predictions": predictions}
