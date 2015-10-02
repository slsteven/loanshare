from system.core.controller import *
import twilio
import smtplib
from twilio.rest import TwilioRestClient

account_sid = "AC5557801c4252c083b249d35b5fbef374"
auth_token  = "3ee0d202fb03d4d0b341be99c1c19312"
client = TwilioRestClient(account_sid, auth_token)



class Loans(Controller):
    def __init__(self, action):
        super(Loans, self).__init__(action)
        self.load_model('Loan')
    def index(self):
        # return self.load_view('index.html')
        return self.load_view('home.html')


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

            print phone_number
            phone_txt = "+1" + phone_number
            print phone_txt

            message = client.messages.create(body="Welcome to BORROW, " + new_user['first_name'] +"!",
                to= phone_txt,    # Replace with your phone number
                from_="+12173546021") # Replace with your Twilio number
            print message.sid


            TO = new_user['email']
            SUBJECT = 'WELCOME'
            TEXT ='Welcome to BORROW, ' + new_user['first_name'] + "!"

            gmail_sender   = 'loanshare.dojo@gmail.com'
            gmail_passwd = 'Codingdojo1!'

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo
            server.login(gmail_sender,gmail_passwd)


            BODY = '\r\n'.join([
                "TO: %s" % TO,
                'FROM: %s' % gmail_sender,
                'SUBJECT: %s' % SUBJECT,
                '',
                TEXT
                ])

            try:
                server.sendmail(gmail_sender,[TO], BODY)
                print 'email sent'

            except:
                print 'error sending email'


            server.quit()            

        else:
            for message in validate['errors']:
                flash(message)
        return redirect('/')

    def login(self):
        user_info={
            'log_email':request.form['log_email'],
            'log_pw':request.form['log_pw']
        }
        print "testing login"

        validate = self.models['Loan'].validate_login(user_info)

        if validate['status']:
            session['id'] = validate['user'][0]['id']
            return redirect('/users/dashboard')
        else:
            flash('Login information was incorrect. Please try again')
            return redirect('/')

    def user_login(self):
        return self.load_view('login.html')

    def show_dashboard(self):
        if not 'id' in session:
            flash("You must be logged in to view this page")
            return redirect('/')
        user_info = self.models['Loan'].get_user_info(session['id'])

        #check if user is a lender or borrower and renders information accordingly
        if user_info[0]['account_type'] == "1":
            loan_info = self.models['Loan'].lender_table_info(session['id'])
     
            session['account_type'] = "Lender"


        elif user_info[0]['account_type'] == "2":
            loan_info = self.models['Loan'].borrower_table_info(session['id'])

            session['account_type'] = "Borrower"


        #Checks if user already has loans
        check = self.models['Loan'].loan_check(session['id'],session['account_type'])
        
        if check:
            active_loan = self.models['Loan'].ledger(loan_info)
            if active_loan['status']:
                return self.load_view("dashboard.html",loan_info = loan_info,user=user_info[0],ledger=active_loan['ledger'])
            else:
                return self.load_view("dashboard.html",loan_info = loan_info,user=user_info[0])
        else:
            return self.load_view("dashboard.html",user=user_info[0])


    def logout(self):
        session.clear()
        flash("You have successfully logged out")
        return redirect('/')
    ######SHOWS LOAN ON SHOW.HTML##########
    def show_loan(self,loan_id):
        loan_info = self.models['Loan'].get_loan_info(loan_id)
        user_info = self.models['Loan'].get_user_info(session['id'])


        # return self.load_view("show.html")
        if user_info[0]['account_type'] == "1":
            #user is a lender
            return self.load_view("show.html",loan=loan_info[0],user=user_info[0], lender = True)
        elif user_info[0]['account_type'] == "2":
            #user is a borrower
            lender_query = self.models['Loan'].borrower_table_info(session['id'])
            lender_info = self.models['Loan'].get_user_info(lender_query[0]['lender_id'])

            return self.load_view("show.html",loan=loan_info[0],user=user_info[0],lender=lender_info[0])



    def accepted_loan(self,id):
        self.models['Loan'].accept_loan(id)
        return redirect ("/users/dashboard")


    def new_loan(self):
        if 'old_info' in session:
            return self.load_view('load_new.html', info = session['old_info'][0])
        else:
            return self.load_view('loan_new.html')


    def create_loan(self):
        passed_info = {
        'title' : request.form['name_loan'],
        'amount':request.form['amount_loan'],
        'interest': request.form['interest_loan'],
        'term': request.form['term'],
        'start': request.form['start'],
        'to_email': request.form['person_to_email'],
        'user_id': session['id']
        }
        
        validate = self.models['Loan'].new_loan(session['id'],passed_info)
        if validate:
            return redirect('/users/dashboard')
        else:
            flash(validate['message'])
            return redirect("/users/get_loan")

    def accept_loan(self,loan_id):
        self.models['Loan'].accept_loan(loan_id)
        flash("Congratualations! You've accepted your loan")
        return redirect('/users/dashboard')

    def adjust_loan(self,loan_id):
        self.models['Loan'].adjust_loan(loan_id)
        loan_info = self.models['Loan'].get_loan_info(loan_id)
        email_to_grab = self.models['Loan'].get_borrower_email(loan_id)
        print loan_info
        if session['account_type'] == "Lender":
            email_for_form = email_to_grab[0]['borrowers_email']
        elif session['account_type'] == "Borrower":
            print "in elif"
            email_for_form = email_to_grab[0]['lenders_email']

        return self.load_view("counter.html", info = loan_info[0], email = email_for_form)

    # def counter_offer(self,oldinfo):
    #     old_loan_info = self.models['Loan'].get_loan_info(oldinfo)
    #     borrower_email = self.models['Loan'].get_borrower_email(oldinfo)
    #     #self.models['Loan'].counter(old_loan_info)
    #     return self.load_view("counter.html", oldinfo = old_loan_info, oldemail = borrower_email)



