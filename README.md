# point72_test
Solution to the Point72 test project.

Function: 
- Allow users to register/login to site
- users have admin or regular privileges
- admins can update and deleter users in the database
- both types of users can see the user database and filter by Age, Name, E-Mail, and Country


### Running the Web App "Server":

In order for the Web Application to be "live" the main.py file needs to be executed.

This is done by navigating with the command line to the point72_test folder and executing the main.py file in the python3 environment.
```
$ python3 main.py
```

The Web Application will be available on http://127.0.0.1:8080/ .

### Web App usage:

#### Login Page
When accesing the http://127.0.0.1:8080/ page, the login page will be rendered.

The login page allows the user to login, if he has registered before.
Alternatively, if he hasn't registered, there is a "register" button redirecting to the registration page.

#### Registration Page
Can only be rendered after redirection from login page.

Allows for registration of a new user, who will now be able to log in, as well as be available in the database of the web app.

#### Home Page

