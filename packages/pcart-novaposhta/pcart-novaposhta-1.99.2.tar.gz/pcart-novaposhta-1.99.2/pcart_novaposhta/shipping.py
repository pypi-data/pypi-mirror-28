from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from pcart_cart.shipping import BaseShipping
from .models import Area, City, Office


class NovaPoshtaShippingForm(forms.Form):
    def __init__(self, strict_validation, *args, **kwargs):
        super(NovaPoshtaShippingForm, self).__init__(*args, **kwargs)
        self.strict_validation = strict_validation
        _data = self.data.copy()

        # Areas
        areas = Area.objects.all().values('id', 'description')
        area_choices = [(None, '-----')]
        area_choices += [(x['id'], x['description']) for x in areas]

        self.fields['area'] = forms.ChoiceField(
            label=_('Region'),
            choices=area_choices,
            required=False,
        )

        if 'area' in _data and _data['area']:
            cities = City.objects.filter(area_id=_data['area']).values('id', 'description')
            city_choices = [(None, '-----')]
            city_choices += [(x['id'], x['description']) for x in cities]

            self.fields['city'] = forms.ChoiceField(
                label=_('City'),
                choices=city_choices,
                required=False,
            )

        if 'city' in _data and _data['city']:
            offices = Office.objects.filter(city_id=_data['city']).values('id', 'description')
            office_choices = [(None, '-----')]
            office_choices += [(x['id'], x['description']) for x in offices]
            self.fields['office'] = forms.ChoiceField(
                label=_('Office'),
                choices=office_choices,
                required=False,
            )
        self.selected_office = None

    def clean_area(self):
        from django.utils.translation import ugettext
        area = self.cleaned_data['area']
        if self.strict_validation and not area:
            raise forms.ValidationError(ugettext('Region field is required'))
        return area

    def clean_city(self):
        from django.utils.translation import ugettext
        city = self.cleaned_data['city']
        if self.strict_validation and not city:
            raise forms.ValidationError(ugettext('City field is required'))
        return city

    def clean_office(self):
        from django.utils.translation import ugettext
        office = self.cleaned_data['office']
        if self.strict_validation and not office:
            raise forms.ValidationError(ugettext('Office field is required'))
        if office:
            try:
                self.selected_office = Office.objects.get(id=office)
            except Office.DoesNotExist:
                self.selected_office = None
        return office


class NovaPoshtaShipping(BaseShipping):
    title = _('Nova Poshta')
    info_block_include = 'novaposhta/info_block.html'

    def __init__(self, config={}):
        super(NovaPoshtaShipping, self).__init__(config)
        self.api_key = config.get('api_key', getattr(settings, 'PCART_NOVAPOSHTA_API_KEY', ''))

    def get_form(self, request, strict_validation, *args, **kwargs):
        if self.api_key is not None:
            form = NovaPoshtaShippingForm(strict_validation, *args, **kwargs)
            return form

    def render_data(self, data, plain_text=False):
        from django.template.loader import render_to_string

        area_id = data.get('area')
        city_id = data.get('city')
        office_id = data.get('office')

        area = Area.objects.get(pk=area_id) if area_id else None
        city = City.objects.get(pk=city_id) if city_id else None
        office = Office.objects.get(pk=office_id) if office_id else None

        context = {
            'method': self,
            'area': area,
            'city': city,
            'office': office,
        }
        if plain_text:
            return render_to_string('admin/novaposhta/shipping_preview.txt', context)
        else:
            return render_to_string('admin/novaposhta/shipping_preview.html', context)
