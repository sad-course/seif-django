
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