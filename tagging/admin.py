from django.contrib import admin

import diet.models as diet


@admin.register(diet.Diet)
class DishAdmin(admin.ModelAdmin):
    filter_horizontal = ('dishes', )
    exclude = ('user', )
    list_display = ('title', 'user', )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.generate()
        super(DishAdmin, self).save_model(request, obj, form, change)
