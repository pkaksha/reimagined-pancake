# reimagined-pancake
A simple Backend only Bakery-Managament Application in DJango and Postgresql

1. #### POSTMAN API COLLECTION LINK
https://www.getpostman.com/collections/24f3a32da6ec821f0e65

2. #### STEPS FOR RUNNING THE BAKERY_APP :
   
    - Fetch repository :
       > git clone https://github.com/pkaksha/reimagined-pancake.git
    - if Docker is not installed
       > Check for installation steps of Docker at https://docs.docker.com/compose/install/
      
    - To build docker image and spin-off two container one for Django Web app and another for Postgresql run :
        > docker-compose up -d --build
       
    - Check Running Container :
        > docker ps
      
    - To Migrate prebuilt Migrations into DB :
        > docker-compose exec web python manage.py migrate
      
        - If any error such as jango.db.utils.OperationalError: FATAL:  database "db_name" does not exist then execute :
            > 1. docker-compose down -v
            > 2. docker-compose exec web python manage.py migrate
          
    - To bring down development containers (and the associated volumes with the -v flag) :
        > docker-compose down -v
