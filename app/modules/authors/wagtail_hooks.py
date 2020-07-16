from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Author


class AuthorAdmin(ModelAdmin):
    model = Author
    menu_label = "Authors"
    menu_icon = "user"


modeladmin_register(AuthorAdmin)
