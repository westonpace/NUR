from django.db import models
import custom_models

class InventoryItem(models.Model):
  item_type        = models.CharField(max_length=128)
  item_description = models.CharField(max_length=1024)
  
  def __unicode__(self):
    return self.item_type
  
class Order(models.Model):
  order_date     = models.DateTimeField()
  confirmed_date = models.DateTimeField()
  paid_date      = models.DateTimeField()
  shipped_date   = models.DateTimeField()
  subtotal       = custom_models.CurrencyField()
  shipping_cost  = custom_models.CurrencyField()
  
  def __unicode__(self):
    return 'Order with cost {0} made on {1}'.format(self.total_cost, self.order_date)

  @property
  def total_cost(self):
    return self.subtotal + self.shipping_cost

class LineItem(models.Model):
  order          = models.ForeignKey(Order)
  inventory_item = models.ForeignKey(InventoryItem)
  quantity       = models.PositiveIntegerField(default=1)
  
  def __unicode__(self):
    return '{0}: {1}'.format(self.inventory_item.item_type, self.quantity)

# Create your models here.
