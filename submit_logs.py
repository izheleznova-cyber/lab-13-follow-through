#!/usr/bin/env python3
"""
📤 Submit Logs - Автоматическая отправка логов в Git репозиторий
Запустите после завершения игры для отправки логов преподавателю
"""

import os
import subprocess
import glob
import sys
from datetime import datetime

def print_header():
    print("\n" + "="*60)
    print("📤 ОТРАВКА ЛОГОВ В GITHUB РЕПОЗИТОРИЙ")
    print("="*60)

def find_logs():
    """Находит все лог-файлы в текущей директории"""
    log_files = glob.glob("log_*.json")
    return log_files

def check_git_status():
    """Проверяет, настроен ли Git"""
    try:
        result = subprocess.run(["git", "config", "user.name"], 
                              capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Git не настроен!")
        print("💡 Выполните команды:")
        print("   git config --global user.name \"Ваше Имя\"")
        print("   git config --global user.email \"ваш@email.com\"")
        return False

def submit_logs(log_files):
    """Отправляет логи в Git репозиторий"""
    
    print(f"\n📁 Найдено логов: {len(log_files)}")
    for f in log_files:
        size = os.path.getsize(f)
        print(f"  ✅ {f} ({size} байт)")
    
    # Проверяем Git
    if not check_git_status():
        return False
    
    # Добавляем файлы в Git
    print("\n🔄 Добавление файлов в Git...")
    try:
        subprocess.run(["git", "add","-f"] + log_files, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при добавлении файлов: {e}")
        return False
    
    # Делаем коммит
    print("💾 Создание коммита...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_message = f"Add game logs - {timestamp}"
    
    try:
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Возможно, файлы уже закоммичены: {e}")
    
    # Отправляем в GitHub
    print("📤 Отправка в GitHub...")
    print("💡 Если спросит пароль — используйте Personal Access Token")
    
    try:
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("\n" + "="*60)
        print("✅ ЛОГИ УСПЕШНО ОТПРАВЛЕНЫ В РЕПОЗИТОРИЙ!")
        print("="*60)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка при отправке: {e}")
        print("\n💡 Попробуйте вручную:")
        print("   git push origin main")
        return False

def main():
    print_header()
    
    # Ищем логи
    log_files = find_logs()
    
    if not log_files:
        print("\n❌ Лог-файлы не найдены!")
        print("💡 Запустите игру сначала: python game.py")
        sys.exit(1)
    
    # Отправляем логи
    success = submit_logs(log_files)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
