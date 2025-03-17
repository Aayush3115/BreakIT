from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import GroupForm, ExpenseForm
from .models import Group, Expense

# Create your views here.

def dashboard(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'core/dashboard.html', {'groups': groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'core/group_detail.html', {'group': group})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user  # Set admin to current user
            group.save()
            form.save_m2m()  # Save members (ManyToMany field)
            return redirect('dashboard')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.payer = request.user
            expense.save()
            return redirect('group_detail', group_id=expense.group.id)
    else:
        form = ExpenseForm()
    return render(request, 'create_expense.html', {'form': form})

def create_expense(request):
    # ... (previous code)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.payer = request.user
        expense.save()

        # Split equally among members
        group = expense.group
        members = group.members.all()
        share = expense.amount / members.count()
        for member in members:
            if member != expense.payer:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=member,
                    share=share
                )
        return redirect('group_detail', group_id=group.id)