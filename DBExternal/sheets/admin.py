from django.contrib import admin
from sheets.models import Users, Ownership, Sheets, Cell, ContainedIn, DataObject, Documents, Has, Image, IsIn, Text, Video

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email_id')

class DocAdmin(admin.ModelAdmin):
    list_display = ('doc_id', 'doc_name', 'created_on','created_by')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('username', 'doc','rights')


class SheetAdmin(admin.ModelAdmin):
    list_display = ('sheet_id', 'sheet_name','total_columns','total_rows')

class ContainedInAdmin(admin.ModelAdmin):
    list_display = ('doc','sheet')

class CellAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'cell_x','cell_y','cell_color')

class IsInAdmin(admin.ModelAdmin):
    list_display = ('sheet','cell')

admin.site.register(Users,UserAdmin)
admin.site.register(Ownership,OwnerAdmin)
admin.site.register(Documents,DocAdmin)
admin.site.register(ContainedIn,ContainedInAdmin)
admin.site.register(Sheets,SheetAdmin)
admin.site.register(IsIn,IsInAdmin)
admin.site.register(Cell,CellAdmin)
admin.site.register(DataObject)
admin.site.register(Has)
admin.site.register(Image)
admin.site.register(Text)
admin.site.register(Video)
# Register your models here.
