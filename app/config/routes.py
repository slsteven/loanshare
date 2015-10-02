
from system.core.router import routes

routes['default_controller'] = 'Loans'
routes['POST']['/users/register'] = 'Loans#new_user'
routes['POST']['/users/login'] = 'Loans#login'
routes['POST']['/users/loan_form'] = 'Loans#create_loan'
routes['GET']['/users/get_loan'] = 'Loans#new_loan'
routes['GET']['/users/dashboard'] = 'Loans#show_dashboard'
routes['GET']['/users/logout'] = 'Loans#logout'
routes['GET']['/login'] = 'Loans#user_login'
routes['GET']['/users/loan/<loan_id>'] = 'Loans#show_loan'
routes['GET']['/home'] = 'Loans#home'
routes['POST']['/accept/<id>'] = 'Loans#accepted_loan'

routes['GET']['/users/<loan_id>/adjust'] = 'Loans#adjust_loan'
routes['GET']['/users/<loan_id>/accept'] = 'Loans#accept_loan'

routes['GET']['/admin_dash'] = 'Loans#admin_dash'
routes['GET']['/index_json'] = 'Loans#index_json'

routes['/loan_payment'] = 'Loans#payment_amount'
routes['POST']['/payment'] ='Loans#payment'
routes['POST']['/charge'] = 'Loans#stripe_charge'


"""
    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
