from django.shortcuts import render, redirect, HttpResponse
from RecoveryProject.settings import db
from django.views.decorators.csrf import csrf_exempt
import json, random
from datetime import datetime
from bson.objectid import ObjectId
from . models import RecoveryDataModel
from RecoveryProject.settings import STATIC_ROOT
import pandas as pd

# disabled = RecoveryDataModel.objects.filter(recoverydone = 'False')
# print('-----------',disabled)
# for i in disabled:
# 	i.disabled = "True"
# 	i.save()

def RecoveryHomepage(request):
	context = {}
	try:
		check_admin = request.user.is_superuser
		context['employee_columns'] = set([emp['employee_name'].strip().title() for emp in RecoveryDataModel.objects.order_by().values('employee_name').distinct()])
		print('-------------employee_columns---------------',context['employee_columns'])
		context['employee_value'] = [(emp, RecoveryDataModel.objects.filter(employee_name__icontains = emp).count() or 0) for emp in context['employee_columns']]
		
		if check_admin == True:
			context['check_admin'] = check_admin

		context['month_wise'] = False
		context['date_wise'] = False
		context['filter'] = False

		recovered = RecoveryDataModel.objects.filter(recoverydone='True').count()
		notrecovered= RecoveryDataModel.objects.filter(recoverydone='False', disabled='False').count()
		exceedattempts = RecoveryDataModel.objects.filter(recovery_attempt__gt = 2, recoverydone='False').count()
		disabled = RecoveryDataModel.objects.filter(disabled='True',recoverydone='False').count()
		allseeds = RecoveryDataModel.objects.all().count()
		context['results'] = [recovered, notrecovered, exceedattempts, disabled]
		context['total_seeds'] = allseeds

		context['month_filter'] = RecoveryDataModel.objects.order_by().values('recovery_month').distinct()
		dates = [i['recovery_date'] for i in RecoveryDataModel.objects.order_by().values('recovery_date').distinct()]
		context['date_filter'] = sorted(dates, key=lambda d: d.split('-'), reverse=True)

		# context['recovered']  = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'True'})
		# context['notrecovered'] = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'False'})
		# context['exceedattempts'] = db.RecoveryApp_recoverydatamodel.find({'recovery_attempt': { '$gt': 2}})
		# context['disabled'] = db.RecoveryApp_recoverydatamodel.find({'disabled':'True'})
		# context['allseeds'] = db.RecoveryApp_recoverydatamodel.find()
		# context['results'] = [context['recovered'].count(),context['notrecovered'].count(),context['exceedattempts'].count(),context['disabled'].count()]
		# context['total_seeds'] = context['recovered'].count() + context['notrecovered'].count()

		if request.method == 'POST':
			seeds = request.POST.get('seed')
			month_filter = request.POST.get('month_filter')
			date_filter = request.POST.get('date_filter')
			print('month_filter',month_filter, 'date_filter',date_filter)		
			if seeds != None:
				total_seeds = seeds.split('\n')
				for seed in total_seeds:
					seeddetails = seed.split('\t')
					if len(seeddetails) == 11:
						duplicate = RecoveryDataModel.objects.filter(username=seeddetails[7])
						if len(duplicate) == 0:
							try:
								recoverydomain = ['@hownewhouse.com','@racehexagon.com','@markquasar.com','@partyfierce.com']
								recoveryemail = seeddetails[7]+random.choice(recoverydomain)
								modelobject = RecoveryDataModel(proxy=seeddetails[0],firstname=seeddetails[1],
									lastname=seeddetails[2],gender=seeddetails[3],birth_month=seeddetails[4],
									birth_day=seeddetails[5],birth_year=seeddetails[6],username=seeddetails[7],
									password=seeddetails[8],phone=seeddetails[9],recoveryemail=recoveryemail,
									employee_name=seeddetails[10])
								modelobject.save()
							except:
								continue
					else:
						context['error'] = 'Please Insert data in below Format'
				return redirect('RecoveryHomepage')

			if month_filter != None and seeds == None and date_filter==None :
				context['month_wise'] = True
				context['employee_columns'] = set([emp['employee_name'].strip().title() for emp in RecoveryDataModel.objects.order_by().values('employee_name').distinct()])
				context['employee_value'] = [(emp, RecoveryDataModel.objects.filter(employee_name__contains = emp,recovery_month=month_filter).count() or 0) for emp in context['employee_columns']]
				recovered = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'True','recovery_month':month_filter})
				notrecovered = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'False','recovery_month':month_filter})
				# recovered = RecoveryDataModel.objects.filter(recoverydone='True',recovery_month=month_filter)
				# notrecovered = RecoveryDataModel.objects.filter(recoverydone='False',recovery_month=month_filter)
				exceedattempts = RecoveryDataModel.objects.filter(recovery_attempt__gt = 2,recovery_month=month_filter,recoverydone='False')
				disabled = RecoveryDataModel.objects.filter(disabled='True',recovery_month=month_filter)
				allseeds = RecoveryDataModel.objects.filter(recovery_month=month_filter)

				context['recovered'] = recovered
				context['notrecovered'] = notrecovered
				context['exceedattempts'] = exceedattempts[:10]
				context['disabled'] = disabled[:10]
				context['month'] = month_filter

				context['results'] = [recovered.count(),notrecovered.count(),exceedattempts.count(),disabled.count()]
				context['total_seeds'] = allseeds.count()
				return render(request,'RecoveryApp/index.html', context)
				

			if date_filter != None and seeds == None and month_filter == None:
				context['date_wise'] = True
				context['employee_columns'] = set([emp['employee_name'].strip().title() for emp in RecoveryDataModel.objects.order_by().values('employee_name').distinct()])
				context['employee_value'] = [(emp, RecoveryDataModel.objects.filter(employee_name__contains = emp,insert_date=date_filter).count()) for emp in context['employee_columns']]
				
				context['recovered'] = RecoveryDataModel.objects.filter(recoverydone='True',recovery_date=date_filter)
				# context['notrecovered'] = RecoveryDataModel.objects.filter(recoverydone='False',recovery_date=date_filter)
				# context['exceedattempts'] = RecoveryDataModel.objects.filter(recovery_attempt__gt = 2,recovery_date=date_filter)
				# context['disabled'] = RecoveryDataModel.objects.filter(disabled='True',recovery_date=date_filter)
				# context['allseeds'] = RecoveryDataModel.objects.filter(recovery_date=date_filter)
				# context['results'] = [context['recovered'].count(),context['notrecovered'].count(),context['exceedattempts'].count(),context['disabled'].count()]
				# context['total_seeds'] = context['allseeds'].count()


				# context['recovered']  = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'True','recovery_date':date_filter})
				context['notrecovered'] = db.RecoveryApp_recoverydatamodel.find({'recoverydone':'False','recovery_date':date_filter,'disabled':'False'})
				context['exceedattempts'] = db.RecoveryApp_recoverydatamodel.find({'recovery_attempt': { '$gt': 2},'recovery_date':date_filter, 'recoverydone':'False'})
				context['disabled'] = db.RecoveryApp_recoverydatamodel.find({'disabled':'True','recovery_date':date_filter})
				context['results'] = [context['recovered'].count(),context['notrecovered'].count(),context['exceedattempts'].count(),context['disabled'].count()]
				context['total_seeds'] = context['recovered'].count() + context['notrecovered'].count()

				return render(request,'RecoveryApp/index.html', context)
				
			else:
				return redirect('RecoveryHomepage')
	except:pass
	
	return render(request,'RecoveryApp/index.html', context)


