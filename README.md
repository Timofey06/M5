# Моделирование колебаний физического маятника в поле тяжести земли
Этот проект моделирует колебания физического маятника представленного диском подвешенным за край, ось вращения параллельна плоскости диска.

## 1. Установка и использование

### Шаг 1. Клонировать проект

```bash
git clone https://github.com/username/project-name.git
```

### Шаг 2. Создать и активировать виртуальное окружение

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### Шаг 4. Настроить параметры моделирования

Параметры задаются в файле `params.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<parameters>
    <initial_angle_deg>15</initial_angle_deg>
    <damping>0.15</damping>
</parameters>
```
Где:

* `initial_angle_deg` - угол начального положения в градусах
* `damping` - коэффициент трения

### Шаг 5. Запустить симуляцию
Запустить одну из нескольких симуляций:

* `fluct` - графики колебаний и изменений энергии
* `perfromdamp` - график зависимости периода от трения
* `perfromampl` - график зависимости периода от амплитуды

# 2. Ограничения вхлдных данных

* `initial_angle_deg` От 0 до 180 градусов
* `damping` от 0 до 10






