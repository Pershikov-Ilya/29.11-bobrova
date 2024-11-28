import numpy as np
import math
import random
import statistics
import matplotlib.pyplot as plt

from six import print_

min_Cgar = 1010101010101
opt_C1 = 0
opt_C2 = 0
opt_C3 = 0
opt_Vmax = 0
opt_rent_price = 0

max_zatr = []  # Переместите это сюда

for i in range(100):
    mean_demand = 10  # средний спрос
    var_demand = 2    # отклонение
    mean_time = 3     # среднее время доставки
    var_delivery = 2  # отклонение
    C1 = random.randint(10, 20)  # стоимость хранения
    C2 = random.randint(2, 10)   # стоимость доставки партии
    C3 = random.randint(2, 10)   # штраф за дефицит товара
    reverse = 100      # изначальный запас на складе
    period_work = 100  # период работы склада (100 дней)
    part = 100         # объем новой партии товара
    Vmax = random.randint(100,500)      # вместимость склада
    rent_price = random.randint(10,20)  # стоимость аренды
    new_party_level = 40                      # уровень запаса, при котором заказывается новая партия

    def normal(mean, var):
        x = 0
        for i in range(12):
            x += random.random()
        x = x-6
        y = mean + var * x
        return math.ceil(y)

    price_all = 0
    price_day = 0
    price = []
    rent = 0
    days_new_party = 0
    flag = False
    flag_zakaz = False

    for day in range(period_work):
        # Если заявка на новую партию создана, уменьшается время её ожидания.
        # Когда партия прибыла, склад пополняется, а стоимость доставки добавляется к затратам.
        if days_new_party > 0 and flag_zakaz:
            days_new_party -= 1
        elif days_new_party == 0 and flag_zakaz:
            reverse += part
            price_all += part * C2

        price_all += reverse * C1

        spros = normal(mean_demand, var_demand)
        reverse -= spros

        # проверка на сколько свободен склад
        if reverse > Vmax:
            rent = reverse - Vmax
            reverse = Vmax
        elif reverse < Vmax and rent != 0:
            while reverse < Vmax and rent != 0:
                reverse += 1
                rent -= 1

        # +сумма за аренду
        if rent_price != 0:
            price_all += rent_price * rent

        # +цена за дефицит
        if reverse < 0:
            price_all += abs(reverse) * C3
            reverse = 0

        # проверка уровень запаса не меньше ключевого значения
        if reverse < new_party_level:
            flag = True

        # создание заявки на новую партию
        if flag:
            flag = False
            days_new_party = normal(mean_time, var_delivery)
            flag_zakaz = True

        price_day = price_all - price_day
        price.append(price_day)
        price_day = price_all

    Cgar = price_all / period_work + 1.28 * statistics.stdev(price)

    max_zatr.append(Cgar)  # Добавляем значение в max_zatr
    print(Cgar)

    if min_Cgar > Cgar:
        min_Cgar = Cgar
        opt_C1 = C1
        opt_C2 = C2
        opt_C3 = C3
        opt_Vmax = Vmax
        opt_rent_price = rent_price

print('Минимальный максимальные гарантированные затраты: ', min_Cgar)
print("Оптимальные значения:")
print('C1', opt_C1)
print('C2', opt_C2)
print('C3', opt_C3)
print('Vmax', opt_Vmax)
print('rent_price', opt_rent_price)

plt.plot(range(len(max_zatr)), max_zatr, marker='o')
plt.xlabel('Индекс элемента')  # Подписываем ось X
plt.ylabel('Значение max_zatr')  # Подписываем ось Y
plt.title('График изменения max_zatr')  # Добавляем заголовок
plt.grid(True)  # Включаем сетку
plt.show()  # Показываем график
