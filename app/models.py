from django.db import models
def increment_invoice_number():
    last_invoice = Customer_Detail.objects.all().order_by('id').last()
    if not last_invoice:
        return 'EV0001'
    order_id = last_invoice.order_id
    invoice_int = int(order_id.split('EV')[-1])
    width = 4
    new_invoice_int = invoice_int + 1
    formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
    new_invoice_no = 'EV' + str(formatted)
    return new_invoice_no 
def Customer_number():
    last_invoice = Customer_Detail.objects.all().order_by('id').last()
    if not last_invoice:
        return 'CUS0001'
    customer_id = last_invoice.customer_id
    invoice_int = int(customer_id.split('CUS')[-1])
    width = 4
    new_invoice_int = invoice_int + 1
    formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
    new_invoice_no = 'CUS' + str(formatted)
    return new_invoice_no
def Worker_number():
    last_invoice = Worker_Detail.objects.all().order_by('id').last()
    if not last_invoice:
        return 'WOR0001'
    worker_id = last_invoice.worker_id
    invoice_int = int(worker_id.split('WOR')[-1])
    width = 4
    new_invoice_int = invoice_int + 1
    formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
    new_invoice_no = 'WOR' + str(formatted)
    return new_invoice_no  	
class Admin_Detail(models.Model):
	username = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	mobile = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.username
class Event(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000,null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)
	def __str__(self):
		return self.name
class Customer_Detail(models.Model):
	order_id = models.CharField('Event Id',max_length = 500, default = increment_invoice_number, null = True, blank = True)
	customer_id = models.CharField('Customer Id',max_length = 500, default = Customer_number, null = True, blank = True)
	customer_name = models.CharField(max_length=30)
	event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
	phone = models.CharField(max_length=30)
	event_date = models.DateField()
	event_time = models.CharField(max_length=30)
	address = models.TextField(max_length=2000)
	amount = models.CharField(max_length=30)
	place = models.TextField(max_length=2000)
	status = models.CharField(max_length=30)
	amount_paid = models.CharField(max_length=30,null=True,blank=True)
	def __str__(self):
		return self.customer_name
class Worker_Detail(models.Model):
	worker_id = models.CharField('Worker Id',max_length = 500, default = Worker_number, null = True, blank = True)
	event_id = models.CharField(max_length=200)
	worker_name = models.CharField(max_length=30)
	customer_id  = models.ForeignKey(Customer_Detail, on_delete=models.CASCADE)
	phone = models.CharField(max_length=30)
	job = models.CharField(max_length=30)
	tot_amount = models.CharField(max_length=200)
	paid = models.CharField(max_length=30)
	address = models.TextField(max_length=2000)
	def __str__(self):
		return self.worker_name