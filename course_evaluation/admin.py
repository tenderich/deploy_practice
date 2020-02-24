from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import *


@admin.register(Evaluation, Course)
class ImportExport(ImportExportActionModelAdmin):
    pass

