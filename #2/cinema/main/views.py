from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Sala, Proiezione, Film, Biglietto
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json


def home(request):
    return render(request, 'main/index.html')


def film(request):
    return render(request, 'main/film.html')


def sale(request):
    return render(request, 'main/sale.html')


def proiezioni(request):
    return render(request, 'main/proiezioni.html')


def film_api(request):
    films = Film.objects.annotate(
        proiezioni=Count('proiezione__numProiezione', distinct=True),
        vendite=Count('proiezione__biglietto')
    ).values(
        'codice', 'titolo', 'anno', 'durata', 'lingua', 'proiezioni', 'vendite'
    )

    return JsonResponse(list(films), safe=False)


def sale_api(request):
    sale_queryset = Sala.objects.annotate(
        num_proiezioni=Count('proiezioni')
    ).values('numero', 'dim', 'tipo', 'num_proiezioni')

    return JsonResponse(list(sale_queryset), safe=False)


def proiezioni_api(request):
    proiezioni = Proiezione.objects.annotate(
        biglietti=Count('biglietto')
    ).values('numProiezione', 'sala__numero', 'filmProiettato__titolo', 'biglietti', 'data',  'ora')
    data = [
        {
            'numProiezione': p['numProiezione'],
            'sala': p['sala__numero'],
            'film': p['filmProiettato__titolo'],
            'biglietti': p['biglietti'],
            'data': str(p['data']),
            'ora': str(p['ora'])[:5]
        }
        for p in proiezioni
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
def film_insert(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            film = Film(
                titolo=data['titolo'],
                anno=data['anno'],
                durata=data['durata'],
                lingua=data['lingua']
            )
            film.save()
            return JsonResponse({'success': True, 'codice': film.codice})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Metodo non supportato'}, status=405)


@csrf_exempt
def film_update(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            film = get_object_or_404(Film, codice=data['codice'])
            film.titolo = data['titolo']
            film.anno = data['anno']
            film.durata = data['durata']
            film.lingua = data['lingua']
            film.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Metodo non supportato'}, status=405)


@csrf_exempt
def film_delete(request, codice):
    if request.method == "DELETE":
        try:
            film = get_object_or_404(Film, codice=codice)
            film.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Metodo non supportato'}, status=405)
