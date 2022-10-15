import flask
import firebase, db from firebase

def create_app():
    app = flask.Flask(__name__)
    @app.route('/home')
    def home():
        return 'Welcome to Pairitas'
    @app.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                data = {"password": password, "sleep", "noise": 0, "roommate_num": 0, "phil_response": 0}
                db.child("users").child(username).set(data)

            flash(error)

        return render_template('auth/register.html')
    @bp.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            users = db.child("users")

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

        return render_template('auth/login.html')