@csrf_exempt
def UpdateLog(request, ):

	"""
		# pass following parameter to API

		import json ,requests
		url = 'http://localhost:8000/updatelog'
		seed = {"id": 1, "log": "In Process", "error": "Error Not Found", "proxy": "181.214.155.62:3129", "firstname": "Britta", "lastname": "Cox", "gender": "Female", "birth_month": "7", "birth_day": "10", "birth_year": "1995", "username": "BrittaCoxjybxxm", "password": "8LyjfeOBmIei", "phone": "83153246362\r", "recoveryemail": "BrittaCoxjybxxm@hownewhouse.com", "recoverydone": "False"},
		myobj = {'seed':json.dumps(seed)}
		print(myobj)
		x = requests.post(url, data = myobj)
		print(x.text)

	"""

	try:
		if request.method == 'POST':
			seedlog = request.POST.get('seed')
			seedlog = json.loads(seedlog)
			print('-----------seedlog-----------',type(seedlog),seedlog)
			current_object = RecoveryDataModel.objects.get(id=int(seedlog['id']))
			current_object.log = seedlog['log']
			current_object.error = seedlog['error']
			current_object.recoverydone = seedlog['recoverydone'] 
			current_object.process_trigger = seedlog['process_trigger']
			current_object.recovery_attempt = seedlog['recovery_attempt']
			current_object.recovery_month = seedlog['recovery_month']
			current_object.recovery_date = seedlog['recovery_date']
			current_object.recoveryemail = seedlog['recoveryemail']
			current_object.save()

			return HttpResponse("successfully updated log !")
	except Exception as e: print('This error ocuured while updating log : ', e) 
			

