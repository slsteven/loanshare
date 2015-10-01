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
        user = self.db.query_db ("SELECT * FROM users ORDER BY id DESC LIMIT 1")
        print user['phone']

        message = client.messages.create(body="You registered",
            to="+12172550662",    # Replace with your phone number
            from_="+12173546021") # Replace with your Twilio number
        print message.sid
        return self.load_view('index.html')

    def new_user(self):
        phone_number = []

        for x in request.form['reg_phone']:
            phone_number.append(x)
        
        phone_number.pop(0)
        phone_number.pop(3)
        phone_number.pop(6)
        phone_number = ''.join(phone_number)
      

        new_user={
            "first_name":request.form['reg_first'],
            "last_name":request.form['reg_last'],
            "email":request.form['reg_email'],
            "phone":phone_number,
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

















