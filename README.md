[![Django TailWind Badge](https://img.shields.io/badge/Django%20Tailwind-8A2BE2)](https://django-tailwind.readthedocs.io/en/latest/index.html)
[![Django Project Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://docs.djangoproject.com/en/5.1/)
### Getting started
If not existing virtual environment, create one by running
```bash
python -m venv venv
```

Activate the environment by running

**Windows**
```bash
./venv/Scripts/Activate
```
**Linux based systems**
```bash
source venv/bin/activate
```


Install all the requirements

```bash
pip install -r requirements.py
```

Apply all the initial migrations
```bash
python manage.py migrate
```

Install the tailwind CSS dependencies
```bash
python manage.py tailwind install
```

Start the development server for Tailwind by running:
```bash
python manage.py tailwind start
```

Start the development server for Django project by running:
```bash
python manage.py runserver
```