
# Lazy_coder

Lazy Coder Blog, built using the Django framework, is a dynamic web application designed to provide a platform for coding enthusiasts to explore a variety of topics, share their knowledge, and engage with a vibrant community. With a focus on productivity and convenience, Lazy Coder Blog offers a range of features to enhance the blogging experience.

## What It Does:

- #### Multi-category Blogging: 
Lazy Coder Blog allows users to create and publish blog posts across various categories, covering topics such as programming languages, frameworks, productivity hacks, coding challenges, and more. It's a one-stop destination for coders seeking valuable insights and practical advice.

- #### User Authentication: 
Users can easily sign up and create their accounts, gaining access to personalized features and a tailored experience within the blog. Sign-in functionality ensures a secure and seamless user experience.

- #### User Notifications: 
Every time a user signs up, an email notification is sent to welcome them aboard. It's a small touch that fosters a sense of community and engagement.

- #### Interactive Commenting:
Users can like, dislike, and comment on blog posts, promoting meaningful discussions and exchanging ideas. Additionally, comment management allows users to delete their comments, maintaining control over their contributions.

- #### Intuitive User Interface:
Lazy Coder Blog boasts an intuitive and user-friendly interface, ensuring easy navigation and an enjoyable browsing experience for readers and contributors alike.




## Features

- Live previews.
- Fullscreen mode.
- Cross platform.
- User Authentication.
- Posts can be Created Updated and Deleted.
- Comments can be Deleted either the Author of Post or the User who commented.
- Profile can be updated deleted along with images.
- Old imaged will be deleted from DB when user updates to a new Profile picture.
- All blog Post page is paginated.
- Fully Responsive UI.
- Postgre  is used at backend as DB.
- any more more features, discover them yourself.



## Demo
You see, i highly encourage the visitors to got to the [Site](https://lazycoder-production.up.railway.app/) and take live demo of Lazy_coder, but still i am attaching a Screenshot.

![image](https://github.com/fadingreality1/Lazy_coder/assets/114291201/ad259467-4ead-42ef-813e-e8ee6948f8fa)

hope you may find it worthy of one visit.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`

`DEBUG` 

`EMAIL_HOST`

`EMAIL_PORT`

`EMAIL_HOST_USER`

`EMAIL_HOST_PASSWORD`

The below varibale needs to be setup only when you are using some other database instead of sqlite3.
setup for sqlite3 is in master branch

`DB_PASS`

`DB_PORT`

`DB_HOST`

`DB_USER`

`DB_NAME`

`DB_URL`


## Run Locally

To deploy this project, you will need to create a folder of your choice and clone this repository (only master branch)

the process is as follows:-

- First, clone the master branch.
```bash
git clone -b master --single-branch https://github.com/fadingreality1/Lazy_coder.git
```
This command will clone only the master branch on your local machine.

- Change your directory to where you have clone the repository.
```bash
cd project-location
```
- Install The pipenv package

```bash
pip install pipenv

```
- Install all the dependencies from pip.lock
```bash
pipenv install
```
It will automatically install all the required packages.

- Making Tables in Database
```bash
python manage.py makemigrations
``` 
after all migrations are made, run the following command
```bash
python manage.py migrate
```
with this command, a file will appear in your  project directory with extension ```.sqlite3``` which is DB for our project.
- Now create a Super user to manage the DB
```bash
python manage.py createsuperuser
```
The prompt will ask for username, email and password.
just fill'em up and remember those.
- Now we are good to go. run the following command to se your Django blog running.
```bash
python manage.py runserver
```

Your project should be running at localhost at this point.
If you encounter any error till this point, either search on google or contact me via [linkedin](https://www.linkedin.com/in/kunalvermait/) or [email](kunalverma.learn@gmail.com). I will be happy to help you out.


## Lessons Learned

During the development of the Lazy Coder project, I gained valuable knowledge and skills in various areas. Here's a summary of what I learned:

- Django: Through working on this project, I deepened my understanding of the Django framework. I became proficient in leveraging Django's powerful features, such as URL routing, template rendering, and handling HTTP requests and responses.
- Sending Emails with Django: I learned how to implement email functionality using Django's built-in email sending capabilities. This allowed me to send welcome emails to new users upon signup and incorporate email notifications into the application.

- Database Setup: I acquired knowledge on configuring and managing databases within the Django framework. This involved setting up database connections, defining models and relationships, and executing database migrations to ensure data integrity.

- Deployment of Django Apps: I learned how to deploy Django applications on live servers, making them accessible to users. This encompassed configuring server environments, managing dependencies, and ensuring proper deployment procedures for a smooth user experience.

- Bug Fixing and Exception Handling: Throughout the development process, I encountered and resolved various bugs and exceptions. This allowed me to develop effective debugging techniques and learn how to handle errors gracefully, ensuring the stability and reliability of the application.

- Functional Views in Django: I gained an understanding of functional views in Django, which allowed me to create dynamic and interactive web pages. I learned how to handle form submissions, process user input, and render appropriate responses using functional views.

- Model Forms: I explored Django's model forms, enabling me to generate forms based on database models effortlessly. This streamlined the creation of forms, form validation, and data handling, enhancing the user experience in data submission and retrieval.

- Customizing User Model and Forms: I delved into customizing the User model and forms provided by Django's authentication system. This enabled me to tailor the user registration and authentication process to the specific requirements of the Lazy Coder project.

## Tech Stack

**Client:** HTML, CSS, JS, DJANGO TEMPLATE

**Server:** Django

**Database:** Postgre for deployment, sqlite3 for local development


## Acknowledgements

 - [Style Shout](https://styleshout.com/) for their amazing template which i used as base for this Webapp.
 - [Corey Schafer](https://www.youtube.com/@coreyms) for amazing Django tutorial which helped me alot to learn Django.
- [readme.so](readme.so) for this amazing readme builder which helped me a lot.

## Authors

- [@KunalVerma](https://github.com/fadingreality1)

