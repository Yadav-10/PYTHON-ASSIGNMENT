from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job, Task
from .coinmarketcap import CoinMarketCap
from celery import shared_task

class StartScrapingView(APIView):
    def post(self, request):
        coin_symbols = request.data.get('coin_symbols')
        if not isinstance(coin_symbols, list) or not all(isinstance(symbol, str) for symbol in coin_symbols):
            return Response({'error': 'Invalid input. Please provide a list of coin symbols.'}, status=400)
        job = Job.objects.create()
        for symbol in coin_symbols:
            Task.objects.create(job=job, coin_symbol=symbol)
        scrape_task.delay(job.id)
        return Response({'job_id': job.id})

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        job = Job.objects.get(id=job_id)
        tasks = Task.objects.filter(job=job)
        data = {}
        for task in tasks:
            data[task.coin_symbol] = task.scraped_data
        return Response(data)

@shared_task
def scrape_task(job_id):
    job = Job.objects.get(id=job_id)
    tasks = Task.objects.filter(job=job)
    cmc = CoinMarketCap()
    for task in tasks:
        data = cmc.scrape_coin_data(task.coin_symbol)
        task.scraped_data = data
        task.save()