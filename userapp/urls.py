from django.urls import path
from userapp import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_data/', views.expense_data, name='expense_data'),
    path('expense_history/', views.expense_history, name='expense_history'),
    path('expense_edit/<int:dataid>', views.expense_edit, name='expense_edit'),
    path('expense_update/<int:dataid>', views.expense_update, name='expense_update'),
    path('expense_delete/<int:dataid>', views.expense_delete, name='expense_delete'),
    path('delete_expense/<int:dataid>', views.delete_expense, name='delete_expense'),
    path('expense_report/', views.expense_report, name='expense_report'),
]
