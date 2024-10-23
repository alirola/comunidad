from django import forms
from .models import Incidencia
from .models import ReservaPadel

class IncidenciaForm(forms.ModelForm):
	class Meta:
		model = Incidencia
		fields = ['titulo', 'descripcion']

class ReservaPadelForm(forms.ModelForm):
	class Meta:
		model = ReservaPadel
		fields = ['fecha', 'hora_inicio', 'hora_fin']
		widgets = {
			'fecha' : forms.SelectDateWidget(),
			'hora_inicio' : forms.TimeInput(attrs={'type': 'time'}),
			'hora_fin' : forms.TimeInput(attrs={'type': 'time'}),
		}