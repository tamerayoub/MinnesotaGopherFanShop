I might have had to do this
python -m pip install Pillow 

Migrate all the models to the database
python manage.py migrate     

Run the application 
python manage.py runserver  

To access the database
http://127.0.0.1:8000/admin/ 

Create Superuser 
python manage.py createsuperuser

Login to database with new creditials to view sqllite db tables