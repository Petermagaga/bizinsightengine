from sklearn.linear_model import LinearRegression
import numpy as np


def predict_next(values):
    """
    Predict next value using linear regression.

    Example:
    [100, 120, 140] -> 160
    """

    # Remove invalid values
    values = [
        v for v in values
        if isinstance(v, (int, float))
    ]

    # Need enough history
    if len(values) < 3:
        return None

    try:
        X = np.arange(
            len(values)
        ).reshape(-1, 1)

        y = np.array(values)

        model = LinearRegression()
        model.fit(X, y)

        next_x = np.array([
            [len(values)]
        ])

        prediction = model.predict(
            next_x
        )[0]

        return round(
            float(prediction),
            2
        )

    except Exception:
        return None