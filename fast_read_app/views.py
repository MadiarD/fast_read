import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .read_request_handler import read_request_handler


class HomePageView(TemplateView):
    template_name = 'fast-read.html'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            test_id = data.get('id')
            text = data.get('text')
            tel_number = data.get('whatsapp_number')
            time_spent = data.get('time')
            answers = data.get('answers')
            
            return read_request_handler(
                id=test_id,
                text=text,
                tel_number=tel_number,
                time=time_spent,
                answers=answers
            )
        
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
    
    



