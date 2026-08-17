    import numpy as np
    sigma = np.array([
        [0.034969, 0.00954141, -0.00758712],
        [0.00954141, 0.059049, 0.02806032],
        [-0.00758712, 0.02806032, 0.097344]
    ])
    inv_sigma = np.linalg.inv(sigma)
    ones = np.ones(3)
    x = inv_sigma @ ones
    # x = [28.85555737, 7.32701365, 10.41076707]
    S = np.sum(x)
    # S = 46.59333809
    w = x / S
    # w = [0.61938593, 0.15727393, 0.22334014]
    var = 1 / S
    # var = 0.02146230
    vol = np.sqrt(var)
    # vol = 0.14650339
    