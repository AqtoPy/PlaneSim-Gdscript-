# Ссылки на элементы интерфейса
@onready var altitude_label = $AltitudeLabel
@onready var speed_label = $SpeedLabel
@onready var fuel_label = $FuelLabel
@onready var engine_power_label = $EnginePowerLabel
@onready var stress_label = $StressLabel
@onready var weather_label = $WeatherLabel
@onready var wind_label = $WindLabel
@onready var passengers_label = $PassengersLabel
@onready var passengers_health_label = $PassengersHealthLabel
@onready var passengers_trust_label = $PassengersTrustLabel

# Параметры игры
var altitude: int = 10000
var speed: int = 800
var fuel: int = 100
var engine_power: int = 100
var stress: int = 0
var weather: String = "clear"
var wind_speed: int = 5
var wind_direction: int = 0
var passengers: int = 100
var passengers_health: int = 100
var passengers_trust: int = 100
var is_flying: bool = true
var money: int = 200

func _ready():
    # Инициализация игры
    update_ui()
    start_flight()

func start_flight():
    # Запуск основного цикла игры
    while is_flying and passengers > 0:
        await get_tree().create_timer(1.0).timeout  # Задержка 1 секунда
        flight_step()
        if randf() < 0.3:  # 30% шанс события
            random_event()
        if randf() < 0.01:  # 1% шанс аварии
            crash()
        update_ui()

    if passengers <= 0:
        status_label.text = "💀 Все пассажиры погибли. Игра окончена."
    elif stress >= 100:
        status_label.text = "😫 Пассажиры в панике. Игра окончена."
    elif fuel <= 0:
        status_label.text = "⛽ Топливо закончилось. Игра окончена."

func flight_step():
    # Обновление состояния игры
    altitude += (engine_power - 50) / 10  # Высота зависит от мощности двигателя
    speed = engine_power * 2  # Скорость зависит от мощности двигателя
    fuel -= max(1, 5 - engine_power / 20)  # Расход топлива
    stress += randi_range(1, 3)
    passengers_health -= randi_range(0, 2)
    passengers_trust -= randi_range(0, 1)

    if fuel < 0:
        fuel = 0
    if altitude < 0:
        altitude = 0
    if stress > 100:
        stress = 100
    if passengers_health < 0:
        passengers_health = 0
    if passengers_trust < 0:
        passengers_trust = 0

    # Влияние на пассажиров
    if stress > 50:
        passengers_health -= randi_range(1, 3)
    if passengers_health < 50:
        passengers -= randi_range(1, 5)
    if passengers_trust < 30:
        stress += randi_range(5, 10)

    # Влияние погоды и ветра
    if weather == "storm":
        speed -= 10
        stress += 10
        altitude -= randi_range(1, 5)
        passengers_health -= randi_range(1, 3)
    elif weather == "fog":
        speed -= 5
        stress += 5
    if wind_speed > 10:
        speed -= wind_speed / 2
        altitude -= wind_speed / 5

func random_event():
    # Случайное событие
    var events = [
        engine_failure, turbulence, bird_strike, fuel_leak, weather_change,
        medical_emergency, passenger_panic, hijacking
    ]
    var event = events[randi() % events.size()]
    event()

func crash():
    # Редкая авария
    status_label.text = "💥 Произошла авария!"
    altitude -= randi_range(100, 200)
    stress += randi_range(20, 40)
    passengers -= randi_range(10, 20)
    if altitude < 0:
        altitude = 0
    if stress > 100:
        stress = 100

func engine_failure():
    status_label.text = "⚠️ Отказ двигателя!"
    var choice = show_choice_dialog("Что будем делать?", ["Попытаться починить (50$)", "Продолжить полёт"])
    if choice == 0:
        if money >= 50:
            money -= 50
            if randf() < 0.7:
                status_label.text = "✅ Двигатель починен! Продолжаем полёт."
            else:
                status_label.text = "❌ Ремонт не удался. Мощность двигателя снижена."
                engine_power -= randi_range(10, 20)
        else:
            status_label.text = "❌ Недостаточно денег для ремонта."
    else:
        status_label.text = "❌ Игнорируем проблему. Двигатель теряет мощность!"
        engine_power -= randi_range(15, 25)

func turbulence():
    status_label.text = "🌪️ Турбулентность!"
    var choice = show_choice_dialog("Что будем делать?", ["Снизить скорость", "Продолжить полёт"])
    if choice == 0:
        status_label.text = "✅ Скорость снижена. Турбулентность уменьшена."
        speed -= 20
    else:
        status_label.text = "❌ Продолжаем полёт. Стресс увеличивается."
        stress += 10

