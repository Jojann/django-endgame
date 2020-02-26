from django.contrib import admin
from .models import Player,Game, Options, HierarchyOpt
# Register your models here.
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Options)
admin.site.register(HierarchyOpt)
