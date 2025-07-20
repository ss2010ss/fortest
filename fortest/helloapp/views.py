from helloapp.models import textsfortest
from fortest.forms import TextForm

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from random import choices
from django.db.models import Q
from django.contrib import messages






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



def create_text(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            parenttext = form.cleaned_data['parenttext']
            # Проверяем количество записей с таким же parenttext
            parenttext_count = textsfortest.objects.filter(parenttext=parenttext).count()
            if parenttext_count >= 3:
                messages.error(request, f'Нельзя добавить больше трёх записей с parenttext "{parenttext}".')
                return render(request, 'create_text.html', {'form': form})
            text = form.cleaned_data['text']
            text_in_base = textsfortest.objects.filter(text=text).count()
            if text_in_base > 0:
                messages.error(request, f'Текст "{text}" уже существует в базе данных.')
                return render(request, 'create_text.html', {'form': form})
            try:
                form.save()  # Сохраняем данные в базу
                messages.success(request, 'Цитата успешно добавлена!')
                return render(request, 'create_text.html', {'form': TextForm()})  # Очищаем форму после успеха
            except Exception as e:
                messages.error(request, f'Ошибка сохранения: {str(e)}')
                return render(request, 'create_text.html', {'form': form})
        else:
            messages.error(request, 'Ошибка в форме. Проверьте введённые данные.')
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





def look_texts(request):
    # Получаем номер страницы из запроса (по умолчанию 1)
    page = int(request.GET.get('page', 1))
    per_page = 10
    texts = textsfortest.objects.all().order_by('text')  # Сортировка по тексту для предсказуемого порядка
    total_texts = texts.count()
    
    # Вычисляем индексы для выборки
    start = (page - 1) * per_page
    end = start + per_page
    paginated_texts = texts[start:end]
    
    # Вычисляем, есть ли предыдущая и следующая страницы
    has_previous = page > 1
    has_next = end < total_texts

    return render(request, 'look_texts.html', {
        'texts': paginated_texts,
        'page': page,
        'has_previous': has_previous,
        'has_next': has_next,
        'total_texts': total_texts
    })

def search_texts(request):
    query = request.GET.get('q', '')
    if len(query) >= 3:
        # Поиск по полям text и parenttext (без учета регистра)
        results = textsfortest.objects.filter(
            Q(text__icontains=query) | Q(parenttext__icontains=query)
        ).values('text', 'parenttext', 'count', 'like', 'dislike')[:10]  # Ограничиваем до 10 результатов
        results = list(results)
    else:
        results = []
    return JsonResponse({'results': results, 'query': query})

