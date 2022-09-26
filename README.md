# RecípyFind

## Authors
[Geertheihan Elamurugan](https://gitlab.stud.idi.ntnu.no/geerthee)

[Simen Masdal](https://gitlab.stud.idi.ntnu.no/simenmas)

[Mats Undseth](https://gitlab.stud.idi.ntnu.no/matsun)

[Ida Bjørn-Hansen Ahlsand](https://gitlab.stud.idi.ntnu.no/ibahlsan)

[Hanna Meland Vestvik](https://gitlab.stud.idi.ntnu.no/hannamve)

[Tuva Langedal Djupvik](https://gitlab.stud.idi.ntnu.no/tuvald)

[Frank William Daniels](https://gitlab.stud.idi.ntnu.no/frankwd)


## Description
RecìpyFind's goal is to make cooking exciting and grocery shopping easy.

With RecìpyFind discovering new dishes and purchasing the ingredients has never been more simple. 

This application allows the user to browse a world of community contributed recipes and easily share favorites with friends in this online cook book.

Any user feeling up to the task can also contribute their own secret recipe and watch it's popularity rise to the top!


## Setup


##### Dependencies
To install dependencies `pip install -r requirements.txt` 

##### Navigate terminal
Navigate the terminal to the folder `recipyFind/recipyFind` in this project, containing the `manage.py` file and install all dependencies before attempting to run the application.

##### Migrate database
To set up the database on your local host run the following command:
`python manage.py migrate`

##### Populate databse

`python manage.py loaddata initial.json` Which populates according to the initial.json file in this repository

##### Run server
Run the server with the folloring command: `python manage.py runserver`

##### Users
You can now create your own user or, if desired log in with the admin user provided with the initial data:
`username: admin` and `password: admin` 

With the provided admin user, the admin page: http://localhost:8000/admin/ is accessible.

For the other users provided:

`username: Alice, password: password` and
`username: Bob, password: password`

##### Developer commands
In case it is necessary to clear the database content: 
`python manage.py flush`

to run all tests:
`python manage.py test`

To teste a single function inside a testing class:
`python manage.py test main.tests.tests_views.TestViewsPOST`