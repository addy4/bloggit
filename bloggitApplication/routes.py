import secrets
import os
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from bloggitApplication.forms import RegisterForm, LoginForm, profileUpdateForm, PostContentForm, RequestResetForm, ResetPasswordForm
from bloggitApplication.models import User, Post 
from bloggitApplication import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route('/home')
def homepg():
      page_id = request.args.get('page', 1, type=int)
      data = Post.query.order_by(Post.date_posted.desc()).paginate(page=page_id, per_page=5)
      return render_template('home.html', posts = data, title = 'Home Page') 
 
@app.route('/layout')
def basic_layout():
      return render_template('layout.html')

@app.route('/about')
def aboutInfo():
      return render_template('about.html') 

@app.route('/register', methods = ['GET', 'POST'])
def register_me(): 
      if current_user.is_authenticated:
            return redirect(url_for('homepg')) 
      Regform = RegisterForm() 
      if Regform.validate_on_submit():
            password_hashed = bcrypt.generate_password_hash(Regform.password.data).decode() 
            user_for_db = User(username=Regform.username.data, email=Regform.email.data, password=password_hashed)  
            db.session.add(user_for_db) 
            db.session.commit()   
            flash(f'Account created for {Regform.username.data}!', 'success')
            return redirect(url_for('homepg'))
      return render_template('register.html', title = 'Registeration', form_flask = Regform) 

@app.route('/login', methods = ['GET', 'POST']) 
def login_me(): 
      if current_user.is_authenticated:
            return redirect(url_for('homepg'))
      Logform = LoginForm() 
      if Logform.validate_on_submit(): 
            if checkLogin(Logform.email.data, Logform.password.data):
                  user_logger = User.query.filter_by(email=Logform.email.data).first()
                  login_user(user_logger, remember=Logform.remember.data)
                  flash('You are logged in !!', 'success') 
                  next_redirect = request.args.get('next')
                  return redirect(next_redirect) if next_redirect else redirect(url_for('homepg')) #this is a ternary condition in Py3
            else:
                  flash('Log in is unsuccessful. Please check email/password', 'danger')  
      return render_template('loginpage.html', title = 'Log In', form_flask = Logform) 


# We are making sure that a real user exists for the given email ID and password is correct! 
def checkLogin(email_id,password_string):
      log_flag = User.query.filter_by(email=email_id).first()
      if(log_flag and bcrypt.check_password_hash(log_flag.password,password_string)):
            return True 
      else:
            return False 


@app.route('/logout')
def logoutUser():
      logout_user()
      return redirect(url_for('homepg')); 

def save_pic_file(picture_file):
      hex_pattern = secrets.token_hex(8)  
      _, file_extension = os.path.splitext(picture_file.filename)
      saved_pic_file = hex_pattern + file_extension
      saved_file_path = os.path.join(app.root_path, 'static/pics', saved_pic_file)
      picture_file.save(saved_file_path)

      return saved_file_path

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def userAccount():
      print(current_user.username)
      update_form = profileUpdateForm()
      if update_form.display_pic.data:
            current_user.image_file = save_pic_file(update_form.display_pic.data)
      if update_form.validate_on_submit():
            current_user.username = update_form.username.data
            current_user.email = update_form.email.data
            db.session.commit()
            flash('Done!', 'success')
            return redirect(url_for('userAccount'))
      elif request.method == 'GET':
            update_form.username.data = current_user.username
            update_form.email.data = current_user.email
      image_profile = url_for('static', filename=f'pics/{current_user.image_file}')
      return render_template('account.html', title = 'Your Profile', profile_pic = image_profile, form_flask = update_form)

@app.route('/post/create', methods = ['GET', 'POST'])
@login_required
def create_post():
      post_form = PostContentForm()
      if current_user.permit == 0:
            flash('You are not allowed to post yet. Please write to aadhaarb4@gmail.com for the rights', 'success')
            return redirect(url_for('homepg'))
      if post_form.validate_on_submit() and current_user.permit == 1:
            post_db = Post(title=post_form.title.data, content=post_form.content.data, author=current_user)
            #current_user.posts = post_db
            db.session.add(post_db)
            db.session.commit()
            flash('Thanks for Posting!', 'success')
            return redirect(url_for('homepg'))
      return render_template('new_post.html', title = 'Post Content',legend = "What's New", form_flask = post_form)


@app.route('/post/<int:post_id>')
def postId(post_id):
      postCustom = Post.query.get_or_404(post_id)
      return render_template('custom_post.html', post_single = postCustom, title = 'Post')


