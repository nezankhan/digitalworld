from pickle import FALSE
from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Inventory(models.Model):
    item_id = models.AutoField(primary_key=True,serialize=True)
    image = models.ImageField(default='default.jpg',upload_to='inventory_pics')
    product_name = models.CharField(max_length=100)
    description = models.TextField() #unrestricted text
    #date_posted = models.DateTimeField(auto_now_add=True) auto_now adds date when it was created but you cant change it later
    date_created = models.DateTimeField(default=timezone.now)
    product_type = models.TextField()
    stock_level = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.product_name

class SaleOrders(models.Model):
    order_number = models.AutoField(primary_key=True,serialize=True)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity= models.IntegerField(null =False)
    shipped_date = models.DateField(null = False)

    def __str__(self):
        return self.order_number

class Employees(models.Model):
    emp_id = models.AutoField(primary_key=True,serialize=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    hired_date = models.DateField(null = False)

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name

class PurchaseOrders(models.Model):
    po_id = models.AutoField(primary_key=True,serialize=True)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField(null =False)
    purchase_date = models.DateField(null = False)

    def __str__(self):
        return self.po_id

class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True,serialize=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name
    
    def save(self, *args, **kwargs):
        if len(Customers.objects.all())==0:
            super(Customers,self).save(*args, **kwargs)
        else:
            self.customer_id = Customers.objects.last().customer_id + 1
            super(Customers,self).save(*args, **kwargs)
    
    
    def get_absolute_url(self):
        return reverse('create-customer')

class SaleInvoices(models.Model):
    invoice_number = models.AutoField(primary_key=True,serialize=True)
    order_number = models.ForeignKey(SaleOrders, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    emp = models.ForeignKey(Employees, on_delete=models.CASCADE)
    discount = models.FloatField()
    invoice_date = models.DateField(null = False)
     
    def __str__(self):
        return self.invoice_number

class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True,serialize=True)
    supplier_address = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null= False)
    net_terms = models.IntegerField()
    date_contracted = models.DateField(null = False)

    def __str__(self):
        return self.company_name

class PurchaseInvoices(models.Model):
    purchase_number = models.AutoField(primary_key=True,serialize=True)
    po = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    amount  = models.FloatField()
    purchase_date = models.DateField(null = False)


    def __str__(self):
        return self.purchase_number

