from django.http import HttpResponse
from django.shortcuts import render,redirect
from userapp.models import expense
from datetime import datetime
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth, ExtractYear,ExtractDay
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.db.models import Q


# Create your views here.

@login_required
def index(request):
    current_user = request.user
    current_date = datetime.now()
    current_month_expenses = expense.objects.filter(
        user=current_user,
        date__year=current_date.year,
        date__month=current_date.month
    )
    total_expense = current_month_expenses.aggregate(Sum('amount'))['amount__sum']

    if total_expense is None:
        total_expense = 0  # Ensure a default value if there are no expenses

    context = {
        'current_month_expenses': current_month_expenses,
        'total_expense': total_expense,
    }

    data = expense.objects.filter(user=current_user).order_by('-created_at')[:5]

    # Calculate expenses by categories
    categories = expense.objects.filter(user=current_user).values('category').annotate(total_amount=Sum('amount'))
    categories_data = [category['category'] for category in categories]
    categories_amount = [category['total_amount'] for category in categories]

    return render(request, 'index.html', {
        'data': data,
        'context': context,
        'categories_data': categories_data,
        'categories_amount': categories_amount,
    })


def delete_expense(req,dataid):
    data=expense.objects.filter(id=dataid)
    data.delete()
    return redirect(index)

def add_expense(req):
    return render(req,'add_expense.html')

@login_required
def expense_data(req):
    if req.method == 'POST':
        current_user = req.user
        en = req.POST.get('expense_name')
        am = req.POST.get('amount')
        dt = req.POST.get('date')
        ct = req.POST.get('category')
        obj = expense(user=current_user, expense_name=en, amount=am, date=dt, category=ct)
        obj.save()

        # Add the following JavaScript script
        return render(req, 'add_expense.html', {'success_message': 'Expense added successfully'})
    return HttpResponse("Invalid Request")

    

@login_required
def expense_history(req):
    current_user = req.user
    # Retrieve all expense records for the logged-in user from the database
    all_expenses = expense.objects.filter(user=current_user)

    # Filter by search query (expense name)
    search_query = req.GET.get('search')
    if search_query:
        all_expenses = all_expenses.filter(Q(expense_name__icontains=search_query))

    # Filter by date
    start_date = req.GET.get('start_date')
    end_date = req.GET.get('end_date')
    if start_date and end_date:
        all_expenses = all_expenses.filter(date__range=[start_date, end_date])

    # Filter by category
    category = req.GET.get('category')
    if category:
        all_expenses = all_expenses.filter(category=category)

    # Initialize a Paginator with the queryset and the number of items per page
    paginator = Paginator(all_expenses, 10)  # 10 items per page

    # Get the current page number from the request's GET parameters
    page_number = req.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(req, 'expense_history.html', {
        'page': page,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'category': category,
    })


def expense_edit(req,dataid):
    data=expense.objects.get(id=dataid)
    return render(req,"edit_expense.html",{"data":data})

def expense_update(req,dataid):
    if req.method=="POST":
        en=req.POST.get('expense_name')
        am=req.POST.get('amount')
        dt=req.POST.get('date')
        ct=req.POST.get('category')
        expense.objects.filter(id=dataid).update(expense_name=en,amount=am,date=dt,category=ct)
        messages.success(req,"Expense updated successfully")
        return redirect(expense_history)
    

def expense_delete(req,dataid):
    data=expense.objects.filter(id=dataid)
    data.delete()
    messages.success(req,"Deleted successfully")
    return redirect(expense_history)

@login_required
def expense_report(request):
    current_user = request.user
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year', datetime.now().year)

        try:
            selected_month = int(selected_month) if selected_month and selected_month != 'Select month' else None
        except ValueError:
            selected_month = None

        # Handle the case where 'Select year' is selected in the form
        if selected_year == 'Select year':
            selected_year = None
        else:
            selected_year = int(selected_year)

        # If only month is selected without a year, provide a message
        if selected_month and not selected_year:
            error_message = "Please select a year along with the month."
            context = {'error_message': error_message}
            return render(request, 'expense_report.html', context)

        # If both month and year are selected, display daily expenses
        if selected_month and selected_year:
            expenses = expense.objects.filter(user=current_user, date__month=selected_month, date__year=selected_year)
            report_type = f"Monthly Report of {selected_month}, {selected_year}"
        # If only year is selected, display monthly expenses
        elif selected_year:
            expenses = expense.objects.filter(user=current_user, date__year=selected_year)
            report_type = f"Yearly Report of {selected_year}"
        else:
            # Handle other cases or provide a default behavior
            return HttpResponse("Invalid selection")

        total_expense = expenses.aggregate(Sum('amount'))['amount__sum']

        categories_data = (
            expenses.values('category')
            .annotate(total_expense=Sum('amount'))
            .order_by('category')
        )

        # Total Expense by Category
        total_expense_by_category = (
            expenses.values('category')
            .annotate(total_expense=Sum('amount'))
            .order_by('category')
        )

        # Adjust the date filtering based on the selected_month and selected_year
        if selected_month and selected_year:
            daily_expenses = expenses.values(day=ExtractDay('date')) \
                .annotate(total_expense=Sum('amount'))

            chart_labels = [f"{selected_month}-{expense['day']}-{selected_year}" for expense in daily_expenses]
            chart_data = [expense['total_expense'] for expense in daily_expenses]
        else:
            monthly_expenses = expenses.values(month=ExtractMonth('date')) \
                .annotate(total_expense=Sum('amount'))

            chart_labels = [f"{expense['month']}-{selected_year}" for expense in monthly_expenses]
            chart_data = [expense['total_expense'] for expense in monthly_expenses]

        context = {
            'report_type': report_type,
            'selected_month': selected_month,
            'selected_year': selected_year,
            'expenses': expenses,
            'total_expense': total_expense or 0,
            'categories_data': categories_data,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'total_expense_by_category': total_expense_by_category,
        }

        return render(request, 'expense_report.html', context)
    else:
        current_date = datetime.now()
        context = {
            'selected_month': None,
            'selected_year': current_date.year,
        }
        return render(request, 'expense_report.html', context)
