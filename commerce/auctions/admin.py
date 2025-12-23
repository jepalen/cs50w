from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment, Watchlist

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)