Welcome to the Minnesotan Gopher Fan Shop E-commerce Project! This is a responsive website that integrates e-commerce features with CRUD operations, allowing users to browse, select, purchase, and update a variety of Gopher products! This website was utilized and developed using tools that include Django, Python, SQLite, HTML/CSS/JS and the MVT design!

To run this project in your environment, please follow the following instructions!


Assuming Django and Python is already installed in your environment ->


Go ahead and pull the Repo from Github and open it up in your preferred IDE


Install Pillow, Pillow is a powerful library for handling images in Python
python -m pip install Pillow 


Migrate all the models to the SQLite Database
python manage.py migrate     


Now run the application, and follow the link given in your terminal
python manage.py runserver  


To access the database, copy the following url to your browser
http://127.0.0.1:8000/admin/ 


Create a Superuser to access the database
python manage.py createsuperuser


Now login to database with your new user creditials to view SQLite db tables!


You should now have access to the Minnesota Gopher Fan Shop aswell as its database! 
I hope you enjoy this project!

Thank you, Tamer



