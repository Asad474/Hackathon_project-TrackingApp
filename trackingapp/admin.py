from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Userprofile)
admin.site.register(Activity)
admin.site.register(Food)