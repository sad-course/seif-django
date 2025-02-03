# This guide will help you to configure the environment to develop

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

</br>

### Configuring the environment to develop
**Create the env file for the variables**
```bash
python manage.py makenv dev
```
* Make your modifications if necessary in you env file
</br>
</br>

**Switch environent to the desired env file**
```bash
python manage.py env dev
```

**Check database configuration and create if not already**
```bash
python manage.py checkdb
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
