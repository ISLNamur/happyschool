from appyschool.bindings import AppySchoolBinding
from schedule_change.models import ScheduleChange
from schedule_change.serializers import ScheduleChangeSerializer


class ScheduleChangeBinding(AppySchoolBinding):
    model = ScheduleChange
    stream = "schedule_change"
    serializer_class = ScheduleChangeSerializer
    queryset = ScheduleChange.objects.all()

    default_order = 'date_start'
    filters = ('teachers', 'date_start', 'date_end', 'classes')
    filters_display = ('Professeurs', 'Date de début', 'Date de fin', 'Classes')

    def order_queryset(self, order_by):
        if order_by == 'date_start':
            return self.queryset.order_by(order_by, 'time_start')
        else:
            return super(ScheduleChange).order_queryset(order_by)
