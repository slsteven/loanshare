"""
    Sample Model File

    A Model should be in charge of communicating with the Database.
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re
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
    def new_loan(self,passed_info):
        self.db.query_db("INSERT INTO `loans` (`title`, `amount`,`interest`,`term`,`start`,created_at,updated_at) VALUES ('{}', '{}','{}','{}','{}',NOW(),NOW())".format(passed_info['title'],passed_info['amount'],passed_info['interest'],passed_info['end'],passed_info['start']))
        user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(passed_info['person_to_email'])
        validate = self.db.query_db(user_query)
        if validate:
