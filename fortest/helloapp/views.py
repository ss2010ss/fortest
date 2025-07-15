from helloapp.models import textsfortest
from django.shortcuts import render, redirect
from fortest.forms import TextForm

# Create your views here.
def index_page(request):
    all_texts = textsfortest.objects.all()
    # This will fetch all records from the textsfortest model

    return render (request, 'index.html', context={'all_texts': all_texts})


def create_text(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняет данные в базу
            return render(request, 'create_text.html', {'form': form})
            #return redirect('success')  # Перенаправление на страницу успеха
    else:
        form = TextForm()
    
    return render(request, 'create_text.html', {'form': form})
