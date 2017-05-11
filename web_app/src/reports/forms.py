from django import forms

from organization.models import Stations, Stages
from basemodel.models import Models 


class FilterForm(forms.Form):
	models = forms.ModelChoiceField(queryset=Models.objects.none(),empty_label='Choose Model')
	stations = forms.ModelChoiceField(queryset=Stations.objects.none(),empty_label='Choose Stations')
	stages = forms.ModelChoiceField(queryset=Stages.objects.none(),empty_label='Choose Stage')

	class Meta:
		fields = ['models']


	def __init__(self, *args, **kwargs):
		super(FilterForm, self).__init__(*args, **kwargs)
		# assign a (computed, I assume) default value to the choice field
		self.fields['models'].queryset = Models.objects.all()
		self.fields['stations'].queryset = Stations.objects.all()
		self.fields['stages'].queryset = Stages.objects.all()