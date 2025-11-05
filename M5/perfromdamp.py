import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from calclib import (
    simulate_free_oscillations,
    estimate_period,
    T0_anal,
    omega0_anal,
    I
)

def load_initial_angle(filename='M5/params.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    theta0_deg = float(root.find('initial_angle_deg').text)
    if theta0_deg < 0 or theta0_deg > 180:
        raise ValueError("Invalid initial_angle_deg, it must be from 0 to 180")
    return np.radians(theta0_deg)

def theoretical_damped_period(k):
    gamma = k / (2 * I)
    if gamma >= omega0_anal:
        return np.nan
    omega_d = np.sqrt(omega0_anal**2 - gamma**2)
    return 2 * np.pi / omega_d

def main():
    theta0 = load_initial_angle()
    theta0_deg = np.degrees(theta0)
    print(f"Начальный угол для всех запусков: {theta0_deg:.1f}°")

    k_max = 0.9 * (2 * I * omega0_anal)
    k_values = np.linspace(0.0, k_max, 20)

    periods_num = []
    periods_th = []

    print("Вычисление зависимости периода от коэффициента трения...")
    for k in k_values:
        print(f"  k = {k:.4f} ...", end="", flush=True)
        try:
            t, th, _ = simulate_free_oscillations(theta0, k=k)
            T_num = estimate_period(t, th)
            T_th = theoretical_damped_period(k)
            periods_num.append(T_num)
            periods_th.append(T_th)
            status = f"T = {T_num:.5f} с" if not np.isnan(T_num) else "нет колебаний"
            print(f" {status}")
        except Exception as e:
            print(f" ошибка: {e}")
            periods_num.append(np.nan)
            periods_th.append(np.nan)

    periods_num = np.array(periods_num)
    periods_th = np.array(periods_th)

    plt.figure(figsize=(8, 6))
    plt.plot(k_values, periods_num, 'ro-', label='Численно', markersize=5)
    plt.plot(k_values, periods_th, 'b--', label='Теория', linewidth=2)
    plt.axhline(T0_anal, color='k', linestyle=':', label=f'Без трения T₀ = {T0_anal:.4f} с')

    plt.xlabel('Коэффициент трения k [Н·м·с]')
    plt.ylabel('Период T [с]')
    plt.title(f'Зависимость периода от трения (θ₀ = {theta0_deg:.1f}°)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
