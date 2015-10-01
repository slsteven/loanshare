
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



"""
    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
