from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime
from django.conf import settings

def admin_login(request):
	if request.session.has_key('admin'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Admin_Detail.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('username')
				request.session['admin'] = username
				a = request.session['admin']
				sess = Admin_Detail.objects.only('id').get(username=a).id
				request.session['admin_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'admin_login.html',{})
def admin_logout(request):
	try:
		del request.session['admin']
		del request.session['admin_id']
	except:
		pass
	return render(request, 'admin_login.html', {})
def dashboard(request):
	tot = Customer_Detail.objects.all().aggregate(Sum('amount'))
	a = Customer_Detail.objects.all().aggregate(Count('id'))
	paid = Customer_Detail.objects.all().aggregate(Sum('amount_paid'))
	w_tot = Worker_Detail.objects.all().aggregate(Sum('tot_amount'))
	w_pay = Worker_Detail.objects.all().aggregate(Sum('paid'))
	return render(request,'dashboard.html',{'tot':tot,'paid':paid,
	'w_tot':w_tot,'w_pay':w_pay,'a':a})
def add_event(request):
	if request.method == 'POST':
		a=request.POST.get('name')
		b = request.POST.get('con')
		c = request.FILES['img']
		post=Event.objects.create(name=a,description=b,image=c)
		messages.success(request,'Event Added Successfully')
	return render(request,'add_event.html',{})
def events(request):
	a=Event.objects.all()
	return render(request,'events.html',{'b':a})
def add_customer(request):
	a = Event.objects.all()
	if request.method == 'POST':
		customer_name=request.POST.get('customer_name')
		event_name = request.POST.get('event_name')
		evn = Event.objects.get(id=int(event_name))
		phone = request.POST.get('phone')
		event_date = request.POST.get('event_date')
		event_time = request.POST.get('event_time')
		address = request.POST.get('address')
		amount = request.POST.get('amount')
		place = request.POST.get('place')
		post=Customer_Detail.objects.create(customer_name=customer_name,event_name=evn,
		phone=phone,event_date=event_date,event_time=event_time,address=address,amount=amount,
		place=place,status='')
		messages.success(request,'Customer Added Successfully')
	return render(request,'add_customer.html',{'a':a})
def customers(request):
	a=Customer_Detail.objects.all()
	return render(request,'customers.html',{'a':a})
def delete_customer(request,pk):
	Customer_Detail.objects.filter(id=pk).delete()
	return redirect(customers)
def booked_event(request):
	a=Customer_Detail.objects.all()
	return render(request,'booked_event.html',{'a':a})
def event_details(request,pk):
	a=Customer_Detail.objects.filter(order_id=pk)
	return render(request,'event_detail.html',{'a':a})
def workers(request,pk,cus_id):
	a=Worker_Detail.objects.filter(event_id=pk,customer_id=cus_id)
	return render(request,'workers.html',{'pk':pk,'cus_id':cus_id,'a':a})
def add_worker(request,pk,cus_id):
	if request.method == 'POST':
		worker_name=request.POST.get('worker_name')
		job = request.POST.get('job')
		customer_id = Customer_Detail.objects.get(id=cus_id)
		phone = request.POST.get('phone')
		tot_amount = request.POST.get('tot_amount')
		paid = request.POST.get('paid')
		address = request.POST.get('address')
		post=Worker_Detail.objects.create(worker_name=worker_name,job=job,event_id=pk,
		phone=phone,customer_id=customer_id,paid=paid,address=address,tot_amount=tot_amount)
		messages.success(request,'Worker Added Successfully')
	return render(request,'add_worker.html',{})
def update(request,pk):
	if request.method == 'POST':
		paid =request.POST.get('paid')
		upd = Worker_Detail.objects.filter(id=pk).update(paid=paid)
		if upd:
			messages.success(request,'updated Successfully')
	return render(request,'update.html',{})
def customer_detail(request):
	event_id = request.GET.get('event_id')
	a=Customer_Detail.objects.filter(order_id=event_id)
	b=Customer_Detail.objects.filter(order_id=event_id)
	if request.method == 'POST':
		amount_paid=request.POST.get('amount_paid')
		status=request.POST.get('status')
		upd=Customer_Detail.objects.filter(order_id=event_id).update(amount_paid=amount_paid,
		status=status)
		if upd:
			messages.success(request,'updated Successfully')
	return render(request,'customer_detail.html',{'a':a,'b':b})
def event_status(request,pk):
	a=Customer_Detail.objects.filter(order_id=pk)
	return render(request,'event_status.html',{'a':a})
def report(request):
	cursor = connection.cursor()
	post = '''SELECT c.order_id,c.customer_id,c.customer_name,c.phone,c.amount,c.amount_paid,
	w.worker_id,w.worker_name,w.tot_amount,w.paid,c.status from app_customer_detail as c INNER JOIN app_worker_detail as w
	ON c.order_id=w.event_id''' 
	query = cursor.execute(post)
	row = cursor.fetchall()
	tot = Customer_Detail.objects.all().aggregate(Sum('amount'))
	paid = Customer_Detail.objects.all().aggregate(Sum('amount_paid'))
	w_tot = Worker_Detail.objects.all().aggregate(Sum('tot_amount'))
	w_pay = Worker_Detail.objects.all().aggregate(Sum('paid'))
	return render(request,'report.html',{'row':row,'tot':tot,'paid':paid,
	'w_tot':w_tot,'w_pay':w_pay})
def single_profit(request,pk):
	tot = Customer_Detail.objects.filter(order_id=pk).aggregate(Sum('amount'))
	paid = Customer_Detail.objects.filter(order_id=pk).aggregate(Sum('amount_paid'))
	w_tot = Worker_Detail.objects.filter(event_id=pk).aggregate(Sum('tot_amount'))
	w_pay = Worker_Detail.objects.filter(event_id=pk).aggregate(Sum('paid'))
	return render(request,'single_profit.html',{'tot':tot,'paid':paid,
	'w_tot':w_tot,'w_pay':w_pay,'pk':pk})
def search(request):
	if request.method == 'POST':
		search = request.POST.get('search')
		a=Worker_Detail.objects.filter(event_id=search)
		return render(request,'search.html',{'a':a})
	return render(request,'search.html',{})

