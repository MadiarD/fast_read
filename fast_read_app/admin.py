from django.contrib import admin
from .models import Text, Block, Quetions, Answer, ClientResult, WhatsappMessage

class TextAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    
class ClientResultAdmin(admin.ModelAdmin):
    list_display = ['tel_number','text', 'speed']
    search_fields = ['tel_number']

admin.site.register(Text, TextAdmin)
admin.site.register(Block)
admin.site.register(Quetions)
admin.site.register(Answer)
admin.site.register(ClientResult, ClientResultAdmin)
admin.site.register(WhatsappMessage)