from django.db import models

# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=50)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12)
    birth_date = models.DateField(max_length=50)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    block_status=models.BooleanField(default=False)
    def _str_(self):
        return str(self.id)

    @staticmethod
    def get_user_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=100)
    image = models.ImageField(null=True,blank=True)

class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=50)
    image = models.ImageField(null=True,blank=True)
    capacity =models.CharField(max_length=20,null=True)
    size =models.CharField(max_length=50)
    price=models.PositiveIntegerField(max_length=10)

class Enterprise(models.Model):
    person_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12)

class Driver(models.Model):
    driver_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    def _str_(self):
        return str(self.id)

    @staticmethod
    def get_user_by_email(email):
        try:
            return Driver.objects.get(email = email)
        except:
            return False
   
class Booking(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    date = models.DateField(max_length=50)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    enterprise_id = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True)
    pick_address=models.CharField(max_length=100)
    drop_address=models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    total_amount =models.PositiveIntegerField(max_length=6)
    status = models.CharField(max_length=50,default='pending')

class Track(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    trackorder_detail=models.CharField(max_length=100)

class Payment(models.Model):
    payment_status=models.BooleanField(default=False)
    payment_type=models.CharField(max_length=10)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Admindetail(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12)
    birth_date = models.DateField(max_length=50)
    def _str_(self):
        return str(self.id)

    @staticmethod
    def get_user_by_email(email):
        try:
            return Admindetail.objects.get(email = email)
        except:
            return False




    