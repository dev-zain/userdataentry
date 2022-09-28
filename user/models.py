from django.db import models
import barcode                      # additional imports
import qrcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw

# Create your models here.
class User(models.Model):
    photo = models.ImageField(upload_to ='images', default='user-icon.jpg', null=True)
    rc_id = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    cnic = models.CharField(max_length=20)
    age = models.CharField(max_length=5)
    address = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    issue_date = models.CharField(max_length=15)
    expiry_date = models.CharField(max_length=15)
    regn_of_vehicle = models.CharField(max_length=30)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # email = models.EmailField(max_length=50, blank=True, null=True)
    barcode = models.ImageField(upload_to='barcodes', blank=True)
    code =models.ImageField(upload_to ='QRcode',blank = True)

    class Meta:
        ordering = ['-created_at','-updated_at']

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):

        # generate barcode
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.rc_id}{self.cnic}{self.name}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.name}br.png', File(buffer), save=False)
       
       # generate qr code
        qr_image = qrcode.make(self.rc_id)
        qr_offset = Image.new('RGB',(310, 310), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.name}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super(User,self).save(*args, **kwargs)

   
            
        
        
    
    