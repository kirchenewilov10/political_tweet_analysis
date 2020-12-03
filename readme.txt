1. Install python packages needed for this website.
   It can be intalled by pip install command and packages needed are
   in ./requirements.txt

   -pip install tweepy==3.8.0
   -pip install django-background-tasks
    ..

2. You can edit file pre-defining group of people here
    - {webroot}/static/library/txt/group

        ..
        @barbarae_whitee, #django
        @SarahuTurnera3, #djangorestframework


3. Run website
    -python manage.py runserver

4. Register and run background task
    4.1 Registering background task
    You have background module for daily update of database from twitter
    and you have to register background task before run it.
    Calling this url of this web will register background task
    or it can be done by curl,postman.

    {webdomain}/task/register_twitter_task

    ex:
        curl -I 'http:localhost/task/register_twitter_task'

    4.2 run background task
    After running background task,database will be updated daily.

    -python manage.py process_tasks