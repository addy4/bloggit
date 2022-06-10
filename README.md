# bloggit
A web application for reading and writing blogs and thus, sharing your thoughts with public on any topic of your interest. 

#### Features
- APIs for registration, login.
- User sessions.
- Authentication via email in case password has been forgotten.
- Users can read blogs
- Bloggers can post content once provided write permissions by admin (user has to drop a mail to admin for permission)

#### What went in creating this ?
- Python3 : Flask, SQLAlchemy, SMTP, LoginManager (for user sessions), Bcrypt (for password encryption) etc.
- SQLite
- HTML, Bootstrap, CSS

> NOTE : In bloggitApplication/keys.py provide your email ID and password to make the password reset APIs work correctly.

#### Front-End (UI/UX)
![alt text](https://github.com/addy4/bloggit/blob/main/bloggitApplication/ui-images/registeration.png?raw=true "Registeration")
