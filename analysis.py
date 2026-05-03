import json
import pandas as pd
import matplotlib.pyplot as plt

# 1. Загрузка данных
with open("log_001.json") as f:
    data = json.load(f)

# 2. Подготовка данных
df = pd.DataFrame(data["log"])
df_move = df[df["event"] == "move"]
collisions = df[df["event"] == "collision"]

# 3. Аналитика (выводим только итоги в консоль)
print("Файл загружен успешно")
print(f"Столкновений: {len(collisions)}")

start_time = df["time"].min()
end_time = df["time"].max()
print(f"Длительность сессии: {end_time - start_time:.2f} сек.")

# 4. Визуализация
plt.figure(figsize=(10, 6))  # Задаем размер графика
plt.plot(df_move["x"], df_move["y"], label="trajectory")
plt.scatter(collisions["x"], collisions["y"], color="red", label="collisions")
plt.scatter(df.iloc[0]["x"], df.iloc[0]["y"], color="green", label="start")
plt.scatter(df.iloc[-1]["x"], df.iloc[-1]["y"], color="blue", label="end")

# Настройки оформления
plt.gca().invert_yaxis()  # Инверсия оси Y (важно для игры)
plt.legend()
plt.title("Trajectory with collisions")
plt.grid()

# 5. Сохранение и показ
# Используем имя из файла лога (или 'unknown', если его нет)
name = data.get("name", "unknown")
plt.savefig(f"traject_{name}.png", dpi=150, bbox_inches='tight')
print(f"✅ График сохранен: traject_{name}.png")

plt.show()
plt.close()  # Корректно закрывает окно после показа