@app.route('/post/<int:post_id>/update', methods= ['GET', 'POST'])
@login_required
def updatePost(post_id):
      postCustom = Post.query.get_or_404(post_id)
      if postCustom.author != current_user:
            abort(403)
      post_form = PostContentForm()
      if post_form.validate_on_submit():
            postCustom.title = post_form.title.data
            postCustom.content = post_form.content.data
            db.session.commit()
            flash('Post updated', 'success')
            return redirect(url_for('postId', post_id=postCustom.id))
      post_form.title.data = postCustom.title
      post_form.content.data = postCustom.content
      return render_template('new_post.html', title = 'Post Content', legend = 'Update Post', form_flask = post_form)


@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def deletePost(post_id):
      postCustom = Post.query.get_or_404(post_id)
      if postCustom.author != current_user:
            abort(403)
      db.session.delete(postCustom)
      db.session.commit()
      flash('Post deleted', 'success')
      return redirect(url_for('homepg'))


@app.route("/user/<string:user_name>")
def user_specific_posts(user_name):
      page_id = request.args.get('page', 1, type=int)
      user_person = User.query.filter_by(username=user_name).first_or_404()
      data = Post.query.filter_by(author=user_person).order_by(Post.date_posted.desc()).paginate(page=page_id, per_page=5)
      return render_template('userSpecificPosts.html', posts = data, title = 'Home Page', user = user_person) 

def sendResetLink(user_person):
      stoken = user_person.get_reset_token()
      msg = Message('Password Reset Request', sender = 'aadhaarb4@gmail.com', recipients = [user_person.email])
      msg.body = f'''
      To reset password, visit : 
      {url_for('resetFromLink', token=stoken, _external=True)}

      If you did not make the request, ignore this!
      '''
      mail.send(msg)

@app.route("/reset/reset_password", methods=['GET', 'POST'])
def resetPasswordreq():
      if current_user.is_authenticated:
            return redirect(url_for('homepg'))
      req_reset_form = RequestResetForm()
      if req_reset_form.validate_on_submit():
            user_person = User.query.filter_by(email=req_reset_form.email.data).first()
            print(user_person)
            if user_person is None:
                  flash('No such user', 'danger')
                  return redirect(url_for('homepg'))
            sendResetLink(user_person)
            flash('Email sent', 'success')
            return redirect(url_for('login_me'))
      return render_template('password_reset.html', title = 'Reset Password', form_flask = req_reset_form)

@app.route("/reset/reset_password/<token>", methods = ['GET', 'POST'])
def resetFromLink(token):
      if current_user.is_authenticated:
            return redirect(url_for('homepg'))
      user_person = User.verify_token(token)
      if user_person is None:
            flash('Invalid/Expired token.. please try again!', 'danger')
            return redirect(url_for('resetPasswordreq'))
      reset_password_form = ResetPasswordForm()
      if reset_password_form.validate_on_submit():
            password_hashed = bcrypt.generate_password_hash(reset_password_form.new_password.data).decode()
            user_person.password = password_hashed
            db.session.commit()
            flash('Password reset is successful', 'success')
            return redirect(url_for('login_me')) 
      return render_template('enter_new_password.html', title = 'Change Password', form_flask = reset_password_form)

#################### Helper APIs ####################

#pass user name and permit_id (permit_id = 1 -> permitted to post, permit_id = 0 -> NOT permitted to post)
#prefer using a secret key instead "give_permission" 
@app.route('/give_permission/<string:user_person>/<int:permit_id>', methods = ['GET','POST'])
def permitUser(user_person, permit_id):
      user_name = User.query.filter_by(username=user_person).first_or_404()
      user_name.permit = permit_id
      db.session.commit()
      if permit_id == 1:
            print (f'Post permission given to {user_name.username}')
      if permit_id == 0:
            print (f'Post permission NOT given to {user_name.username}')
      return redirect(url_for('homepg'))

@app.route('/personInfo_from_username/<string:user_name>')
def getPersonfromUserName(user_name):
      personIs = User.query.filter_by(username=user_name).first_or_404()
      personIsInfo = {"username":user_name, "emailid":personIs.email}
      return personIsInfo

@app.route('/personInfo_from_email/<string:email_id>')
def getPersonfromEmailId(email_id):
      personIs = User.query.filter_by(email=email_id).first_or_404()
      personIsInfo = {"username":personIs.username, "emailid":email_id}
      return personIsInfo