func bird_strike():
    status_label.text = "🐦 Столкновение с птицей!"
    var choice = show_choice_dialog("Что будем делать?", ["Проверить двигатель (30$)", "Продолжить полёт"])
    if choice == 0:
        if money >= 30:
            money -= 30
            if randf() < 0.5:
                status_label.text = "✅ Двигатель в порядке. Продолжаем полёт."
            else:
                status_label.text = "❌ Повреждение двигателя. Мощность снижена."
                engine_power -= randi_range(10, 20)
        else:
            status_label.text = "❌ Недостаточно денег для проверки."
    else:
        status_label.text = "❌ Игнорируем проблему. Двигатель теряет мощность!"
        engine_power -= randi_range(15, 25)

func fuel_leak():
    status_label.text = "⛽ Утечка топлива!"
    var choice = show_choice_dialog("Что будем делать?", ["Попытаться устранить утечку (20$)", "Продолжить полёт"])
    if choice == 0:
        if money >= 20:
            money -= 20
            if randf() < 0.5:
                status_label.text = "✅ Утечка устранена! Продолжаем полёт."
            else:
                status_label.text = "❌ Утечка продолжается. Топливо быстро уходит."
                fuel -= randi_range(20, 30)
        else:
            status_label.text = "❌ Недостаточно денег для устранения утечки."
    else:
        status_label.text = "❌ Игнорируем утечку. Топливо заканчивается!"
        fuel -= randi_range(30, 40)

func weather_change():
    var new_weather = ["clear", "storm", "fog"][randi() % 3]
    weather = new_weather
    status_label.text = f"🌦️ Погода изменилась: {new_weather}."

func medical_emergency():
    status_label.text = "🚑 Медицинская помощь требуется!"
    var choice = show_choice_dialog("Что будем делать?", ["Оказать помощь (30$)", "Игнорировать"])
    if choice == 0:
        if money >= 30:
            money -= 30
            passengers_health += randi_range(10, 20)
            status_label.text = "✅ Пассажирам стало лучше."
        else:
            status_label.text = "❌ Недостаточно денег для помощи."
    else:
        status_label.text = "❌ Игнорируем проблему. Пассажиры теряют здоровье!"
        passengers_health -= randi_range(10, 20)

func passenger_panic():
    status_label.text = "😱 Паника среди пассажиров!"
    var choice = show_choice_dialog("Что будем делать?", ["Успокоить пассажиров (20$)", "Игнорировать"])
    if choice == 0:
        if money >= 20:
            money -= 20
            stress -= randi_range(10, 20)
            passengers_trust += randi_range(5, 10)
            status_label.text = "✅ Пассажиры успокоились."
        else:
            status_label.text = "❌ Недостаточно денег для успокоения."
    else:
        status_label.text = "❌ Игнорируем панику. Стресс увеличивается!"
        stress += randi_range(10, 20)

func hijacking():
    status_label.text = "🔫 Угроза захвата самолёта!"
    var choice = show_choice_dialog("Что будем делать?", ["Переговоры (50$)", "Сопротивляться"])
    if choice == 0:
        if money >= 50:
            money -= 50
            if randf() < 0.5:
                status_label.text = "✅ Угроза устранена. Пассажиры в безопасности."
            else:
                status_label.text = "❌ Переговоры провалились. Пассажиры в опасности!"
                passengers -= randi_range(10, 20)
        else:
            status_label.text = "❌ Недостаточно денег для переговоров."
    else:
        status_label.text = "❌ Сопротивляемся. Пассажиры в опасности!"
        passengers -= randi_range(20, 30)

func update_ui():
    # Обновление интерфейса
    altitude_label.text = f"Высота: {altitude} м"
    speed_label.text = f"Скорость: {speed} км/ч"
    fuel_label.text = f"Топливо: {fuel}%"
    engine_power_label.text = f"Мощность двигателя: {engine_power}%"
    stress_label.text = f"Стресс: {stress}%"
    weather_label.text = f"Погода: {weather}"
    wind_label.text = f"Ветер: {wind_speed} м/с, {wind_direction}°"
    passengers_label.text = f"Пассажиры: {passengers}"
    passengers_health_label.text = f"Здоровье пассажиров: {passengers_health}%"
    passengers_trust_label.text = f"Доверие пассажиров: {passengers_trust}%"

func show_choice_dialog(prompt, options):
    # Показ диалога с выбором (заглушка)
    print(prompt)
    for i in range(options.size()):
        print(f"{i + 1}. {options[i]}")
    return randi() % options.size()  # Заглушка: случайный выбор
