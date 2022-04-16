## User manual

___________________________________________________________________________________________________________________________________________________________________________________________________________________________

### Install requirements for project
Run command 'pip install -r path/to/requirements_file' or 'pip3 install -r path/to/requirements_file'

___________________________________________________________________________________________________________________________________________________________________________________________________________________________

### Running PostgreSQL on Docker container
The docker-compose.yaml file is used to set the project database as a container, with mapping to the graphical user interface (set to localhost 8080).
Before running the file, you should set environment variables to configure the connection to the database.
This can be done easily in PyCharm:

example configuration

![conifg](https://user-images.githubusercontent.com/76202883/163683358-0e2dffd2-f66e-4816-a41b-9d9608717c5c.png)

example environment variables

![env](https://user-images.githubusercontent.com/76202883/163683363-7a06efd2-461f-4056-b521-5e53d86b7d58.png)

A database running on a Docker container has configured backup folder (if the container shut down all data disappear)
to set the volume that stores data on your local machine set the 'WORKING_DIR' env variable then all future containers will start
with data stored locally without any data loss.

#### First launch

If this is first time running database you have to create testing table. To do that 
go to 'localhost:8080' (GUI of database should appear). Then create table 'Testing' with two fields 'id' -> auto increment
and 'desc' -> accept NULL. Insert two records into table:
1. record with desc = 'ConfigTest' 
2. record with desc = 'DevelopmentTest'

This table will be used for possibly checking the connection to the database and simplifying debugging
when some issues occur.

___________________________________________________________________________________________________________________________________________________________________________________________________________________________

### Running arq_service_tests locally
Before running tests locally the connection with database has to be established, and
few environment variables has to be set:
* POSTGRES_USER = use same env as in docker-compose configuration
* POSTGRES_PASSWORD = use same env as in docker-compose configuration
* POSTGRES_DB = use same env as in docker-compose configuration
* HOST = localhost

Right-click on the 'arq_service_tests' package and choose 'Run arq_service_tests',
making sure the docker container is running. For this run command 'docker ps' or check-in
Docker desktop:

![dock](https://user-images.githubusercontent.com/76202883/163683798-f6b38c25-e10b-4096-a60f-af851176658c.png)

Test status after the successfully configured environment

![test](https://user-images.githubusercontent.com/76202883/163683799-3f68a774-932f-4df1-8748-139582febee1.png)

___________________________________________________________________________________________________________________________________________________________________________________________________________________________

