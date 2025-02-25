from typing import List, Tuple
from scipy.interpolate import make_interp_spline
import numpy as np

def smooth_curve(x: List[int], y: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    x = np.array(x)
    y = np.array(y)
    spline = make_interp_spline(x, y)
    x_new = np.linspace(x.min(), x.max(), 50)
    y_new = spline(x_new)
    return x_new, y_new