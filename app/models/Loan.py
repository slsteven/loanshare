""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Loan(Model):
    def a__init__(self):
        super(Loan, self).__init__()

    def validate_reg(self,user):
        errors = []
        ##### Name Validation #####
        if not user['name']:
            errors.append('Name cannot be blank')
        elif len(user['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        ##### Email Validation #####
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid!')
        ##### PW Validation #####    
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['pw_confirm']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            #encrypt password with bcrypt
            pw_hash = self.bcrypt.generate_password_hash(user['password'])
            # insert form info into DB
            
            self.db.query_db("INSERT INTO `tasks`.`users` (`name`, `email`, `password`, `birthday`,`created_at`) VALUES ('{}', '{}','{}', '{}', NOW())".format(user['name'],user['email'],pw_hash,user['birthday']))
            return {'status':True}

    def validate_login(self,user):
        #query DB for matching email
        user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(user['email'])
        validate = self.db.query_db(user_query)
        #Check for email/pw match using bcrypt check_pw method
        if validate == []:
            return {'status': False}
        elif self.bcrypt.check_password_hash(validate[0]['password'],user['password']):
            return {'status': True, 'user': validate}
        else:
            return {'status': False}
