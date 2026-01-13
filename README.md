# Формирование FuzzyOWL-онтологии из текста

> Курсовая работа по дисциплине «Системы искусственного интеллекта»

## Запуск

```sh
docker build . -t fuzzyowl
```

```sh
mkdir -p data
```

```sh
echo "Система сильно влияет на надежность. Высокая производительность повышает эффективность работы." > data/input.txt
```

```sh
docker run --rm -v $(pwd)/data:/usr/src/app/data fuzzyowl -i data/input.txt
```
