from django import forms


class SearchForm(forms.forms.Form):
    query = forms.CharField()

    @property
    def query_value(self):
        if self.is_valid():
            return self.cleaned_data['query']
