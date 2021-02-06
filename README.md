# online-store-redirects
Проект "Редиректы в поиске интернет-магазина" на Зимней Школе CompTech 2021

## Цель проекта
Целью проекта является разработка методов автоматического определения запросов посетителей в поиске онлайн-магазина на редирект, в результате которого мы отправляем посетителя на страницу с релевантной категорией для этого запроса.


## Как запустить
Запускать нужно файл ____?

## Папки
1. `pipeline` - папка, содержащая код для инференса(классы `Filter` и `Predictor`), а также для обучения `sklearn`-модели(`pipeline.training`) и построения отрицательных примеров(`negative_examples`)
1. `utils` - набор утилит для работы с деревом категорий, построения признаков, загрузки `pickle`-файлов
1. `notebooks` - директория для `jupyter`-тетрадок
1. также `jupyter`-тетрадки расположены в корне проекта(для удобного импорта пакетов)
1. `example.py` - файл, показывающий применение класса `Predictor`

## Результат

| Модель                               | F1     | Accuracy  | 
|--------------------------------------|--------|-----------|
|Random Forest (hand-crafted features) | 0.6165 | 0.5466    |   
|--------------------------------------|--------|-----------|                      
|Logistic Regression (char tfidf)      | 0.554  | 0.72      |        
|--------------------------------------|--------|-----------|
|Blending(0.25*RF + 0.75*LR > 0.505)   |0.6289  |0.6949     | 



## Ссылки на документацию

[Презентация] (https://docs.google.com/presentation/d/1N9Hj4b8ol7ExR1q2LkybQ0ht8RjJyS17826BlIaSNok/edit#slide=id.gbc22f9a0fe_0_40)

[ТЗ] (https://docs.google.com/document/d/1o8JIeMlEbMW4oPwd5l8Nbk2Udt3HWPNuU8VmkNJgNuc/edit)

[Общая документация проекта]  (https://docs.google.com/document/d/1903gAG3l-4KBe9XCsAV2WcRVkBxlLhliUQKAH-6I1Q4/edit#)

##

## Команда

Денис Скрипов - капитан

Костя Печененко - разработчик

Кирилл Муравьев - разработчик

Орлан Сарыглар -технический писатель

Галина Смагина- EDA, разработчик

Ольга Рудакова -аналитик

Елена Аксенова - EDA 

