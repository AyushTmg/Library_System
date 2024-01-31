#             Library System API 







Technologies used:Django, Django Rest Framework,Simple JWT ,Celery, Django Debug Toolbar, PostgreSQL, Redis, etc


    Please Use Better Comments Extension of VsCode for better 
    readability since i have used it in this project to highlight 
    my Comments 



## Installation


1-First of all clone this repo
--

        https://github.com/AyushTmg/Library_System_Ramailo_Tech.gitt


2-Setup a virtual enviroment
--

        python -m venv venv


3-Install all dependencies from the requirements.txt in a virtual enviroment
--

        pip install -r requirements.txt


4- Configure database according to your reliability in this case postgres is used
--
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME':os.environ.get("DB_NAME"),
                'USER': 'postgres', 
                'PASSWORD':os.environ.get("DB_PASS"), 
                'HOST': 'localhost', 

            }
        }

- If you want to use default database you can also uncomment from the setting.py 

5-Add .env File and add these field or just configure example.env
--

        EMAIL="Your Email Address"
        EMAIL_PASSWORD="You Email Password"

- You need to add this if you are also using postgres as your database 

        DB_NAME='Add Your Database Name'
        DB_PASS='Add Your Database Password'



6-Migrate the changes to your database
--
        python manage.py makemigrations 
        python manage.py migrate

7-Run Application
--
        python manage.py runserver

## API documentation

        https://documenter.getpostman.com/view/30946823/2s9YytgfuE
