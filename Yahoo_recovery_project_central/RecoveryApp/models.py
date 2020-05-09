from django.db import models
from datetime import date

class RecoveryDataModel(models.Model):
	proxy = models.CharField(max_length = 100, db_index=True)
	firstname = models.CharField(max_length = 100, db_index=True)
	lastname = models.CharField(max_length = 100, db_index=True)
	gender = models.CharField(max_length = 10, db_index=True)
	birth_month = models.CharField(max_length = 10, db_index=True)
	birth_day = models.CharField(max_length = 10, db_index=True)
	birth_year = models.CharField(max_length = 10, db_index=True)
	username = models.CharField(max_length = 100, db_index=True, unique=True)
	password = models.CharField(max_length = 15, db_index=True)
	phone = models.CharField(max_length = 15, db_index=True)
	recoveryemail = models.CharField(max_length = 100, db_index=True)
	recoverydone = models.CharField(max_length = 10, default = 'False', db_index=True)
	log = models.CharField(max_length = 100, default = 'Not In Process', db_index=True)
	error = models.CharField(max_length = 100, default = 'No Error', db_index=True)
	insert_date = models.CharField(max_length = 20 , default = str(date.today()), db_index=True)
	process_trigger = models.CharField(max_length = 10, default = 'False', db_index=True)
	recovery_attempt = models.IntegerField(default = 0, db_index=True)
	disabled = models.CharField(max_length=10, default = 'False', db_index=True)
	employee_name = models.CharField(max_length = 100, default = 'None', db_index=True)
	recovery_month = models.CharField(max_length = 100, default = 'None')
	recovery_date = models.CharField(max_length = 100, default = 'None')


