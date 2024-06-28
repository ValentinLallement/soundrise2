from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ( 'username', 'id','rank','email', 'full_name', 'country','tel', 'is_staff','mail_pro')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('full_name','rank', 'email', 'country','mail_pro')}),
        (('data'), {'fields': ('profile_picture', 'profile_free_text','darkTheme')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    
admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib.auth import get_user_model
from .models import Message, Conversation

# Use get_user_model() to reference the User model
User = get_user_model()

class MessageAdmin(admin.ModelAdmin):
  """
  Admin interface for Message model.
  """
  list_display = ('sender', 'recipient', 'body', 'created_at')
  readonly_fields = ('created_at',)
  search_fields = ('sender__username', 'recipient__username', 'body')

admin.site.register(Message, MessageAdmin)

class ConversationAdmin(admin.ModelAdmin):
  """
  Admin interface for Conversation model.
  """
  list_display = ('get_participants',)  # Fix 1: Use method name for list_display

  # Define a custom method to display participants in list view
  def get_participants(self, obj):
    return ", ".join([user.username for user in obj.participants.all()])
  get_participants.short_description = 'Participants'

admin.site.register(Conversation, ConversationAdmin)

