import numpy as np

def compute_bond_metrics(face_value=100, coupon_rate=0.046, ytm=0.053, periods=7):
    """
    Calculate price, Macaulay duration, modified duration, and convexity
    for an annual coupon bullet bond.

    Parameters
    ----------
    face_value : float
        Par value of the bond
    coupon_rate : float
        Annual coupon rate
    ytm : float
        Yield to maturity (annual, compounded annually)
    periods : int
        Number of years to maturity

    Returns
    -------
    dict
        Dictionary with keys 'price', 'macaulay_duration_years',
        'modified_duration_years', 'convexity'
    """
    coupon = face_value * coupon_rate
    t = np.arange(1, periods + 1)

    # Present value of each cash flow
    pv_coupons = coupon / (1 + ytm) ** t
    pv_face = face_value / (1 + ytm) ** periods
    cashflow_pv = np.append(pv_coupons, pv_face)

    # Total price
    price = np.sum(cashflow_pv)

    # Weights of each cash flow in the price
    weights = cashflow_pv / price

    # Time vector: coupon times 1..periods, face value at 'periods'
    times = np.append(t, periods)

    # Macaulay duration (weighted average time to receipt of cash flows)
    macaulay_duration = np.sum(weights * times)

    # Modified duration
    modified_duration = macaulay_duration / (1 + ytm)

    # Convexity: sum[ t * (t+1) * PV(CF) ] / (price * (1+ytm)^2)
    convexity = np.sum(times * (times + 1) * cashflow_pv) / (price * (1 + ytm) ** 2)

    result = {
        'price': price,
        'macaulay_duration_years': macaulay_duration,
        'modified_duration_years': modified_duration,
        'convexity': convexity
    }
    return result

if __name__ == "__main__":
    # Bonds parameters as per task
    result = compute_bond_metrics(
        face_value=100,
        coupon_rate=0.046,
        ytm=0.053,
        periods=7
    )
    print(result)
