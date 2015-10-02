
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
    def new_loan(self,user_id,loan):
        user_query = "SELECT * FROM users WHERE email = '{}'".format(loan['to_email'])
        validate = self.db.query_db(user_query)

        self_info =self.db.query_db("SELECT * FROM users WHERE id = '{}'".format(user_id))

        if validate == []:
            # right now theres no way to hold the loan id info so just tell the user that the other user must have a registered account
            # in order to successfuly petition the loan
            print "there is no user by that email"
            return {'status':False,'message':"Cannot find user"}
        else:
            new_loan_query = "INSERT INTO `hackathon`.`loans` (`title`, `amount`, `interest`, `term`, `start`, `status`,`created_at`,`updated_at`) VALUES ('{}','{}','{}','{}','{}','{}', NOW(),NOW())".format(loan['title'],loan['amount'],loan['interest'],loan['term'],loan['start'],"1")
            self.db.query_db(new_loan_query)

            if self_info[0]['account_type'] == "1":
                print"in if"
                ##session will be lender
                lender_query = "INSERT INTO `hackathon`.`user_loans` (`lender_id`,`borrower_id`) VALUES ('{}', '{}')".format(user_id,validate[0]['id'])
                self.db.query_db(lender_query)

            elif self_info[0]['account_type'] == "2":
                print "in elif"
                borrower_query = "INSERT INTO `hackathon`.`user_loans` (`borrower_id`,`lender_id`) VALUES ('{}', '{}')".format(user_id,validate[0]['id'])
                self.db.query_db(borrower_query)

 
            # inserting into loans table all of the user passed information
            # self.db.query_db("INSERT INTO `loans` (`title`, `amount`,`interest`,`term`,`start`,created_at,updated_at) VALUES ('{}', '{}','{}','{}','{}',NOW(),NOW())".format(passed_info['title'],passed_info['amount'],passed_info['interest'],passed_info['end'],passed_info['start']))
            # creating a var that gathers all the info of the potential lender by querying the db for the user inserted email
            # info_of_lender = self.db.query_db("SELECT users.id, users.first, users.last FROM users WHERE email = '{}'".format(validate[0]['email']))
            # print info_of_lender
            #By gathering the title of the newly inserted loan we can grab the loan id and any other piece of info thats nessecery
            # info_of_loan = self.db.query_db("SELECT * FROM loans WHERE title = '{}' ".format(loan['title']))
            # print info_of_loan
            # by takinf all of the newly gathered info from the above two select statments we can then correctly update the users_loans table
            # take special note that passed_info[0]['id'] is the session['id'] variable
            # self.db.query_db("INSERT INTO user_loans (loan_ID , borrower_ID , lender_ID) VALUES('{}','{}','{}')".format(validate[0]['id'],loan['user_id'],validate[0]['id']))
            print "IF WE GOT HERE THEN WE INSERT AND SELECTED ALL MYSQL QUERIES SUCCESFULLY"
            return {'status':True}
    def accept_loan(self, loan_id):
        query ="UPDATE `hackathon`.`loans` SET `status`='1' WHERE `id`='{}';".format(loan_id)
        return self.db.query_db(query)

    def get_loan_info(self,id):
        return self.db.query_db("SELECT * FROM loans WHERE loans.id = {}".format(id))


    def get_user_info(self,id):
        return self.db.query_db("SELECT * FROM users WHERE id = {}".format(id))

    def counter(self,old_loan):
        pass
    def get_borrower_email(self,id):
        query="SELECT users2.first AS borrower, users.first AS lender, users2.email AS borrowers_email FROM users LEFT JOIN user_loans ON users.id = user_loans.lender_id LEFT JOIN users AS users2 ON users2.id = user_loans.borrower_id WHERE user_loans.loan_ID = '{}';".format(id)
        return self.db.query_db(query)
    #Retrieves loans for borrowers

    def get_loans(self,id):
        user_query = self.db.query_db("SELECT users.id AS borrow_id, users2.id AS lender_id, users.first AS borrower,  users2.first AS lender, users.email AS borrow_email, users2.email AS lender_email FROM users LEFT JOIN user_loans ON users.id = user_loans.lender_id LEFT JOIN users AS users2 ON users2.id = user_loans.borrower_id WHERE users.id = {}".format(id))
        print user_query

        # loan_query = self.db.query_db("SELECT * FROM loans WHERE user_loans.lender_id = {} AND user_loans.borrower_id = {}".format(user_query[0]['lender'],user_query[0]['borrower']))

        # print loan_query

        #info being returned:
        #[{'lender_email': None, 'borrow_email': 'chungkyd@gmail.com', 'lender': None, 'borrow_id': 1, 'borrower': 'Darrick', 'lender_id': None}]
        return user_query


    def get_borrower_loans(self,id):
        query = "SELECT users.first AS borrower, users2.first AS lender FROM users LEFT JOIN user_loans ON users.id = user_loans.lender_id LEFT JOIN users AS users2 ON users2.id = user_loans.borrower_id WHERE users.id = {}".format(id)
        return self.db.query_db(query)



    def lender_table_info(self,id):
        # Grabs table information
        return self.db.query_db("SELECT loans.id,loans.title,loans.amount,loans.interest,loans.term,loans.start,loans.status,loans.created_at,ledgers.balance, user_loans.borrower_id, user_loans.lender_id  FROM hackathon.loans LEFT JOIN user_loans ON loans.id = user_loans.loan_id LEFT JOIN ledgers on loans.id = ledgers.loan_id WHERE user_loans.lender_id = {}".format(id))

    def borrower_table_info(self,id):
        # Grabs table information
        query = "SELECT loans.id,loans.title,loans.amount,loans.interest,loans.term,loans.start,loans.status,loans.created_at,ledgers.balance, user_loans.borrower_id,user_loans.lender_id FROM hackathon.loans LEFT JOIN user_loans ON loans.id = user_loans.loan_id LEFT JOIN ledgers on loans.id = ledgers.loan_id WHERE user_loans.borrower_id = {}".format(id)
        return self.db.query_db(query)


    def get_loan_info(self,id):
        return self.db.query_db("SELECT * FROM loans WHERE loans.id = {}".format(id))



    def ledger(self, loan):
        query = "SELECT ledgers.id,ledgers.change, ledgers.balance,ledgers.comment,ledgers.created_at FROM ledgers LEFT JOIN loans ON ledgers.loan_id = loans.id WHERE loans.id = {}".format(loan[0]['id'])
        if loan[0]['status'] == "2":
            return {'status':True, 'ledger':self.db.query_db(query)}
        else:
            return {'status': False}


    def loan_check(self,id,acct_type):
        if acct_type == "Lender":
            query = "SELECT loans.id AS loan_id from users left join user_loans on users.id = user_loans.lender_id left join loans on user_loans.loan_id = loans.id where user_loans.lender_id = {}".format(id)
            check = self.db.query_db(query)
            if check == []:
                return False
            else: 
                return True
        elif acct_type == "Borrower":
            query = "SELECT loans.id AS loan_id from users left join user_loans on users.id = user_loans.lender_id left join loans on user_loans.loan_id = loans.id where user_loans.borrower_id = {}".format(id)
            check = self.db.query_db(query)
            if check == []:
                return False
            else: 
                return True



























