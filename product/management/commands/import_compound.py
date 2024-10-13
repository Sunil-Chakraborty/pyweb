import csv
from django.core.management.base import BaseCommand
from product.models import Compound, RawMat, RawGrp
from sales.models import Customer, Product, SalesInvoice, SalesInvoiceItem

from datetime import datetime
from django.utils import timezone

#python manage.py import_compound

"""
class Command(BaseCommand):
    help = 'Import compound data from comp.csv'

    def handle(self, *args, **kwargs):
        with open('comp.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                compound = Compound(
                    comp_cd=row['comp_cd'],
                    sap_cd=row['sap_cd'],
                    batch_wt=row['batch_wt'],
                    uom=row['uom'],
                    spg=row['spg'],
                    created_date=timezone.now()
                )
                compound.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))

class Command(BaseCommand):
    help = 'Import RawGrp data from raw_grp.csv'

    def handle(self, *args, **kwargs):
        with open('raw_grp.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rawgrp = RawGrp(
                    grp_cd  = row['grp_cd'],
                    grp_des = row['grp_des'],                    
                    created_date=timezone.now()
                )
                rawgrp.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))



class Command(BaseCommand):
    help = 'Import Raw Mat data from raw_mat.csv'
    
    #grp_cd      = models.ForeignKey("RawGrp", on_delete=models.CASCADE, related_name='group')
    
    def handle(self, *args, **kwargs):
        with open('raw_mat.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Fetch the RawGrp instance based on the grp_cd value
                try:
                    grp = RawGrp.objects.get(grp_cd=row['grp_cd'])
                except RawGrp.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"RawGrp with grp_cd {row['grp_cd']} does not exist."))
                    continue
                    
                # Check if the record already exists
                #if RawMat.objects.filter(rm_cd=row['rm_cd']).exists():
                #if RawMat.objects.filter(rm_cd=row['rm_cd'], sap_cd=row['sap_cd']).exists():

                    #self.stdout.write(self.style.WARNING(f"RawMat with rm_cd {row['rm_cd']} already exists. Skipping import."))
                    #continue

                rawmat          = RawMat(
                    rm_cd       = row['rm_cd'],
                    sap_cd      = row['sap_cd'],
                    rm_des      = row['rm_des'],
                    grp_cd      = grp,  # Assign the RawGrp instance here
                    uom         = row['uom'],
                    rate        = row['Rate'],
                    created_date=timezone.now()
                )
                rawmat.save()
        
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))




        
class Command(BaseCommand):
    help = 'Import SalesInvoice data from invoices.csv'

    def handle(self, *args, **kwargs):
        with open('invoices.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                invoices = SalesInvoice(
                    invoice_no  = row['invoice_no'],
                    date = row['date'],
                    customer = row['customer'],                     
                    created_date=timezone.now()
                )
                invoices.save()
        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))




class Command(BaseCommand):
    help = 'Import SalesInvoice data from invoices.csv'

    def handle(self, *args, **kwargs):
        with open('invoices.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get the Customer instance based on name (or use another unique identifier)
                try:
                    customer = Customer.objects.get(name=row['customer'])
                except Customer.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Customer {row['customer']} not found. Skipping row."))
                    continue
                
                # Convert date from 'DD-MM-YYYY' to 'YYYY-MM-DD' format
                try:
                    date_obj = datetime.strptime(row['date'], '%d-%m-%Y').date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid date format in row: {row['date']}. Skipping row."))
                    continue
                    
                # Create the SalesInvoice instance
                invoice = SalesInvoice(
                    invoice_no=row['invoice_no'],
                    date = date_obj,  # Ensure the date format in CSV is valid
                    customer=customer,  # Assign the retrieved Customer instance
                    created_date=timezone.now()
                )
                invoice.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))


"""

class Command(BaseCommand):
    help = 'Import SalesInvoiceItem data from invoice_items.csv'

    def handle(self, *args, **kwargs):
        with open('invoice_items.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get the SalesInvoice instance based on the invoice number
                try:
                    invoice = SalesInvoice.objects.get(invoice_no=row['invoice'])
                except SalesInvoice.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"SalesInvoice {row['invoice']} not found. Skipping row."))
                    continue

                # Get the Product instance based on the product name
                try:
                    product = Product.objects.get(name=row['product'])
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Product {row['product']} not found. Skipping row."))
                    continue

                # Create the SalesInvoiceItem instance
                try:
                    invoice_item = SalesInvoiceItem(
                        invoice=invoice,  # Assign the retrieved SalesInvoice instance
                        product=product,  # Assign the retrieved Product instance
                        quantity=row['quantity'],
                        rate=row['rate'],
                        total=row['total'],
                        created_date=timezone.now()  # Automatically set the created date
                    )
                    invoice_item.save()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error saving row {row}: {e}. Skipping row."))
                    continue

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))    