def getRecoveryData(request):
	current_user = request.user
	allseeds = RecoveryDataModel.objects.filter(recoverydone='False', recovery_attempt__lt = 3, disabled = 'False', process_trigger = 'False')[:5]
	seeds = []
	for seed in allseeds:
		seeddict = {'id':seed.id, 'log':seed.log, 'error':seed.error,'proxy':seed.proxy ,
		'firstname':seed.firstname, 'lastname':seed.lastname, 'gender':seed.gender, 
		'birth_month':seed.birth_month, 'birth_day':seed.birth_day, 'birth_year':seed.birth_year,
		'username':seed.username, 'password':seed.password, 'phone':seed.phone, 
		'recoveryemail':seed.recoveryemail, 'recoverydone':seed.recoverydone, 'insert_date':seed.insert_date,
		'recovery_attempt' : seed.recovery_attempt, 'disabled' : seed.disabled, 'employee_name' : seed.employee_name }
		seeds.append(seeddict)
		
	return HttpResponse(json.dumps(seeds))



def getLiveData(request):
	current_user = request.user
	allseeds = RecoveryDataModel.objects.filter(process_trigger = 'True')
	
	seeds = []
	for seed in allseeds:
		seeddict = {'id':seed.id, 'log':seed.log, 'error':seed.error,'proxy':seed.proxy ,
		'firstname':seed.firstname, 'lastname':seed.lastname, 'gender':seed.gender, 
		'birth_month':seed.birth_month, 'birth_day':seed.birth_day, 'birth_year':seed.birth_year,
		'username':seed.username, 'password':seed.password, 'phone':seed.phone, 
		'recoveryemail':seed.recoveryemail, 'recoverydone':seed.recoverydone, 'insert_date':seed.insert_date,
		'recovery_attempt' : seed.recovery_attempt, 'disabled' : seed.disabled, 'employee_name' : seed.employee_name }
		seeds.append(seeddict)

	
		
	return HttpResponse(json.dumps(seeds))


def ClearLog(request):
	allseeds = RecoveryDataModel.objects.filter(process_trigger = 'True')
	for seed in allseeds:
		try:
			seed.process_trigger = 'False'
			seed.save()
		except:
			continue
	return redirect('RecoveryHomepage')


def EnableExceed(request):
	allseeds = RecoveryDataModel.objects.filter(recovery_attempt__gt = 2)
	for seed in allseeds:
		try:
			seed.recovery_attempt = 1
			seed.save()
		except:
			continue
	return redirect('RecoveryHomepage')