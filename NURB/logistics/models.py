from django.db import models
import custom_models

class InventoryItem(models.Model):
  item_type        = models.CharField(max_length=128)
  item_description = models.CharField(max_length=1024)
  
  def __unicode__(self):
    return self.item_type
  
class Inventory(models.Model):
  inventory_items = models.ManyToManyField(InventoryItem)
  
  def __unicode__(self):
    return '\n'.join(self.inventory_items)

class PostalAddress(models.Model):
  city     = models.CharField(max_length=256)
  state    = models.CharField(max_length=32)
  zipcode  = models.IntegerField()
  street_1 = models.CharField(max_length=256)
  street_2 = models.CharField(max_length=256)

  def __unicode__(self):
    return '{0} {1} : {2}, {3} {4}'.format(self.street_1, self.street_2, self.city, self.state, self.zipcode)

class Customer(models.Model):
  name    = models.CharField(max_length=256)
  address = models.ForeignKey(PostalAddress)

  def __unicode__(self):
    return self.name
  
class Order(models.Model):
  order_date     = models.DateTimeField()
  confirmed_date = models.DateTimeField()
  paid_date      = models.DateTimeField()
  shipped_date   = models.DateTimeField()
  subtotal       = custom_models.CurrencyField()
  shipping_cost  = custom_models.CurrencyField()
  customer       = models.ForeignKey(Customer)
  
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
