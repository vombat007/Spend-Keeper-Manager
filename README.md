# Spend-Keeper-Manager
"Spend Keeper Manager": Track expenses, set budgets, and manage finances effortlessly. 
With intuitive tools and insightful analytics, stay in control of your money on the go. Built for Android using Python Kivy.


# Full descriptions
"Spend Keeper Manager" is a comprehensive financial management application designed to empower users with effective expense tracking and personalized budget management. 
Built on the Python Kivy framework for seamless integration across Android platforms, this app offers intuitive tools to monitor spending habits, categorize expenses, and set budgetary goals.

With Spend Keeper Manager, users can effortlessly track their daily expenditures, identify trends, and make informed financial decisions. 
The app provides insightful analytics and customizable reports to visualize spending patterns and allocate resources wisely.

From managing recurring expenses to planning for long-term financial objectives, Spend Keeper Manager serves as a reliable companion for individuals seeking to achieve greater fiscal responsibility and control over their finances.



## Run the Django API app locally :
~~~
python manage.py runserver --settings=django_spend_keeper.settings.dev 
~~~

## See url of documentation

~~~
http://your_ip/api/schema/
http://your_ip/api/schema/redoc/
http://your_ip/api/schema/swagger-ui/
~~~


## To run tests use this command:
~~~
python manage.py test django_app_api.tests --settings=django_spend_keeper.settings.dev
 
python manage.py test django_app_api.tests.tests_models --settings=django_spend_keeper.settings.dev

python manage.py test django_app_api.tests.tests_views --settings=django_spend_keeper.settings.dev 
~~~