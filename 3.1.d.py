import numpy as np
import matplotlib.pyplot as plt

# --- displacement star functions (u = eps * u_star) ---
def u_star(X1, X2):
    u1 = 0.1*X1 + 0.8*X2*np.sin(4*X1) - 0.2*X1*np.sin(5*X2)
    u2 = 0.2*(np.cos(4*X1) - 1.0)
    u3 = 0.0
    return u1, u2, u3

# --- construct undeformed domain points (on faces of the box) ---
def build_faces():
    n1, n2 = 20, 12
    x1 = np.linspace(0,1,n1)
    x2 = np.linspace(-0.2,0.2,n2)
    x3 = np.array([-0.2,0.2])
    faces = []

    # X3 = -0.2 and X3 = 0.2
    X1g, X2g = np.meshgrid(x1, x2, indexing='xy')
    for z in x3:
        Xpts = np.vstack((X1g.ravel(), X2g.ravel(), z*np.ones(X1g.size))).T
        faces.append(Xpts)

    # X2 = -0.2 and X2 = 0.2
    X1g, X3g = np.meshgrid(x1, x3, indexing='xy')
    for y in [-0.2, 0.2]:
        Xpts = np.vstack((X1g.ravel(), y*np.ones(X1g.size), X3g.ravel())).T
        faces.append(Xpts)

    # X1 = 0 and X1 = 1
    X2g, X3g = np.meshgrid(x2, x3, indexing='xy')
    for x in [0.0, 1.0]:
        Xpts = np.vstack((x*np.ones(X2g.size), X2g.ravel(), X3g.ravel())).T
        faces.append(Xpts)

    return np.vstack(faces)

# --- deformation map ---
def deform_points(X, eps):
    u1, u2, u3 = u_star(X[:,0], X[:,1])
    x = np.vstack((X[:,0] + eps*u1, X[:,1] + eps*u2, X[:,2] + eps*u3)).T
    return x

# --- main plotting function ---
def plot_deformation(eps=0.25):
    X_all = build_faces()
    x_all = deform_points(X_all, eps)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    # scatter reference vs deformed surfaces
    ax.scatter(X_all[:,0], X_all[:,1], X_all[:,2], s=6, label='Undeformed (reference)')
    ax.scatter(x_all[:,0], x_all[:,1], x_all[:,2], s=6, label=f'Deformed (eps={eps})')

    # line ℓ1 (X2=0.2, X3=0)
    t = np.linspace(0,1,300)
    X_l1 = np.vstack((t, 0.2*np.ones_like(t), np.zeros_like(t))).T
    x_l1 = deform_points(X_l1, eps)
    ax.plot(X_l1[:,0], X_l1[:,1], X_l1[:,2], 'b-', linewidth=2, label='ℓ1 undeformed')
    ax.plot(x_l1[:,0], x_l1[:,1], x_l1[:,2], 'r-', linewidth=2, label='ℓ1 deformed')

    # line ℓ2 (X2=0.4X1-0.2, X3=0)
    X_l2 = np.vstack((t, 0.4*t - 0.2, np.zeros_like(t))).T
    x_l2 = deform_points(X_l2, eps)
    ax.plot(X_l2[:,0], X_l2[:,1], X_l2[:,2], 'g-', linewidth=2, label='ℓ2 undeformed')
    ax.plot(x_l2[:,0], x_l2[:,1], x_l2[:,2], 'm-', linewidth=2, label='ℓ2 deformed')

    # labels and legend
    ax.set_xlabel('X1 (or x)')
    ax.set_ylabel('X2 (or y)')
    ax.set_zlabel('X3 (or z)')
    ax.set_title(f'Undeformed and deformed shapes of Ω (eps={eps})')
    ax.legend(loc='best')

    plt.show()

# --- call the function ---
plot_deformation(eps=0.25)
