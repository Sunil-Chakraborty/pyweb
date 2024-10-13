from django.shortcuts import render, get_object_or_404
from .models import SalesInvoice

def sales_invoice_print(request, invoice_no):
    invoice = get_object_or_404(SalesInvoice, invoice_no=invoice_no)
    total_amount = sum(item.total for item in invoice.items.all())
    
    return render(request, 'sales/sales_invoice_print.html', {
        'invoice': invoice,
        'total_amount': total_amount
    })