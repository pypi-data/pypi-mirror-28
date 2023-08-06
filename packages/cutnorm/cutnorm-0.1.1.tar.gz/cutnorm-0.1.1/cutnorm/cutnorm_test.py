import numpy as np
from cutnorm import cutnorm
import matplotlib.pyplot as plt

n = 1000
a = np.ones((n, n))
a_small = np.ones((n // 2, n // 2))
b = np.ones((n, n))
b[n // 3:-n // 3, n // 3:-n // 3] = 0

print("Opt obj function val: " + str(np.sum(a - b) / np.sum(a)))

# # Same-dim, not weighted
# objfval, S, T, w, debug_info = cutnorm(a, b)
# print("Same Dim, not weighted")
# print(objfval)

# # Diff-dim, not weighted
# objfval, S, T, w, debug_info = cutnorm(a_small, b)
# print("Diff Dim, not weighted")
# print(objfval)

# # Diff-dim Weighted
# objfval, S, T, w, debug_info = cutnorm(a_small, b,
#                                        np.ones(n // 2) / (n // 2),
#                                        np.ones(n) / n)
# print("Diff Dim, weighted")
# print(objfval)

# Same-dim, not weighted, logn
objfval, S, T, w, debug_info = cutnorm(a, b, logn_lowrank=True, debug=True)
print("Same Dim, not weighted, lowrank")
print(objfval)
print("Debug Keys: ", debug_info.keys())
