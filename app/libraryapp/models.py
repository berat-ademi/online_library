from django.db import models


# Create your models here.
class Customer(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " " + self.email + " " + self.address

class Authors(models.Model):
    author_name = models.CharField(max_length=50)

    def __str__(self):
        return self.author_name

class Publishers(models.Model):
    publisher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.publisher_name

class Books(models.Model):
    book_name = models.CharField(max_length=50)
    author_id = models.ForeignKey(Authors, on_delete=models.CASCADE) #foreign key prej tabeles Authors
    isbn = models.CharField(max_length=25)
    publisher_id = models.ForeignKey(Publishers, on_delete=models.CASCADE) #foreign key prej tabeles Publisher
    price = models.FloatField()

    def __str__(self):
        return self.book_name

class Loans(models.Model):
    loan_date = models.DateField()
    loan_is_active = models.BooleanField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE) #foreign key prej tabeles Customer
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE)#foreign key prej tabeles Books

    def __str__(self):
        return str(self.loan_date)