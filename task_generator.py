import json
import hashlib
import random
import os

def generate_student_tasks(name, level=1):
    """
    Генерирует персональные задания для студента
    
    Args:
        name: имя студента
        level: максимальный уровень заданий (1-4)
    
    Returns:
        dict с заданиями
    """
    # Хеш имени для детерминированного выбора
    name_hash = hashlib.md5(name.encode()).hexdigest()
    seed = int(name_hash[:8], 16) % 10000
    random.seed(seed)
    
    # Загружаем базу заданий
    with open('tasks_database.json', 'r', encoding='utf-8') as f:
        tasks_db = json.load(f)
    
    # Выбираем задания для каждого уровня
    student_tasks = {
        'name': name,
        'seed': seed,
        'levels': {}
    }
    
    for lvl in range(1, level + 1):
        level_key = f'level_{lvl}'
        if level_key not in tasks_db:
            continue
        
        # Выбираем 3 случайных задания из уровня
        available_tasks = tasks_db[level_key]
        selected = random.sample(available_tasks, min(3, len(available_tasks)))
        
        student_tasks['levels'][level_key] = {
            'tasks': selected,
            'completed': [False] * len(selected),
            'max_points': sum(t['points'] for t in selected)
        }
    
    # Сохраняем персональный файл
    filename = f'student_tasks_{name}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(student_tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Задания сгенерированы для {name}")
    print(f" Seed: {seed}")
    print(f"📊 Всего баллов: {sum(l['max_points'] for l in student_tasks['levels'].values())}")
    
    return student_tasks

def display_tasks(name):
    """Красиво отображает задания студента"""
    filename = f'student_tasks_{name}.json'
    
    if not os.path.exists(filename):
        print(f"❌ Файл заданий не найден! Сначала сгенерируйте.")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print(f"📚 ЗАДАНИЯ ДЛЯ: {data['name'].upper()}")
    print(f"🎲 Seed: {data['seed']}")
    print("="*60)
    
    total_points = 0
    
    for level_key, level_data in data['levels'].items():
        level_num = level_key.replace('level_', '')
        stars = '⭐' * int(level_num)
        
        print(f"\n{stars} УРОВЕНЬ {level_num} (макс: {level_data['max_points']} баллов)")
        print("-" * 60)
        
        for i, task in enumerate(level_data['tasks']):
            status = "✅" if level_data['completed'][i] else "⬜"
            print(f"{status} [{task['id']}] {task['title']}")
            print(f"    {task['description']}")
            print(f"    💡 Подсказка: {task['hint']}")
            print(f"    🏆 Баллы: {task['points']}")
            print()
        
        total_points += level_data['max_points']
    
    print("="*60)
    print(f"📊 ИТОГО МАКСИМУМ: {total_points} баллов")
    print("="*60)

if __name__ == "__main__":
    # Генерация при первом запуске
    name = input("👤 Введите ваше имя: ").strip().lower()
    
    if not name:
        name = "anonymous"
    
    # Спрашиваем уровень (можно автоматизировать)
    print("\n📈 Выберите уровень сложности:")
    print("1 - Только базовые (⭐)")
    print("2 - Базовые + средние (⭐⭐)")
    print("3 - Все уровни (⭐⭐⭐)")
    print("4 - Полный курс (⭐⭐⭐⭐)")
    
    level_choice = input("\nВаш выбор (1-4): ").strip()
    level = int(level_choice) if level_choice.isdigit() else 1
    
    # Генерируем задания
    generate_student_tasks(name, level)
    
    # Показываем
    display_tasks(name)
    
    print("\n💾 Файл сохранён: student_tasks_{name}.json")
    print("📝 Покажите этот файл преподавателю для проверки!")
