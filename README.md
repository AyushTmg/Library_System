#             Library Management system 



Welcome to the Library Management System – your library's newest ally! 📚 This intelligent system simplifies library tasks, serving everyone from avid readers to the unsung heroes working behind the scenes.


Technologies used: Django, Django Rest Framework, Djoser,Celery, Django Debug Toolbar, PostgreSQL, Redis, Pillow, Requests, Django-CORS-Headers,DRF-Nested-Routers.


User Roles:
--

Normal User: Explore the library catalog, view book details, leave reviews, reply to reviews, and reserve books.

Staff User: Possess all the permissions of a normal user, with additional capabilities to add, delete, and update books. Staff members can also monitor user activities, keeping track of book borrowings and returns using unique user IDs.

Admin User: Administrators possess elevated permissions, allowing them to manage all aspects of the library system, including user management, book inventory, and system configuration.



Notification
=


Reservation Notification
--

Upon successful reservation, a notification email is sent to the user.\
![image](https://github.com/AyushTmg/Library_System/assets/119398357/b15e5c9c-460b-4677-ad4a-381cc85ddf18)


Borrowing Notification
--
When a user borrows a book, a notification is sent, including details the due date.\
![image](https://github.com/AyushTmg/Library_System/assets/119398357/1c0b24be-f29d-4465-bdf4-de87ec52589d)


Return Notification
--
Upon returning books, a notification is sent, confirming the return and providing any relevant information\
![image](https://github.com/AyushTmg/Library_System/assets/119398357/1887e642-538a-479f-8a72-f7c4cfa30033)



## Installation


1-First of all clone this repo
--

        git clone https://github.com/AyushTmg/Library-System.git


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
                'NAME': 'your_database_name',
                'USER': 'your_database_user',
                'PASSWORD': 'your_database_password',
                'HOST': 'localhost',
                'PORT': '5432',
        }
        }

5-Add .env file and add these field
--

        EMAIL_USER="Your email"
        EMAIL="Your email"
        EMAIL_PASSWORD="email password"

        SECRET_KEY='secret key'


6-Migrate the changes to your database
--
        python manage.py makemigrations
        python manage.py migrate
        

7-Run Application with celery 
--
        python manage.py runserver
        celery -A main worker -l info
