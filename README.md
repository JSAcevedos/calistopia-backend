# Calistopia
Calistopia web


To run the app, you will need to have Docker Compose installed. Once you have Docker Compose installed, you can follow these steps:

Clone the GitHub repository to your local machine.
Navigate to the directory containing the Docker Compose file.
Run the following command:

```
$ docker-compose up -d
```

The first time you run the app, an error may appear due to the permissions that the folder "postgres-data" may have. First try to stop the containers and run them again to fix this, if this does not works, give all permissions to your current user and run the last command again.

This will start the app in a container and expose port 8000 to the host machine. You can then access the app at http://localhost:8000.

Additional tips:

If you are using a custom Docker image, you may need to pull the image from the public registry before running docker-compose up -d.
If you are using a database, you may need to create the database and configure the app to use it.
You can view the logs for the app by running the following command:

```
$ docker-compose logs -f
```

To stop the app, you can run the following command:

```
$ docker-compose down
```

This will stop the container and remove it.

Troubleshooting:

If you are having trouble running the app, here are a few things to try:

Make sure that Docker Compose is installed and running.
Make sure that you have pulled the Docker image from the public registry (if you are using a custom image).
Check the logs for the app for any errors.

Try restarting the app by running 

```
$ docker-compose down
```

and then 

```
$ docker-compose up -d again.
```

If you are still having trouble running the app, please create a new issue on the GitHub repository.

Add changes

If you'd like to add a dependency, you can add it in the requirements.txt file and run the following changes to apply changes.

```
$ docker-compose up --build
```
