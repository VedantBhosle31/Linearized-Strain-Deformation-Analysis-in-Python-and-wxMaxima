import numpy as np
import matplotlib.pyplot as plt

# --- displacement star functions (u = eps * u_star) ---
def u_star(X1, X2):
    u1 = 0.1*X1 + 0.8*X2*np.sin(4*X1) - 0.2*X1*np.sin(5*X2)
    u2 = 0.2*(np.cos(4*X1) - 1.0)
    u3 = 0.0
    return u1, u2, u3

# --- derivatives a_ij = d(u_i*)/dX_j ---
def a_components(X1, X2):
    a11 = 0.1 + 3.2*X2*np.cos(4*X1) - 0.2*np.sin(5*X2)
    a12 = 0.8*np.sin(4*X1) - 1.0*X1*np.cos(5*X2)
    a21 = -0.8*np.sin(4*X1)
    a22 = 0.0
    return a11, a12, a21, a22

# --- functions to compute deformed line coordinates ---
def deformed_line_points_line1(eps, n=2000):
    t = np.linspace(0,1,n)
    X1 = t
    X2 = 0.2*np.ones_like(t)
    X3 = np.zeros_like(t)
    u1, u2, u3 = u_star(X1, X2)
    x = np.vstack((X1 + eps*u1, X2 + eps*u2, X3 + eps*u3)).T
    return x

def deformed_line_points_line2(eps, n=2000):
    t = np.linspace(0,1,n)
    X1 = t
    X2 = 0.4*X1 - 0.2
    X3 = np.zeros_like(t)
    u1, u2, u3 = u_star(X1, X2)
    x = np.vstack((X1 + eps*u1, X2 + eps*u2, X3 + eps*u3)).T
    return x

# --- arc length utility ---
def arc_length(points):
    diffs = np.diff(points, axis=0)
    seg_lengths = np.linalg.norm(diffs, axis=1)
    return seg_lengths.sum()

# --- analytic (linearized) predictions ---
def analytic_length_line1(eps):
    return 1.0 + eps * (0.1 + 0.16*np.sin(4.0) - 0.2*np.sin(1.0))

def analytic_length_line2(eps):
    L0 = np.sqrt(1.0 + 0.4**2)
    t = np.linspace(0,1,2000)
    X1 = t
    X2 = 0.4*X1 - 0.2
    a11, a12, a21, a22 = a_components(X1, X2)
    integrand = a11 - 0.4*X1*np.cos(5*X2)
    integral = np.trapz(integrand, X1)
    return L0 + eps * integral / L0

# --- compute errors ---
eps_values = [0.05, 0.1, 0.2, 0.4, 0.8]
errors_L1 = []
errors_L2 = []

for eps in eps_values:
    L1_num = arc_length(deformed_line_points_line1(eps))
    L2_num = arc_length(deformed_line_points_line2(eps))
    L1_ana = analytic_length_line1(eps)
    L2_ana = analytic_length_line2(eps)
    errors_L1.append(100.0*(L1_num - L1_ana)/L1_num)
    errors_L2.append(100.0*(L2_num - L2_ana)/L2_num)

# --- plot ---
plt.figure(figsize=(8,6))
plt.plot(eps_values, errors_L1, 'o-', label="ℓ₁ relative error")
plt.plot(eps_values, errors_L2, 's-', label="ℓ₂ relative error")
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("ε (strain scaling)")
plt.ylabel("Relative error (%)")
plt.title("Relative error of linearized analytic length vs numerical length")
plt.legend()
plt.grid(True)
plt.show()
