"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Loans(Controller):
    def __init__(self, action):
        super(Loans, self).__init__(action)
        self.load_model('Loan')
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """
        A loaded model is accessible through the models attribute
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('index.html')

    def new_user(self):
        new_user={
            "first_name":request.form['reg_first'],
            "last_name":request.form['reg_last'],
            "email":request.form['reg_email'],
            "phone":request.form['reg_phone'],
            "acct_type":request.form['acct_type'],
            "password":request.form['reg_pw'],
            "password_confirm":request.form['reg_pw_confirm']
        }

        validate = self.models['Loan'].validate_reg(new_user);

        if validate['status']:
            flash('You have successfully registered!')
        else:
            for message in validate['errors']:
                flash(message)
        return redirect('/')

    def login(self):
        user_info={
            'log_email':request.form['log_email'],
            'log_pw':request.form['log_pw']
        }

        validate = self.models['Loan'].validate_login(user_info)
        print validate
        if validate['status']:
            session['id'] = validate['user'][0]['id']
            return redirect('/users/dashboard')
        else:
            flash('Login information was incorrect. Please try again')
            return redirect('/')

    def show_dashboard(self):
        return self.load_view("dashboard.html")

    def logout(self):
        session.clear()
        flash("You have successfully logged out")
        return redirect('/')

    def new_loan(self):
        return self.load_view('loan_new.html')

    def create_loan(self):
        passed_info = {
        'title' : request.form['name_loan'],
        'amount':request.form['amount_loan'],
        'interest': request.form['interest_loan'],
        'start': request.form['start'],
        'end': request.form['end'],
        'to_email': request.form['person_to_email']
        }
        self.load_models['Loan'].new_loan(passed_info)
