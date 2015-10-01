
from system.core.model import Model
import re
from system.core.controller import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class Loan(Model):
    def a__init__(self):
        super(Loan, self).__init__()

    def validate_reg(self,user):
        errors = []
        ##### Name Validation #####
        if not user['first_name'] or not user['last_name']:
            errors.append('Name cannot be blank')
        elif len(user['first_name']) < 2 or len(user['last_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        ##### Email Validation #####
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid!')
        ##### Phone Validation #####
        if not user['phone']:
            errors.append('Phone cannot be empty')
        ##### PW Validation #####
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['password_confirm']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {"status": False, "errors": errors}
        else:

            #encrypt password with bcrypt
            pw_hash = self.bcrypt.generate_password_hash(user['password'])
            # insert form info into DB
            self.db.query_db("INSERT INTO `users` (`first`, `last`,`email`,`password`,`phone`,`account_type`,created_at,updated_at) VALUES ('{}', '{}','{}','{}','{}','{}',NOW(),NOW())".format(user['first_name'],user['last_name'],user['email'],pw_hash,user['phone'],user['acct_type']))

            return {'status':True}

    def validate_login(self,user):
        #query DB for matching email
        user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(user['log_email'])
        validate = self.db.query_db(user_query)
        #Check for email/pw match using bcrypt check_pw method
        if validate == []:
            return {'status': False}
        elif self.bcrypt.check_password_hash(validate[0]['password'],user['log_pw']):
            return {'status': True, 'user': validate}
        else:
            return {'status': False}

### this is the new loan method it checks to see if the user is in the databases
    def new_loan(self,passed_info):
        user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(passed_info['to_email'])
        validate = self.db.query_db(user_query)
        if validate == []:
            # right now theres no way to hold the loan id info so just tell the user that the other user must have a registered account
            # in order to successfuly petition the loan
            print "there is no user by that email"
        else:
            print "IF WE GOT HERE THEN WE FOUND THE EMAIL OF THE PERSON WE WANT TO SEND THE LOAN OFFER TO"
            # inserting into loans table all of the user passed information
            self.db.query_db("INSERT INTO `loans` (`title`, `amount`,`intrest`,`term`,`start`,created_at,updated_at) VALUES ('{}', '{}','{}','{}','{}',NOW(),NOW())".format(passed_info['title'],passed_info['amount'],passed_info['interest'],passed_info['end'],passed_info['start']))
            # creating a var that gathers all the info of the potential lender by querying the db for the user inserted email
            info_of_lender = self.db.query_db("SELECT users.id, users.first, users.last FROM users WHERE email = '{}'".format(validate[0]['email']))
            #By gathering the title of the newly inserted loan we can grab the loan id and any other piece of info thats nessecery
            info_of_loan = self.db.query_db("SELECT * FROM loans WHERE title = '{}' ".format(passed_info['title']))
            # by takinf all of the newly gathered info from the above two select statments we can then correctly update the users_loans table
            # take special note that passed_info[0]['id'] is the session['id'] variable
            self.db.query_db("INSERT INTO user_loans (loan_ID , borrower_ID , lender_ID) VALUES('{}','{}','{}')".format(info_of_loan[0]['id'],passed_info['user_id'],info_of_lender[0]['id']))
            print "IF WE GOT HERE THEN WE INSERT AND SELECTED ALL MYSQL QUERIES SUCCESFULLY"
        return

    def get_user_info(self,id):
        return self.db.query_db("SELECT * FROM users WHERE id = {}".format(id))

    #Retrieves loans for borrowers
    def get_borrower_loans(self,id):
        query = "SELECT users.first AS borrower, users2.first AS lender FROM users LEFT JOIN user_loans ON users.id = user_loans.lender_id LEFT JOIN users AS users2 ON users2.id = user_loans.borrower_id WHERE users.id = {}".format(id)
        return self.db.query_db(query)
