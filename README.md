

# MicroServices

A basic level microservice architecture demo  
Separate microservices project  
Generate token to authenticate users to access api  
UUID is used as a unique identifier in our system to ensure that each item and order has a globally distinct identification, facilitating reliable data management and preventing collisions in distributed microservices architecture.  


# Installation

cd project  
py -m venv venv  
venv/scripts/activate  
pip install -r requirements.txt  
py manage.py migrate  
py manage.py runserver  