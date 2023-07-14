from math import pow, dist
from scipy.optimize import minimize

# Define function
C0 = -1
C1 = 5
C2 = -5
C3 = 6
f = lambda x: C0 + C1 * x + C2 * pow(x, 2) + C3 * pow(x, 3)

# Define function to minimize
p_x = 12
p_y = -7
min_f = lambda x: pow(x-p_x, 2) + pow(f(x) - p_y, 2)

# Minimize
min_res = minimize(min_f, 0)  # The starting point doesn't really matter here

f_x = min_res.x[0]
f_y = f(min_res.x[0])

p = [p_x, p_y]
q = [f_x, f_y]

# Show result
print("Closest point is x=", min_res.x[0], " y=", f(min_res.x[0]))

print("dist is: ", dist(p,q))
