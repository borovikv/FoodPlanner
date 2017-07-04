from django import forms


class UrlForm(forms.forms.Form):
    url = forms.URLField()


class UrlsForm(forms.forms.Form):
    urls_list = forms.CharField(widget=forms.Textarea)

    def urls(self):
        return self.cleaned_data['urls_list'].split('\n')


class SearchForm(forms.forms.Form):
    query = forms.CharField()
