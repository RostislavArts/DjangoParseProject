# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Videocard

def videocard_list(request):
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        videocards = Videocard.objects.all().order_by('name')
    elif sort_by == 'id':
        videocards = Videocard.objects.all().order_by('id')
    else:
        videocards = Videocard.objects.all()
    return render(request, 'product_list.html', {'videocards': videocards})

def videocard_detail(request, id):
    videocard = get_object_or_404(Videocard, id=id)
    return render(request, 'product_detail.html', {'videocard': videocard})
