from flask import Flask, flash, abort, make_response, redirect, session, url_for, render_template, request
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = b'411eb23ed1367722ef878dbaadf87a55e30e67b5cbd0930c71358f919214eb43'


@app.route("/")
def index():
    return "<p>Hello, me!</p>"


@app.route("/<name>")
def show_name(name):
    return f"Hello, {escape(name)}!"


@app.route('/user/<username>')
def show_username(username):
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {escape(subpath)}'


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.get('/login')
def login_get():
    return 'show_the_login_form()'


@app.post('/login')
def login_post():
    return 'do_the_login()'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login-form', methods=['POST', 'GET'])
def login2():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


def valid_login(username, password):
    if username == 'admin' and password == 'pass':
        return True
    return False


def log_the_user_in(username):
    return f'Welcome {escape(username)}'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file2']
        filename = f"/tmp/{secure_filename(file.filename)}"
        file.save(filename)
        return filename


@app.route('/cookie')
def cookie():
    username = request.cookies.get('username')
    resp = make_response(render_template('cookie.html'))
    resp.set_cookie('username', f'received {username}')
    return resp


@app.route('/redirect-hello')
def redirect_hello():
    return redirect(url_for('hello'))


@app.route('/abort')
def abort_me():
    abort(401)
    this_is_never_executed()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/user_image")
def user_image():
    return ''


@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user['username'],
        "theme": user['theme'],
        "image": url_for("user_image", filename=user['image']),
    }


def get_current_user():
    return {'username': 'asdf', 'theme': 'dark', 'image': 'asdf.png'}


@app.route("/users")
def users_api():
    users = get_all_users()
    return users


def get_all_users():
    return [{'username': 'asdf', 'theme': 'dark', 'image': 'asdf.png'}]


app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')


@app.route('/session-check')
def session_check():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'


@app.route('/session-update', methods=['GET', 'POST'])
def session_update():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/session-destroy')
def session_destroy():
    session.pop('username', None)
    return redirect(url_for('index'))


counter = 0


@app.route('/flash')
def flash_req():
    global counter
    counter += 1
    if counter % 2 == 0:
        flash(f'{counter}')
    return render_template('flash.html', counter=counter)

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('show_name', name='Doe Doe'))
#     print(url_for('about', next='/'))
#     print(url_for('show_username', username='John Doe'))
