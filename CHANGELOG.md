# 0.0.2
## Update to django 2 and daphne 2

### Django
Python packages :
```sudo pip3 install -U django django django-crispy-forms django_auth_ldap```
Pull updates for django-bootstrap3-datetimepicker
### Daphne
Update and install new required package.
```sudo pip3 install -U daphne channels channels_api channels_redis```
Add/modify ASGI_APPLICATION and CHANNEL_LAYERS in settings.py like in settings.example.py.
For deployement, change supervisord configuration so it doesn't launch runworker and that daphne point to the correct asgi entry `happyschool.asgi:application`:
```
command=/usr/local/bin/daphne -b 0.0.0.0 -p 8080 happyschool.asgi:application --access-log /var/log/daphne.log
```
