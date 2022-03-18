#Pizzeria API
___
##Установка и запуск

* Склонируйте данный репозиторий

```
https://github.com/duny-explorer/RTUITLAB_pizzeria.git
```

* Запустите локально Redis
* Установите требования из requirements.txt

```Bash
pip install -r requirements.txt
```

* Запустите миграции 

```Bash
python manage.py migrate
```

* Откройте командную строку из этой папки и введите

```Bash
python manage.py runserver
```
* Это запустит веб-сервер на http://127.0.0.1:8000/.

## Конечные точки API

| Путь                                 | Метод  | Параметры                                                                                                                                                                              | Описание                                            |
|--------------------------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| /health                              | GET    |                                                                                                                                                                                        | Возвращает ответ с кодом 200                        |
| /version                             | GET    |                                                                                                                                                                                        | Возвращает версию API                               |
| /pizzas/                             | GET    | page: какую вернуть страницу (если не указать, то выведет все экземпляры)<br/>size: сколько объектов на странице (по умолчанию 5)                                                      | Возвращает список всех пицц                         |
| /pizzas/                             | POST   | name: Имя пиццы<br/>info: инофрмация о ней                                                                                                                                             | Добавление новой пиццы                              |
| /pizzas/{slug_pizza}/                | GET    |                                                                                                                                                                                        | Возвращает информацию о конкретной пицце            |
| /pizzas/{slug_pizza}/                | PATCH  | name: Имя пиццы<br/>info: инофрмация о ней                                                                                                                                             | Заменить переданные поля                            |
| /pizzas/{slug_pizza}/                | DELETE |                                                                                                                                                                                        | Удаление конкретной пиццы                           |
| /pizzas/{slug_pizza}/products/       | GET    |                                                                                                                                                                                        | Вывод всех вариаций данной пиццы                    |
| /pizzas/{slug_pizzas}/products/      | POST   | size: размер пиццы (25, 30 или 35 см)<br/>weight: вес<br/>price: цена<br/>available: доступна ли для продажи                                                                           | Создание вариации для данной пиццы                  |
| /pizzas/{slug_pizzas}/products/{pk}/ | GET    |                                                                                                                                                                                        | Вывод информации о pk-той вариации данной пиццы     |
| /pizzas/{slug_pizzas}/products/{pk}/ | PATCH  | size: размер пиццы (25, 30 или 35 см)<br/>weight: вес<br/>price: цена<br/>available: доступна ли для продажи                                                                           | Заменить переданные поля                            |
| /pizzas/{slug_pizzas}/products/{pk}/ | DELETE |                                                                                                                                                                                        | Удаление pk-той вариации конкретной пиццы           |
| /orders/                             | GET    | page: какую вернуть страницу (если не указать, то выведет все экземпляры)<br/>size: сколько объектов на странице (по умолчанию 5)<br/>Есть поиск по полям last_name, first_name, email | Возвращает список всех заказов                      |
| /orders/                             | POST   | first_name: Имя заказчика<br/>last_name: фамилия<br/>email: почта<br/>address: адресс<br/> paid: заплатили ли<br/>comment: комментарии к заказу                                        | Добавление новоого заказа                           |
| /orders/{id_order}/                  | GET    |                                                                                                                                                                                        | Возвращает информацию о конкретном заказе           |
| /orders/{id_order}/                  | PATCH  | first_name: Имя заказчика<br/>last_name: фамилия<br/>email: почта<br/>address: адресс<br/> paid: заплатили ли<br/>comment: комментарии к заказу                                        | Заменить переданные поля                            |
| /orders/{id_order}/                  | DELETE |                                                                                                                                                                                        | Удаление конкретного заказ                          |
| /orders/{id_order}/items/            | GET    |                                                                                                                                                                                        | Вывод всех объектов заказа                          |
| /orders/{id_order}/items/            | POST   | quantity: кол-во<br/> pizza: название вариаации пиццы в формате "Название размер"                                                                                                      | Создание нового объекта заказа                      |
| /orders/{id_order}/items/{pk}/       | GET    |                                                                                                                                                                                        | Вывод информации о pk-того объекта заказ            |
| /orders/{id_order}/items/{pk}/       | PATCH  | quantity: кол-во<br/> pizza: название вариаации пиццы в формате "Название размер"                                                                                                      | Заменить переданные поля                            |
| /orders/{id_order}/items/{pk}/       | DELETE |                                                                                                                                                                                        | Удаление pk-того предмета заказа                    |

Автоматически сгенерированную интерактивную документацию API можно найти в разделе docs/.

Методы связанные с orders и все POST, PATCH, DELETE требуют аутентификации (username: duny, password: duny).