from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()  # Load variables from .env file
# Secret key for session management
app.secret_key = os.getenv('SECRET_KEY')

# Secure mail config
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.after_request
def add_ngrok_skip_header(response):
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hire-me')
def hire():
    return render_template('hire-me.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message("New Portfolio Inquiry", recipients=[os.getenv('MAIL_USERNAME')])
        msg.body = f"From: {name} <{email}>\n\nMessage:\n{message}"
        mail.send(msg)

        flash("Thanks!", "success")
        flash("Your message has been sent successfully.", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash("Oops! Something went wrong. Please try again later.", "error")

    return redirect(url_for('index'))  # Or 'hire' if form is on /hire-me


if __name__ == '__main__':
    app.run(debug=True)
