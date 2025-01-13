[![Django Project Badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://docs.djangoproject.com/en/5.1/)
[![TailwindCSS](https://img.shields.io/badge/Django%20TailWind-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://django-tailwind.readthedocs.io/en/latest/index.html)
--
Django project styled with TailWindCSS with the Tailwind-Django

## Getting started

Initialize the GitFlow (press enter for all options)
```bash
git flow init
```
For more information about how Git Flow works click in [read more](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

</br>

### If not existing virtual environment, create one by running
```bash
python -m venv venv
```

### Activate the environment by running

**Windows**
```bash
./venv/Scripts/Activate
```
**Linux based systems**
```bash
source venv/bin/activate
```
</br>

### Install all the requirements

```bash
pip install -r requirements.py
```

**Install all the precommit hooks:**
```bash
pre-commit install
```

**Apply all the initial migrations**
```bash
python manage.py migrate
```

**Install the TailWind CSS dependencies**
```bash
python manage.py tailwind install
```

**Start the development server for TailWind by running:**
```bash
python manage.py tailwind start
```

**Start the development server for Django project by running:**
```bash
python manage.py runserver
```
