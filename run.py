#start
from bloggitApplication import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000,debug=True)
    # If host != '0.0.0.0', the server is not accessible from a remote host !!
    # In other words, if host = '0.0.0.0', the server is avilable on localhost only !! 
