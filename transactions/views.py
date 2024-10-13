# transactions/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from .forms import TransactionForm

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('date')
    total_amount = sum(t.amount if t.tr == 'Rct' else -t.amount for t in transactions)
    total_rect = sum(t.amount for t in transactions if t.tr == 'Rct')
    total_exp = sum(t.amount for t in transactions if t.tr == 'Exp')
    return render(request, 'transactions/tran_listing.html', {
        'transactions': transactions,
        'total_amount': total_amount,
        'total_rect': total_rect,
        'total_exp': total_exp,
    })

def add_transaction(request):
    form = TransactionForm()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions:transaction_list')
    
    return render(request, 'transactions/add_transaction.html', {'form': form})


@csrf_exempt
def edit_transaction(request, transactionId):
    if request.method == 'POST':
        tr          = request.POST.get('tr')
        name        = request.POST.get('name')
        comment     = request.POST.get('comment')
        amount      = request.POST.get('amount')
        doc_date    = request.POST.get('date')
        

        # Get the transaction object and update its fields
        transaction = get_object_or_404(Transaction, id=transactionId)
        transaction.tr = tr
        transaction.name = name
        transaction.comment = comment
        transaction.amount = amount
        transaction.date = doc_date
        transaction.save()

        return redirect('transactions:transaction_list')  # Update with your actual list view name

    return redirect('transactions:transaction_list')



def delete_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    transaction.delete()
    return redirect('transactions:transaction_list')
