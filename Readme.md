# Budget Calculator - Third Milestone Project

[View my project](https://budgetcalculator-thirdproject.herokuapp.com)

This website was made as my second Milestone project at [Code Institute](https://codeinstitute.net/).
My goal with this web application is to create a Budget calculator. With the use of the application we can register ourselves
and log in with using cookie session. The password is stored encrypted to increase the users security.

## UX

Everything about UX

### Mockup

- Adobe XD:
    - Adobe XD is a vector-based user experience design tool for web apps and mobile apps, developed and published by Adobe Inc.
    - [Wiremock link](https://xd.adobe.com/view/575c63b2-9432-4562-6bb7-837708d73534-216d/)

### User Stories

#### Sign Up
#### Log In
#### Log out

## Features

Demo page where I test the features from Data Centric Development lecture and copied my code to here:
[link](https://github.com/IstvanGercsak/PythonAndMySQLPractice)

### Existing Features

- Responsive web application
- Sign up with user
- Login up with user
- Logout with user
- Cookie session handling 
    - Login:
        - Create active cookie session 
    - Logout:
        - Delete active cookie session
- Store data in Database
- Encrypt password and store it in database
- Decrypt encrypted password from database
- Summarize Balance
- Summarize each groups
- Summarize Sub items
- Add new group
- Edit existing group
- Remove Existing group
- Add new sub item
- Edit existing sub item
- Remove Existing sub item
- Charts
- Uniqueness
    - Unique username
    - Unique group name 

### Features Left to Implement



## Technologies Used

- [HTML5](https://www.w3.org/html/)
    - Hypertext Markup Language is the standard markup language for creating web pages and web applications.
- [CSS3](https://www.w3.org/Style/CSS/)
    - Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a 
    markup language like HTML.
- [BootStrap 4.3.1](https://getbootstrap.com/docs/3.3/)
    - Front End Framework for developing responsive websites.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
    - JavaScript is a lightweight interpreted or just-in-time compiled programming language with first-class functions. While it is most well-known as the scripting language for Web pages.
- [JQuery 3.4.1](https://jquery.com)
    - The project uses to simplify DOM manipulation.
- [Git](https://git-scm.com/)
    - Git is a distributed version-control system for tracking changes in source code during software development.
- [GitHub](https://github.com/)
    -  GitHub Inc. is a web-based hosting service for version control using Git.
- [Flask](https://palletsprojects.com/p/flask/)
    - Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions
- [Python](https://www.python.org/)
    - Python is an interpreted, high-level, general-purpose programming language
- [Heroku](https://www.heroku.com/)
    - Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud
- [MySQL server](https://www.mysql.com/)
    -  MySQL is an Oracle-backed open source relational database management system (RDBMS) based on Structured Query Language (SQL)
- [Jinja2](https://palletsprojects.com/p/jinja/)
    - Jinja is a web template engine for the Python programming language. Jinja2 is a modern and designer-friendly templating language for Python, modelled after Django's templates.

## Testing

You can find the testing document in the [Testing.md](https://github.com/IstvanGercsak/BudgetCalculator-ThirdMileStoneProject/blob/master/Testing.md) file.


## Deployment

How I implement this project:

Firstly I built the basic functionality one of my private repository until I get the first working version of website. 
After this I copied the code snippets in this public repository, and explained the actual small pieces of the commits in the commit comment section.

- **Set up**:
    - I use local IDE for create the project, I installed the Git locally and synchronized my local IDE 
    with the local git. I use IntelliJ Pycharm for the front end development with its helpful built in deployment tools. 
    After I created a Git and GitHub repository, I could start to work and I could test my features locally.
    I could see my changes locally to open my index.html file with the View/Open browser menu option in my local IDE.
    Here I could choose the required browser which I want to use. (Chrome, Mozilla, etc.)
- **Commits**:
    - After every small piece and increment, I made commit to my local Git repository. After that in the end of the 
    bigger section that gives value to my project I pushed my modification to my online GitHub repository.
    - For the development I only use one branch called "master".
- **Local and online deployment**
    - Locally: It is very easy to clone repository from my account if you follow these steps:
        1. Follow this link [Project GitHub repository]() 
        2. Under the repository name, click "Clone or download".
        3. Here you have to copy the url's of the repository
        4. In your local IDE you can choose to create new project from version control/Git 
        5. Paste the link there that you copied before
        6. For additional help you can more information under this [link](https://help.github.com/en/articles/cloning-a-repository)
    - Online: (Need to expand)
        1. I used heroku:
        2. Create project
        3. Choose github project that is connected to Heroku
        4. Set the deployment to Autodeploy so after every commit there will be a new deployment into Heroku.
        5. Create requirements.txt file:
        6. pip freeze > requirements.txt