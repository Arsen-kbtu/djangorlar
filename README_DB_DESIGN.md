# Импорт Django моделей в DB Designer

Этот документ содержит инструкции по переносу Django моделей вашего проекта в DB Designer.

## Файлы

- `database_schema.sql` - SQL скрипт для создания всех таблиц в DB Designer

## Структура базы данных

### Приложение Catalogs
1. **Restaurant** - рестораны, которые продают блюда
2. **Category** - категории блюд (например, "Пицца", "Напитки")
3. **Option** - дополнительные опции (например, "Большая", "Дополнительный сыр")
4. **MenuItem** - блюда, принадлежащие ресторану
5. **ItemCategory** - промежуточная таблица для связи MenuItem и Category с полем position
6. **ItemOption** - промежуточная таблица для связи MenuItem и Option (не реализована в коде, но добавлена в SQL)

### Приложение Commerces
1. **auth_user** - пользователи Django (встроенная модель)
2. **Address** - сохраненные адреса доставки пользователей
3. **PromoCode** - промо-коды для скидок
4. **Order** - заказы, размещенные пользователями
5. **OrderItem** - снимок MenuItem внутри заказа
6. **OrderItemOption** - выбранные опции для каждого элемента заказа
7. **OrderPromo** - промежуточная таблица для связи Order и PromoCode

## Инструкции по импорту в DB Designer

### Способ 1: Прямой импорт SQL
1. Откройте DB Designer (https://www.dbdesigner.net/)
2. Создайте новый проект
3. Нажмите "Import" или используйте меню File → Import
4. Выберите "SQL" как тип файла
5. Загрузите файл `database_schema.sql`
6. DB Designer автоматически создаст все таблицы с правильными связями

### Способ 2: Ручное создание (если импорт не работает)
1. Создайте таблицы в следующем порядке:
   - auth_user
   - catalogs_restaurant
   - catalogs_category
   - catalogs_option
   - commerces_promocode
   - commerces_address
   - catalogs_menuitem
   - catalogs_itemcategory
   - catalogs_itemoption
   - commerces_order
   - commerces_orderitem
   - commerces_orderitemoption
   - commerces_orderpromo

2. Для каждой таблицы:
   - Скопируйте структуру из SQL файла
   - Создайте поля согласно типам данных
   - Установите первичные ключи (id)
   - Добавьте внешние ключи согласно FOREIGN KEY constraints

### Способ 3: Использование Django для генерации SQL
Вы также можете использовать Django для генерации SQL:

```bash
# В папке project выполните:
python manage.py sqlmigrate catalogs 0001
python manage.py sqlmigrate commerces 0001
```

## Ключевые связи

### One-to-Many (1:N)
- Restaurant → MenuItem
- User → Address
- User → Order
- Address → Order
- Restaurant → Order
- Order → OrderItem
- OrderItem → OrderItemOption

### Many-to-Many (M:N) через промежуточные таблицы
- MenuItem ←→ Category (через ItemCategory)
- MenuItem ←→ Option (через ItemOption)
- Order ←→ PromoCode (через OrderPromo)

## Примечания

1. **Отсутствующая модель**: В вашем коде отсутствует модель `ItemOption`, но она упоминается в комментариях. Я добавил её в SQL скрипт.

2. **Индексы**: В SQL файле включены индексы для улучшения производительности запросов.

3. **Ограничения**: Добавлены UNIQUE constraints для предотвращения дублированных связей в промежуточных таблицах.

4. **CASCADE**: Используется ON DELETE CASCADE для автоматического удаления связанных записей.

## Проверка целостности

После импорта проверьте:
- ✅ Все внешние ключи правильно связаны
- ✅ Primary keys установлены на поле id
- ✅ UNIQUE constraints на промежуточных таблицах
- ✅ Правильные типы данных для всех полей