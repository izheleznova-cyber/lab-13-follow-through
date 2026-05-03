
#!/bin/bash
echo "🐳 Проверка Docker-окружения..."
if ! docker compose version &> /dev/null; then
  echo "❌ Docker Compose не найден. Установите Docker Desktop или docker-compose-plugin"
  exit 1
fi

echo "🔨 Сборка образа..."
docker compose build --quiet || { echo "❌ Ошибка сборки"; exit 1; }

echo "📦 Проверка зависимостей..."
docker compose run --rm analyzer python3 -c "import pandas, matplotlib; print('✅ Библиотеки OK')" || exit 1

echo " Всё готово! Запускайте: docker compose up"
