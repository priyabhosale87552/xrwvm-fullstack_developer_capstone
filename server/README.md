# Django server

Set `DJANGO_SECRET_KEY` in the environment before running the Django server.
For example, in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-local-development-key"
python manage.py runserver
```

## Deploy to Render

1. Push this repository to GitHub and sign in to Render.
2. Select **New +** → **Blueprint** and connect `priyabhosale87552/xrwvm-fullstack_developer_capstone`.
3. Review `render.yaml`. It creates a free web service and a free PostgreSQL database. The free database is temporary and may expire; upgrade to a paid persistent database if review data must be retained.
4. Select **Apply** to create the services. Render installs dependencies, collects static files, applies database migrations at startup, and launches Gunicorn.
5. Wait for the web service deployment to finish successfully, then open its `onrender.com` URL.
6. Use **Sign up** on the deployed home page to create an account, then sign in to post reviews. Create an admin user from the Render service shell with `python manage.py createsuperuser` if admin access is needed.
