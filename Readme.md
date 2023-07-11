Fetch Rewards Data Engineering Take Home

This readme provides instructions for setting up and testing the  Fetch Rewards - Data Engineering Takehome application locally. 

Prerequisites:

Before proceeding, make sure you have the following:

The following software installed on your local machine:
Docker: Follow the installation guide specific to your operating system.
Docker Compose
AWS CLI Local: Install using the command pip install awscli-local.
PostgreSQL: Install the PostgreSQL database.
Setting up the Test Environment
To run the test environment, use the provided docker-compose YAML file. The file specifies the required Docker images with pre-baked test data (PostgreSQL and Localstack). Here's an example of the docker-compose YAML:

```
version: "3.9"
services:
  localstack:
    image: fetchdocker/data-takehome-localstack
    ports:
      - "4566:4566"
  postgres:
    image: fetchdocker/data-takehome-postgres
    ports:
      - 5432:5432
```

PostgreSQL Credentials
The PostgreSQL database in the test environment can be accessed using the following credentials:

Username: postgres
Password: postgres
Testing Local Access
To test local access and ensure everything is set up correctly, follow these steps:

1.Read a message from the queue using AWS CLI Local:
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue

2.Connect to the PostgreSQL database and verify that the table is created:

Open a terminal and run the following command and enter the password once prompted:
```
$ psql -d postgres -U postgres -p 5432 -h localhost -W
Password:
```

Once connected to the PostgreSQL database, execute the following SQL query:
```
$ postgres=# select * from user_logins;
```

This completes the setup and testing process for the Data Takehome application in the local environment.