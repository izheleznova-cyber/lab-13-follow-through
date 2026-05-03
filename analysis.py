#!/usr/bin/env python3
"""
Lab 13: Follow Through — Analysis Module
(На основе рабочего кода студента, адаптировано для Docker)
"""

import os
import json
from pathlib import Path

# 🔧 Обязательно для Docker (нет графического интерфейса)
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# CONFIG
# ============================================================================
WORKSPACE = Path('/app/workspace')
OUTPUT_DIR = Path('/app/output')

# Нормализуем имя: убираем пробелы, приводим к нижнему регистру
RAW_NAME = os.getenv('STUDENT_ID', 'unknown').strip()
STUDENT_ID = RAW_NAME.lower()

# ============================================================================
# MANIFEST (цифровая подпись Docker)
# ============================================================================
def create_manifest():
    """Создаёт execution_manifest.json для верификации"""
    is_docker = os.path.exists('/.dockerenv')
    
    manifest = {
        "timestamp": pd.Timestamp.utcnow().isoformat(),
        "hostname": os.uname().nodename,
        "container": f"lab-13-{STUDENT_ID}",
        "env": "docker" if is_docker else "local",
        "student_id": STUDENT_ID,
        "lab_number": os.getenv('LAB_NUMBER', '13')
    }
    
    # 🔧 Сохраняем в корень репозитория (WORKSPACE), а не в output/
    manifest_path = WORKSPACE / 'execution_manifest.json'
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Manifest: {manifest_path.name}")

# ============================================================================
# ПОИСК ФАЙЛА (кейс-инсенситивный)
# ============================================================================
def find_log_file():
    """Ищет log_<name>.json игнорируя регистр имени"""
    if not WORKSPACE.exists():
        return None
    
    for f in WORKSPACE.glob('log_*.json'):
        # Извлекаем имя из имени файла: log_Vitaliy.json -> vitaliy
        fname = f.stem  # 'log_Vitaliy'
        if fname.startswith('log_'):
            file_name = fname[4:].lower()  # 'vitaliy'
            if file_name == STUDENT_ID:
                return f
    return None

# ============================================================================
# MAIN LOGIC (ваш оригинальный код + адаптация)
# ============================================================================
def main():
    print(f"🚀 Analysis for '{RAW_NAME}' (normalized: '{STUDENT_ID}')")
    
    # 1. Создаём манифест
    create_manifest()
    
    # 2. Ищем лог-файл
    log_path = find_log_file()
    if not log_path:
        print(f"❌ Log file not found for '{STUDENT_ID}'")
        print(f"   Available files:")
        for f in WORKSPACE.glob('*.json'):
            print(f"     - {f.name}")
        return
    
    print(f"✅ Found: {log_path.name}")
    
    # 3. Загружаем данные (ВАШ ОРИГИНАЛЬНЫЙ КОД)
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return
    
    # Проверяем структуру
    if "log" not in data:
        print(f"❌ Key 'log' not found in {log_path.name}")
        print(f"   Available keys: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")
        return
    
    # 4. Подготовка данных (ВАШ КОД)
    df = pd.DataFrame(data["log"])
    
    if df.empty:
        print("⚠️ Log is empty")
        return
    
    df_move = df[df["event"] == "move"]
    collisions = df[df["event"] == "collision"]
    
    # 5. Аналитика (вывод в консоль)
    print(f"📊 Total events: {len(df)}")
    print(f"🚶 Moves: {len(df_move)}")
    print(f"💥 Collisions: {len(collisions)}")
    
    if not df_move.empty:
        duration = df["time"].max() - df["time"].min()
        print(f"⏱ Session duration: {duration:.2f} sec")
    
    # 6. Визуализация (ВАШ КОД + сохранение в output/)
    if df_move.empty:
        print("⚠️ No move events to plot")
        return
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_move["x"], df_move["y"], label="trajectory", linewidth=1.5)
    
    if not collisions.empty:
        plt.scatter(collisions["x"], collisions["y"], color="red", label="collisions", s=50, zorder=5)
    
    # Старт и финиш
    if not df_move.empty:
        plt.scatter(df_move.iloc[0]["x"], df_move.iloc[0]["y"], color="green", label="start", s=100, zorder=5, edgecolors='white')
        plt.scatter(df_move.iloc[-1]["x"], df_move.iloc[-1]["y"], color="blue", label="end", s=100, zorder=5, edgecolors='white')
    
    # Оформление (ВАШ КОД)
    plt.gca().invert_yaxis()  # Важно для игры!
    plt.legend()
    plt.title(f"Trajectory: {RAW_NAME}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(alpha=0.4)
    plt.tight_layout()
    
    # 7. Сохранение в output/ (адаптация для Docker)
    output_path = WORKSPACE / f"traject_{STUDENT_ID}.png"
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Graph saved: {output_path.name} (in repo root)")
    print("✅ Analysis complete. Files are in your repository root.")

if __name__ == "__main__":
    main()
