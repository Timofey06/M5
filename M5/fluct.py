import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from calclib import (
    simulate_free_oscillations,
    total_energy,
    estimate_period,
    T0_anal
)

def load_params(filename='M5/params.xml'):
    tree = ET.parse(filename)
    root = tree.getroot()
    theta0_deg = float(root.find('initial_angle_deg').text)
    k = float(root.find('damping').text)
    return np.radians(theta0_deg), k

def main():
    theta0, k_input = load_params()
    theta0_deg = np.degrees(theta0)
    print(f"Начальный угол: {theta0_deg:.1f}°")
    print(f"Коэффициент трения: {k_input}")

    t_no, th_no, w_no = simulate_free_oscillations(theta0, k=0.0)
    E_no = total_energy(th_no, w_no)
    T_no = estimate_period(t_no, th_no)

    t_yes, th_yes, w_yes = simulate_free_oscillations(theta0, k=k_input)
    E_yes = total_energy(th_yes, w_yes)
    T_yes = estimate_period(t_yes, th_yes)

    print(f"\nАналитический период (теория без трения):      {T0_anal:.5f} с")
    print(f"Численный период (без трения): {T_no:.5f} с")
    if not np.isnan(T_yes):
        print(f"Численный период (с трением):  {T_yes:.5f} с")
        print(f"Изменение периода: {(T_yes - T_no)/T_no * 100:.3f}%")

    plt.figure(figsize=(14, 10))
    plt.subplot(2, 2, 1); plt.plot(t_no, th_no, 'b'); plt.title('Без трения'); plt.grid()
    plt.subplot(2, 2, 2); plt.plot(t_no, E_no, 'orange'); plt.title('Энергия (без трения)'); plt.grid()
    plt.subplot(2, 2, 3); plt.plot(t_yes, th_yes, 'g'); plt.title(f'С трением (k={k_input})'); plt.grid()
    plt.subplot(2, 2, 4); plt.plot(t_yes, E_yes, 'red'); plt.title('Энергия (с трением)'); plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
