from system.core.controller import *


class Loans(Controller):
    def __init__(self, action):
        super(Loans, self).__init__(action)
        self.load_model('Loan')
    def index(self):

        """
        A loaded model is accessible through the models attribute
        self.models['WelcomeModel'].get_all_users()
        """

        return self.load_view('index.html')

    def new_user(self):
        phone_number = []

        for x in request.form['reg_phone']:
            phone_number.append(x)

        phone_number.pop(0)
        phone_number.pop(3)
        phone_number.pop(6)
        phone_number = ''.join(phone_number)
# <<<<<<< HEAD
      
# =======





# >>>>>>> f1f1567bf03f2409694ccc69b3ac0fd3487df8c4
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
# <<<<<<< HEAD
    
# =======
#         print validate
# >>>>>>> f1f1567bf03f2409694ccc69b3ac0fd3487df8c4
        if validate['status']:
            session['id'] = validate['user'][0]['id']
            return redirect('/users/dashboard')
        else:
            flash('Login information was incorrect. Please try again')
            return redirect('/')

    def show_dashboard(self):
        if not 'id' in session:
            flash("You must be logged in to view this page")
            return redirect('/')

        user_info = self.models['Loan'].get_user_info(session['id'])
        
        self.models['Loan'].get_loans(session['id'])

        # if user_info[0].account_type == "1":
        #     pass
        # elif user_info[0].account_type == "2":
        #     pass
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
        'to_email': request.form['person_to_email'],
        'user_id': session['id']
        }
        print "GOING INTO MODEL NEW LOAN METHOD"
        self.models['Loan'].new_loan(passed_info)
        print "WE GOT PAST NEW LOAN METHOD"
        return redirect('/users/dashboard')


    def show_loan(self,id):
        return self.load_view("show.html")
