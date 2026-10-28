# Django server

Set `DJANGO_SECRET_KEY` in the environment before running the Django server.
For example, in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-local-development-key"
python manage.py runserver
```
