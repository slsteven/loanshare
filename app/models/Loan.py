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


    def get_user_info(self,id):
        return self.db.query_db("SELECT * FROM users WHERE id = {}".format(id))

    #Retrieves loans for borrowers
    def get_loans(self,id):
        user_query = self.db.query_db("SELECT users.id AS borrow_id, users2.id AS lender_id, users.first AS borrower,  users2.first AS lender, users.email AS borrow_email, users2.email AS lender_email FROM users LEFT JOIN user_loans ON users.id = user_loans.lender_id LEFT JOIN users AS users2 ON users2.id = user_loans.borrower_id WHERE users.id = {}".format(id))
        print user_query

        # loan_query = self.db.query_db("SELECT * FROM loans WHERE user_loans.lender_id = {} AND user_loans.borrower_id = {}".format(user_query[0]['lender'],user_query[0]['borrower']))

        # print loan_query

        #info being returned:
        #[{'lender_email': None, 'borrow_email': 'chungkyd@gmail.com', 'lender': None, 'borrow_id': 1, 'borrower': 'Darrick', 'lender_id': None}]
        return user_query













