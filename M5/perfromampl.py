import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk
from calclib import (
    simulate_free_oscillations,
    estimate_period,
    T0_anal
)

def theoretical_period(theta0):
    k_sq = np.sin(theta0 / 2.0)**2
    return T0_anal * (2.0 / np.pi) * ellipk(k_sq)

def main():
    angles_deg = np.linspace(5, 160, 16)
    angles_rad = np.radians(angles_deg)

    periods_num = []
    periods_th = []

    print("Вычисление T(θ₀)...")
    for theta0 in angles_rad:
        print(f"  θ₀ = {np.degrees(theta0):5.1f}° ...", end="", flush=True)
        t, th, _ = simulate_free_oscillations(theta0, k=0.0)
        T_num = estimate_period(t, th)
        T_th = theoretical_period(theta0)
        periods_num.append(T_num)
        periods_th.append(T_th)
        print(f" T = {T_num:.5f} с")


    plt.figure(figsize=(8, 6))
    plt.plot(angles_deg, periods_num, 'ro-', label='Численно', markersize=5)
    plt.plot(angles_deg, periods_th, 'b--', label='Теория', linewidth=2)
    plt.axhline(T0_anal, color='k', linestyle=':', label=f'Теория малые колебания T₀ = {T0_anal:.4f} с')
    plt.xlabel('Начальный угол θ₀ [градусы]')
    plt.ylabel('Период T [с]')
    plt.title('Зависимость периода от амплитуды')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
