from django.urls import path
from . views import RecoveryHomepage, UpdateLog, getRecoveryData, getLiveData, ClearLog, EnableExceed

urlpatterns = [
    path('', RecoveryHomepage, name = 'RecoveryHomepage'),
    path('updatelog', UpdateLog , name = 'UpdateLog'),
    path('getrecoverydata', getRecoveryData , name = 'getRecoveryData'),
    path('getlivedata', getLiveData, name = 'getLiveData'),
    path('clearlog', ClearLog , name='ClearLog'),
    path('enableexceed', EnableExceed , name='EnableExceed')
]