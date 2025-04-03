from django.db import models
from datetime import datetime




class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    labor_contract = models.IntegerField()
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'
    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)

    def get_last_name(self):
        return self.full_name.split()[0]per

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds()
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds()

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)