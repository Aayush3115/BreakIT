from collections import defaultdict

def calculate_balances(user):
    balances = defaultdict(float)
    # What others owe the user
    paid_expenses = Expense.objects.filter(payer=user)
    for expense in paid_expenses:
        participants = expense.expenseparticipant_set.all()
        for participant in participants:
            balances[participant.user] += participant.share

    # What the user owes others
    involved_expenses = ExpenseParticipant.objects.filter(user=user)
    for participant in involved_expenses:
        balances[participant.expense.payer] -= participant.share

    return balances