import django_tables2 as tables

from .models import CustomersInfoAnalysis


class CustomersInfoAnalysisTable(tables.Table):
    customer_email = tables.Column(verbose_name='E-mail', orderable=False)
    monetary = tables.Column(verbose_name='Monetary', orderable=False)
    frequency = tables.Column(verbose_name='Frequency', orderable=False)
    recency = tables.Column(verbose_name='Recency', orderable=False)
    avg_monetary = tables.Column(verbose_name='Avg. Monetary', orderable=False)
    first_purchase = tables.Column(verbose_name='First Purchase', orderable=False)
    avg_days = tables.Column(verbose_name='Avg. Days', orderable=False)
    purchase_status__title = tables.Column(verbose_name='Purchase Status', orderable=False, attrs={
        "td": {
            'data-status': lambda value: value
        }
    })
    segment__title = tables.Column(verbose_name='Segment', orderable=False)

    def render_monetary(self, value):
        return 'R$ {}'.format(self.real_br_money_mask(value))

    def render_avg_monetary(self, value):
        return 'R$ {}'.format(self.real_br_money_mask(value))

    def render_avg_days(self, value):
        return '{}'.format(round(value, 1))

    @staticmethod
    def real_br_money_mask(my_value):
        a = '{:,.2f}'.format(float(my_value))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        return c.replace('v', '.')

    class Meta:
        model = CustomersInfoAnalysis
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "customer_email",
            "monetary",
            "frequency",
            "recency",
            "avg_monetary",
            "first_purchase",
            "avg_days",
            "purchase_status__title",
            "segment__title")
