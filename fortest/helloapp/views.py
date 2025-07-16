from helloapp.models import textsfortest
from fortest.forms import TextForm

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from random import choices



# Create your views here.


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



def random_text_view(request):
    # Получить все тексты
    texts = textsfortest.objects.all()
    if texts.exists():
        # Извлечь веса для каждого текста
        weights = [max(text.weight, 1) for text in texts]  # Убедимся, что веса неотрицательные
        # Выбрать один случайный текст с учетом весов
        random_text = choices(texts, weights=weights, k=1)[0]
        # Увеличить счетчик посещений
        random_text.count += 1
        random_text.save()
    else:
        random_text = None

    return render(request, 'random_text.html', {'text': random_text})

@require_POST
def update_likes(request, text_id):
    text = get_object_or_404(textsfortest, id=text_id)
    if 'like' in request.POST:
        text.like += 1
    elif 'dislike' in request.POST:
        text.dislike += 1
    text.save()
    return JsonResponse({'likes': text.like, 'dislikes': text.dislike})



def look_texts_view(request):
    return render(request, 'look_texts.html')  # Создайте шаблон, если нужно