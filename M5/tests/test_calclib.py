import numpy as np
import pytest

from M5.calclib import (
    angular_acceleration,
    simulate_free_oscillations,
    total_energy,
    estimate_period,
    T0_anal,
    I,
    omega0_anal
)
from M5.perfromdamp import theoretical_damped_period
from M5.perfromampl import theoretical_period


# Проверяем, что функция не придумывает движение там, где его нет
def test_angular_acceleration_zero_state():
    # При отсутствии угла и скорости, ускорения быть не должно
    # (Возвращаемое значение очень близко к 0)
    a = angular_acceleration(theta=0.0, omega=0.0, k=0.0)
    assert abs(a) < 1e-12

# Здесь просто проверяем знак ускорения (что оно отрицательное)
def test_angular_acceleration_sign_for_small_angle():
    # Для небольшого положительного угла (theta > 0) при нулевой скорости
    # ускорение должно быть отрицательным (т.е. система возвращается к нулю)
    a = angular_acceleration(theta=0.1, omega=0.0, k=0.0)
    assert a < 0

# Проверяем, что симуляция вообще работает
def test_simulation_shapes_and_monotonic_time():
    # Функция должна вернуть три массива одинаковой длины: t, theta, omega
    # Длина массивов должна быть больше 5 (симуляция действительно выполнялась)
    # Массив времени t возрастает строго и монотонно (t[i+1] > t[i])
    t, theta, omega = simulate_free_oscillations(theta0=0.2, k=0.0)

    assert len(t) == len(theta) == len(omega)
    assert len(t) > 5
    assert np.all(np.diff(t) > 0)

# Если стартовать с нулевого угла и скорости, маятник не должен начать качаться сам
def test_simulation_zero_initial_angle():
    # Для theta0 = 0 (маятник не отклонён) симуляция должна выдавать нулевые углы и скорости.
    # estimate_period должен вернуть np.nan (нет видимых пиков/колебаний).

    t, theta, omega = simulate_free_oscillations(theta0=0.0, k=0.0)
    assert np.allclose(theta, 0.0, atol=1e-6)
    assert np.allclose(omega, 0.0, atol=1e-6)
    assert np.isnan(estimate_period(t, theta))

# В покое энергия должна быть нулевой
def test_energy_zero_state():
    # При theta = 0 и omega = 0 энергия равна нулю.
    #Проверяет правильную базовую формулу вычисления энергии.

    assert total_energy(0.0, 0.0) == pytest.approx(0.0, abs=1e-12)

# Энергия не может быть отрицательной
def test_energy_non_negative():
    # Для набора значений энергия не отрицательна.
    # Энергия физически не может быть отрицательной; ловим ошибки в формулах.

    th = np.linspace(-1, 1, 20)
    w = np.linspace(-1, 1, 20)
    E = total_energy(th, w)
    assert np.all(E >= 0)

def test_estimate_period_no_peaks():
    # Если сигнал не содержит пиков (например ноль), estimate_period должен вернуть np.nan.
    # Проверка корректной обработки случая, когда найти период невозможно.

    t = np.linspace(0, 1, 1000)
    theta = np.zeros_like(t)
    assert np.isnan(estimate_period(t, theta))

# Считаем энергию в начале и в конце — они должны почти совпадать.
def test_energy_conservation_no_damping():
    # При отсутствии трения (k = 0) суммарная энергия должна сохраняться
    # по крайней мере на небольшом отрезке времени (относительная вариация < 1%).

    t, theta, omega = simulate_free_oscillations(theta0=0.2, k=0.0)
    E = total_energy(theta, omega)
    variation = (np.max(E) - np.min(E)) / np.mean(E)
    assert variation < 0.01

# Проверка, что модель ведёт себя реалистично
def test_small_angle_period_matches_theory():
    # Для малого начального угла численный период должен быть
    # близок к теоретическому T0_anal.

    t, theta, omega = simulate_free_oscillations(theta0=np.radians(5), k=0.0)
    T_est = estimate_period(t, theta)
    assert T_est == pytest.approx(T0_anal, rel=0.02)


# Если у маятника есть трение — энергия должна уменьшаться
def test_energy_decreases_with_damping():
    # При наличии трения (k > 0) общая энергия на конце симуляции должна быть
    # меньше, чем в начале
    # Проверка, что энергия убывает

    t, theta, omega = simulate_free_oscillations(theta0=0.3, k=0.5)
    E = total_energy(theta, omega)
    assert E[-1] < E[0]

# Модель должна правильно распознавать случай без колебаний
def test_overdamped_no_oscillations():
    # Проверяем ситуацию, когда трение очень большое.
    # Если трение огромное, маятник не будет качаться
    # Он просто начнёт сразу медленно возвращаться к вертикальному положению
    # без каких-либо колебаний.
    k = 5 * I * omega0_anal
    t, theta, omega = simulate_free_oscillations(theta0=0.5, k=k)
    assert np.isnan(estimate_period(t, theta))

def test_moment_of_inertia_positive():
    # Момент инерции I положителен (физическая корректность).
    # Защищает от неправильной инициализации констант в calclib.py.
    assert I > 0

# Проверяем, что при небольшом трении маятник колеблется почти как обычный,
# и его период, рассчитанный программой, почти совпадает с теоретическим.
def test_period_with_small_damping_matches_analytic():
    theta0 = np.radians(10)
    k = 0.05  # небольшое трение

    t, theta, omega = simulate_free_oscillations(theta0=theta0, k=k)
    T_num = estimate_period(t, theta)

    T_exact = theoretical_damped_period(k)

    assert T_num == pytest.approx(T_exact, rel=0.05)

#Проверяем, что при большой амплитуде (например 50°)
# численный период совпадает с аналитическим, рассчитанным по формуле
def test_period_large_angle_matches_analytic():
    theta0 = np.radians(50)

    t, theta, omega = simulate_free_oscillations(theta0=theta0, k=0.0)
    T_num = estimate_period(t, theta)

    T_exact = theoretical_period(theta0)

    assert T_num == pytest.approx(T_exact, rel=0.05)