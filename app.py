from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

# Load the dataset
data = pd.read_csv("testpcosval.csv")
X = data.drop(columns=['PCOS (Y/N)'])
y = data['PCOS (Y/N)']

# Train the model
model = GradientBoostingClassifier()
model.fit(X, y)

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid user')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

# Main application routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input values from the form
        age = int(request.form['Age (yrs)'])
        weight = float(request.form['Weight (Kg)'])
        height = float(request.form['Height(Cm)'])
        bmi = float(request.form['BMI'])
        blood_group = int(request.form['Blood Group'])
        pulse_rate = int(request.form['Pulse rate(bpm)'])
        rr = int(request.form['RR (breaths/min)'])
        hb = float(request.form['Hb(g/dl)'])
        cycle_r_i = int(request.form['Cycle(R/I)'])
        cycle_length = int(request.form['Cycle length(days)'])
        pregnant = int(request.form['Pregnant(Y/N)'])
        abortions = int(request.form['No. of abortions'])
        hip = int(request.form['Hip(inch)'])
        waist = int(request.form['Waist(inch)'])
        rbs = float(request.form['RBS(mg/dl)'])
        weight_gain = int(request.form['Weight gain(Y/N)'])
        hair_growth = int(request.form['hair growth(Y/N)'])
        skin_darkening = int(request.form['Skin darkening (Y/N)'])
        hair_loss = int(request.form['Hair loss(Y/N)'])
        pimples = int(request.form['Pimples(Y/N)'])
        reg_exercise = int(request.form['Reg.Exercise(Y/N)'])
        bp_systolic = int(request.form['BP _Systolic (mmHg)'])
        bp_diastolic = int(request.form['BP _Diastolic (mmHg)'])
        follicle_no_l = int(request.form['Follicle No. (L)'])
        follicle_no_r = int(request.form['Follicle No. (R)'])
        avg_f_size_l = float(request.form['Avg. F size (L) (mm)'])
        avg_f_size_r = float(request.form['Avg. F size (R) (mm)'])
        endometrium = float(request.form['Endometrium (mm)'])

        # Predict PCOS
        prediction = model.predict([[age, weight, height, bmi, blood_group, pulse_rate, rr, hb, cycle_r_i, cycle_length, pregnant, abortions, hip, waist, rbs, weight_gain, hair_growth, skin_darkening, hair_loss, pimples, reg_exercise, bp_systolic, bp_diastolic, follicle_no_l, follicle_no_r, avg_f_size_l, avg_f_size_r, endometrium]])

        # Render the result template with the prediction
        prediction_text = "Yes" if prediction[0] == 1 else "No"
        return render_template('result.html', prediction=prediction_text)

@app.route('/index')
def index():
    if 'name' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('index.html', user=user)
    return redirect(url_for('login'))

@app.route('/prevention')
def prevention():
    return render_template('prevention.html')

@app.route('/diet')
def diet():
    return render_template('diet.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/base')
def base():
    return render_template('base.html')




@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['message']
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
