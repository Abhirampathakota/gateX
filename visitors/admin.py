from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Student, VisitRequest, TimeSlot


# Feature: Download Logs as CSV
def export_visits_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visit_logs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Roll No', 'Student Name', 'Status', 'Entry Time', 'Exit Time'])

    for visit in queryset:
        writer.writerow([
            visit.student.roll_number,
            visit.student.user.first_name if getattr(visit.student, 'user', None) else '',
            visit.status,
            visit.entry_time,
            visit.exit_time,
        ])
    return response


export_visits_csv.short_description = "Download Report (CSV)"


class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'parent_name', 'department')


class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'time_slot', 'status', 'request_date')
    list_filter = ('status', 'time_slot', 'request_date')
    actions = [export_visits_csv]


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('label', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active',)


admin.site.register(Student, StudentAdmin)
admin.site.register(VisitRequest, VisitRequestAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
