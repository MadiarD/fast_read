from django.contrib import admin
from .models import Text, Block, Quetions, Answer, ClientResult, WhatsappMessage

class TextAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    

admin.site.register(Text, TextAdmin)
admin.site.register(Block)
admin.site.register(Quetions)
admin.site.register(Answer)
admin.site.register(ClientResult)
admin.site.register(WhatsappMessage)