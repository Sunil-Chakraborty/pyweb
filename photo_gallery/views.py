from django.shortcuts import render

# Create your views here.
def gallery_view(request):
    # Replace this list with a query to your database if you're using a model
    image_urls = [
        "https://drive.google.com/uc?export=view&id=1r1ocxVSvKsakyJuU48IZhrdgdqZSSk_p",
        "https://drive.google.com/uc?export=view&id=1c-MaKi9V-Bqi_xuH4w6ET8E3veicGTFV",
        
        # Add more image URLs
    ]
    return render(request, 'photo_gallery/gallery.html', {'image_urls': image_urls})
   