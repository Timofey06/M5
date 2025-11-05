import numpy as np

m = 1.0
R = 1.0
I = (5/4) * m * R**2
g = 9.81
N_OSC = 10
MAX_TIME_FACTOR = 15

omega0_anal = np.sqrt(m * g * R / I)
T0_anal = 2 * np.pi / omega0_anal
MAX_TIME = MAX_TIME_FACTOR * T0_anal

def angular_acceleration(theta, omega, k=0.0):
    torque = -m * g * R * np.sin(theta) - k * omega
    return torque / I

def simulate_free_oscillations(theta0, k=0.0, dt_f=60000):
    dt = T0_anal / dt_f

    t_vals = [0.0]
    theta_vals = [theta0]
    omega_vals = [0.0]

    peaks = 0
    last_was_peak = False

    while peaks < N_OSC:
        t = t_vals[-1]
        if t >= MAX_TIME:
            break

        theta = theta_vals[-1]
        omega = omega_vals[-1]

        alpha = angular_acceleration(theta, omega, k)
        omega_new = omega + dt * alpha
        theta_new = theta + dt * omega_new
        t_new = t + dt

        t_vals.append(t_new)
        theta_vals.append(theta_new)
        omega_vals.append(omega_new)

        if len(theta_vals) >= 3:
            if theta_vals[-2] > theta_vals[-3] and theta_vals[-2] > theta_vals[-1]:
                if not last_was_peak:
                    peaks += 1
                    last_was_peak = True
            else:
                last_was_peak = False

    return np.array(t_vals), np.array(theta_vals), np.array(omega_vals)

def total_energy(theta, omega):
    potential = m * g * R * (1 - np.cos(theta))
    kinetic = 0.5 * I * omega**2
    return kinetic + potential

def estimate_period(t, theta):
    peak_times = []
    for i in range(1, len(theta) - 1):
        if theta[i] > theta[i-1] and theta[i] > theta[i+1]:
            peak_times.append(t[i])
    if len(peak_times) < 2:
        return np.nan
    return np.mean(np.diff(peak_times))
