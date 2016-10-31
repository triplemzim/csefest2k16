from django import forms


class SubmitMessage(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	message = forms.CharField()