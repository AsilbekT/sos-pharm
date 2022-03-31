from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from accounts.models import Account
from datetime import date
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Sotuvchilar(models.Model):
    user = models.OneToOneField(Account,  on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['created']
        
    @property
    def get_completed_total(self):
        order = Order.objects.get(sotuvchi=self.id)
        orderqarz = OrderQarz.objects.filter(order=order.id)
        items = order.orderitem_set.all()
        count = 0
        for i in orderqarz:
            qarzitems = i.orderqarzitem_set.filter(completed=True)
            count += len(qarzitems)
        try:
            final = 100 // len(items) * count
        except:
            final = 0
        return final

    @property
    def get_total_aptekalar(self):
        order = Order.objects.get(sotuvchi=self.id)
        items = order.orderitem_set.all()
        total = ""
        for i in items:
            if i.apteka.name not in total:
                total += i.apteka.name + '\n'
        return total
        
    def __str__(self):
        return self.name


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']



class Aptekalar(models.Model):
    user = models.ForeignKey(Sotuvchilar, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()

    class Meta:
        ordering = ['created']
        


    def __str__(self):
        return str(self.id)

class Dorilar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, default='')
    price = models.IntegerField(blank=True, default=0)
    available = models.IntegerField(blank=True, default=0)

    class Meta:
        ordering = ['created']
        


    def __str__(self):
        return self.name





class Order(models.Model):
    sotuvchi = models.ForeignKey(Sotuvchilar, null=True, blank=True, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, default='Tashkent')
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total


    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    dorilar = models.ForeignKey(Dorilar, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    apteka = models.ForeignKey(Aptekalar, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_ended = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = int(self.dorilar.price) * int(self.quantity)
        return total

    def __str__(self):
        return self.dorilar.name


class OrderQarz(models.Model):
    dorilar = models.ForeignKey(Dorilar, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    apteka = models.ForeignKey(Aptekalar, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField(default=date.today)
    qoldi = models.IntegerField(default=0, null=True, blank=True)
    
    @property
    def get_cart_total(self):
        order_items = self.orderqarzitem_set.all()
        total = sum([item.get_total for item in order_items if item.completed != True])
        return total

    @property
    def get_qarz(self):
        order_items = self.orderqarzitem_set.filter(completed=False)
        total = sum([item.get_total for item in order_items if item.completed != True])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderqarzitem_set.all()
        total = sum([item.quantity for item in order_items if item.completed != True])
        return total

    def __str__(self):
        return self.dorilar.name


class OrderQarzItem(models.Model):
    dorilar = models.ForeignKey(Dorilar, on_delete=models.SET_NULL, null=True)
    orderQarz = models.ForeignKey(OrderQarz, on_delete=models.SET_NULL, null=True)
    apteka = models.ForeignKey(Aptekalar, on_delete=models.SET_NULL, null=True)
    dori_name = models.CharField(max_length=200, blank=True)
    apteka_name = models.CharField(max_length=200, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    umumiy_summa = models.IntegerField(default=0, null=True, blank=True)
    qoldi = models.IntegerField(default=0, null=True, blank=True)
    bought_day = models.DateField(default=date.today)
    completed = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.checked == False:
            self.umumiy_summa = int(self.dorilar.price) * int(self.quantity)
            self.qoldi = self.umumiy_summa
            self.dori_name = self.dorilar.name
            self.apteka_name = self.apteka.name
            self.checked = True
        super(OrderQarzItem, self).save(*args, **kwargs)


    @property
    def get_total(self):
        total = int(self.dorilar.price) * int(self.quantity)
        return total

    def __str__(self):
        return self.dorilar.name