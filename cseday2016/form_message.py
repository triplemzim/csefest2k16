from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


class SubmitMessage(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	message = forms.CharField()
	captcha = NoReCaptchaField()