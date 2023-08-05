from frasco import current_context, current_app
from wtforms import SelectField
from .db import *
from . import current_country, country_currency


class CountryField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices',
            sorted([(c.alpha_2, c.name) for c in countries],
                key=lambda v: v[1].lower()))
        if current_country:
            kwargs.setdefault("default", current_country.alpha_2)
        super(CountryField, self).__init__(*args, **kwargs)


class LanguageField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', 
            sorted([(c.alpha_2, c.name) for c in languages if hasattr(c, "alpha_2")],
                key=lambda v: v[1].lower()))
        kwargs.setdefault("default", "en")
        super(LanguageField, self).__init__(*args, **kwargs)


class CurrencyField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', sorted([(c.alpha_3, "%s - %s" % (c.alpha_3, c.name)) for c in currencies],
            key=lambda v: v[1].lower()))
        try:
            if current_country:
                kwargs.setdefault('default', country_currency(current_country))
        except:
            pass
        super(CurrencyField, self).__init__(*args, **kwargs)
