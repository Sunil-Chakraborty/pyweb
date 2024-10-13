from django.db import models
from django.utils import timezone

# Create your models here.

class Compound(models.Model):
    comp_cd     = models.CharField(max_length=10)
    sap_cd      = models.CharField(max_length=10)
    comp_des    = models.CharField(max_length=200)
    batch_wt    = models.DecimalField(max_digits=7, decimal_places=3)
    uom         = models.CharField(max_length=10)
    spg         = models.DecimalField(max_digits=5, decimal_places=3)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.comp_cd
        
class RawMat(models.Model):
    rm_cd       = models.CharField(max_length=10)
    sap_cd      = models.CharField(max_length=10)
    rm_des      = models.CharField(max_length=240)
    grp_cd      = models.ForeignKey("RawGrp", on_delete=models.CASCADE, related_name='group')
    uom         = models.CharField(max_length=10)
    rate        = models.DecimalField(max_digits=7, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)
    
    # Barcode field to store the generated barcode as text (e.g., Code128)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):  
        return self.rm_cd

class Recepi(models.Model):
    card_no         = models.CharField(max_length=10)
    doc_dt          = models.DateField(null=True, blank=True)
    comp_cd         = models.ForeignKey(Compound, on_delete=models.CASCADE)
    rm_cd           = models.ForeignKey(RawMat, on_delete=models.CASCADE)    
    qty             = models.DecimalField(max_digits=7, decimal_places=3)
    created_date    = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.card_no} - {self.comp_cd}'

class RawGrp(models.Model):
    grp_cd       = models.CharField(max_length=10)
    grp_des      = models.CharField(max_length=240)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.grp_cd} - {self.grp_des}'


class MixProd(models.Model):   
    card_no         = models.ForeignKey(Recepi, on_delete=models.CASCADE, related_name="mixprod_card_no") # ForeignKey to Recepi's card_no
    prod_no         = models.CharField(max_length=10)  # Production Order Number
    prod_dt         = models.DateField(null=True, blank=True)  # Production Order Date
    qty             = models.DecimalField(max_digits=7, decimal_places=3)  # Order Quantity
    created_date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.prod_no}'        