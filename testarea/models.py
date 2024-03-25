from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class InvoiceMaster(models.Model):
  invoice_no = models.IntegerField(null=False)
  invoice_desc = models.CharField(max_length=100)
  # invoice_date = models.DateField()
  # invoice_total = models.DecimalField(max_digits=10, decimal_places=2)
  # invoice_image = models.ImageField(upload_to ='invoice_image',null=True)
  # created_date = models.DateTimeField(auto_now_add=True)
  # modified_date = models.DateTimeField(auto_now=True)
  def __str__(self) :
    return str(self.invoice_no)




