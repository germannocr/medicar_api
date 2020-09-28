# Medicar App
App, made in Django and Django Rest in Backend and Angular in Frontend , for creating and maintaining an medical system.

## Setting up the environment:

 ### Backend:
 #### 1) To configure the environment and run the application in a venv, the project has a requirements.txt file with all the necessary dependencies.
 #### 2) You will need to create a database called "medicar" using postgres. The rest of the information on this, as user and password, is in a dictionary called "DATABASES" in the project's settings file. 
 #### 3) Once created, just run the command ```python manage.py makemigrations```, and then ```python manage.py migrate``` for the database to be ready.
 #### 4) To access the administrative interface, it will be necessary to create a superuser with the command ```python manage.py createsuperuser --email admin@example.com --username admin```, passing the password then and confirming it. 
 #### 5) Finally, with the database ready and the dependencies installed, it is necessary to run the command ```python manage.py runserver``` at the root of the project.
 
 ### Frontend:
 #### 1) When cloning the project, it will be necessary to run the command ```npm install``` or ```yarn```, depending on the manager used. After executing the command, the necessary dependencies for the Angular project will be downloaded.
 #### 2) After the download is made, the command ```npm start``` or ```ng serve --o``` it can be run at the root of the project to start the application.
 ## !Reminder: it is necessary that the API of the Backend folder is running for the project to function fully!

 
## Authentication:

 ### If you want to use an application such as Postman or Insomnia to make requests to API in Backend only, or even via curl, you must send a field in the request header called Authorization, with the prefix JWT and the authentication token. The token must be returned when logging in or registering in the application.
 
 #### Example: Authorization: JWT <user_token>
 #### Available URL's:
  - admin/ - Available via browser only. Administrative interface for creating Especialidade, Medico and Agenda objects.
    - For the "horarios" field in the agenda creation, as it is a list of times, it is enough that the user passes in the required field something like: "14:00, 21:00", without quotes.
  - registration/ - POST -> It allows the creation of new users in the system.
  - login/ - POST -> It allows the login of existing users, through username / email and password.
 
  - delete_consulta/<int:consulta_id>: DELETE -> It allows the deletion of an existent Consulta object, passing Consulta unique identifier.
  - create_consulta/: POST -> It allows create new Consulta objects, passing information such as Agenda identifier and scheduled time.
  - retrieve_especialidades/: GET -> Allows you to search existent Especialidade objects.
    - Possible query params: 
      - search: Especialidade name
  - retrieve_medicos/: GET -> Allows you to search existent Medico objects.
    - Possible query params: 
      - search: Medico name
      - especialidade: Especialidade name
  - retrieve_consultas/: GET -> Allows you to search existent Consulta objects.
  - retrieve_agendas/: GET -> Allows you to search existent Agenda objects.
    - Possible query params: 
      - medico: Medico identifier
      - especialidade: Especialidade identifier
      - data_inicio: Start date for filtering, in YYYY-MM-DD format. 
      - data_final: End date for filtering, in YYYY-MM-DD format.

 
