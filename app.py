from flask import Flask, render_template, request, redirect, url_for, Markup, \
    flash  # Imports Flask and all required modules
import databasemanager  # Provides the functionality to load stuff from the database

app = Flask(__name__)
import errormanager  # Enum for types of errors

# DECLARE datamanager as TYPE: databasemanager
datamanager = databasemanager

# DECLARE errorman as TYPE: errormanager
errorman = errormanager

# DECLARE Current User as string
# Provides a means of the application knowing who is signed in
CurrentUser: str


# Route function for homepage.
# @return Returns render template of base.hmtl
@app.route('/')
def Home():
    datamanager.LoadContent()
    return render_template('base.html', entries=datamanager.entries, bFailure=False, app=datamanager)

# Checks the username and the password and handles any errors
# @route Homepage
# @method:  POST
# @return redirect: Redirect to 'AdminHome' function after successful login
# @return render_template: base.html with failure condition
@app.route('/', methods=['POST'])
def Login():
    if request.method == "POST":
        try:
            password = request.form['Password']
            username = request.form['Username']
            if (password != '') and (username != ''):
                if datamanager.CheckUser(username, password) == True:
                    global CurrentUser
                    CurrentUser = username
                    globals()
                    return redirect(url_for('AdminHome', auth=str(datamanager.Encrypt('True')), user=username))
                else:
                    Failure = errorman.EErrorType.FailedPassword
                    return render_template('base.html', fail=Failure, failenum=errorman.EErrorType,
                                           entries=datamanager.entries, bFailure=True, app=datamanager)
            else:
                Failure = errorman.EErrorType.FailedNone
                return render_template('base.html', fail=Failure, failenum=errorman.EErrorType, bFailure=True,
                                       entires=datamanager.entries, app=datamanager)
        except:
            return render_template('base.html', fail=errorman.EErrorType.FailedNone, failenum=errorman.EErrorType,
                                   bFailure=True, entries=datamanager.entries)

# Main route for admin homepage
# Checks for encrypted string to ensure access was granted
# @route: '/adminbase' <auth: encrypted string> <user: user's username>
# @param auth: Encrypted string used for security
# @param user: Username of user
# @return render_template: adminbase.html with entries, the username and the datamanager
# @return redirect: 'Home' will return the user to home if they don't have valid acsses
@app.route('/adminbase/<auth> <user>')
def AdminHome(auth, user):
    if auth == str(datamanager.Encrypt('True')):
        datamanager.LoadContent()
        print(datamanager.entries)
        return render_template('adminbase.html', entries=datamanager.entries, user=user, app=datamanager)
    else:
        return redirect(url_for('Home'))

# Gets the users inputted values for a new entry and adds them to the website
# @route: '/adminbase.html' <user: username of signed in user>
# @param user: username of the signed in user
# @return redirect: 'Admin Home' function with encryption string and username
@app.route('/adminbase.html/<user>', methods=["POST"])
def CreateNew(user: str):
    if request.method == "POST":
        # try:
        title = request.form['Title']
        desc = request.form['Desc']
        image = request.form['Image']
        caption = request.form['Caption']
        id = len(datamanager.entries)
        ind = str(id)
        datamanager.AddNewItem(title, desc, caption, image, id, ind, 0)
        return redirect(url_for('AdminHome', auth=str(datamanager.Encrypt('True')), user=user))
    # except:
    # return render_template('error.html', fail=errorman.EErrorType.FailedNone, failenum=errorman.EErrorType)

# Deprecated
#@app.route('/adminbase', methods=["POST"])
#def Delete():
    #if request.method == "POST":
     #   delete = request.form['Del']
      #  if delete == True:
       #     datamanager.RemoveItem(0)
       #     return render_template(url_for('AdminHome', auth=str(datamanager.Encrypt('True'))))
        #else:
         #   return render_template(url_for('AdminHome', auth=str(datamanager.Encrypt('True'))))

# Main route for signup page
# @route: '/signup'
# @return render_template: signup.html
@app.route('/signup')
def SignUp():
    return render_template('signup.html')

# Gets the entry input values and adds to database also handles errors
# @route '/sign' methods: GET and POST
# @return redirect: 'Home'
# @return render_template: 'error.html' with error type
@app.route('/sign', methods=["POST", "GET"])
def AddNewUser():
    try:
        if request.method == "POST":
            AdminKey = request.form['Key']
            Password = request.form['Password']
            Username = request.form['Username']
            ConfirmPass = request.form['ConfirmPassword']
            if datamanager.CheckKey(AdminKey) == True:
                if ((Password != '') and (Username != '') and (ConfirmPass != '')):
                    if ConfirmPass == Password:
                        if datamanager.NewUser(Username, Password) == True:
                            return redirect(url_for('Home'))
                    else:
                        return render_template('error.html', fail=errorman.EErrorType.FailedPassword,
                                               failenum=errorman.EErrorType)
                else:
                    return render_template('error.html', fail=errorman.EErrorType.FailedNone,
                                           failenum=errorman.EErrorType)
        return render_template('error.html')
    except:
        return render_template('error.html', fail=errorman.EErrorType.FailedNone, failenum=errorman.EErrorType)

# Deprecated
@app.route('/likes/<id>')
def Like(id: int):
    datamanager.AddLike(id)
    return redirect(url_for('Home'))

# Deprecated
@app.route('/deleteconfirm', methods=['GET'])
def ChangeDeleteTarget():
    id = request.form['Delete']
    global deletetarget
    deletetarget = id
    print(deletetarget)
    globals()
    return 'hi'  # This exists because Flask is bad


# Deprecated
@app.route('/delete')
def Delete():
    datamanager.RemoveItem(datamanager.deletetarget)
    global CurrentUser
    CurrentUser = 'user'
    return redirect(url_for('AdminHome', auth=str(datamanager.Encrypt('True')), user=CurrentUser, app=datamanager))


# Main Flask Loop
if __name__ == '__main__':
    app.secret_key = datamanager.Encrypt('key')
    app.run()
