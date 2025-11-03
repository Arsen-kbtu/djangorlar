# admin placeholder for players app
from django.contrib import admin
from .models import Player

# Register placeholder model
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'joined')
