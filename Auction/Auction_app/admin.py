from django.contrib import admin

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage

# Register your models here.
from .models import *

admin.site.register(Category),
admin.site.register(SubCategory),
admin.site.register(AddProduct),
admin.site.register(Bid),
admin.site.register(Cart),
admin.site.register(CartItems),
admin.site.register(RejectedProduct),
admin.site.register(DeliveryBoy),
admin.site.register(Order),
admin.site.register(UserPayment),
admin.site.register(Review),

admin.site.register(ChatMessage),
admin.site.register(BlogPost),
admin.site.register(Like),
admin.site.register(TotalView),
admin.site.register(DeliveryAssignment),


class ChatMessage(admin.TabularInline):
    model = ChatMessage


# class ThreadForm(forms.ModelForm):
#     def clean(self):
#         """
#         This is the function that can be used to
#         validate your model data from admin
#         """
#         super(ThreadForm, self).clean()
#         first_person = self.cleaned_data.get('first_person')
#         second_person = self.cleaned_data.get('second_person')
#
#         lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
#         lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
#         lookup = Q(lookup1 | lookup2)
#         qs = Thread.objects.filter(lookup)
#         if qs.exists():
#             raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')
#

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)