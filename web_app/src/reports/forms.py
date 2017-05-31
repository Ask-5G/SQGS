from django import forms
from django.forms import ModelMultipleChoiceField, ModelChoiceField

from organization.models import *
from basemodel.models import *

def get_plant_list(plant=''):
	if plant != '':
		plant_list = Plants.objects.filter(id=plant)
	else:
		plant_list = Plants.objects.all()
	return plant_list

def get_market_list(plant='', base='', model='', station=''):
	if plant != '':
		models = get_model_list(plant)
		if base != '':
			if model != '':
				if station != '':
					models_list = ModelStations.objects.filter(station=station).filter(id=model).values_list('model', flat=True)
					models = models.filter(base_models=base).filter(id__in=set(models_list))
				else:
					models = models.filter(base_models=base).filter(id=model)
			else:
				if station != '':
					models_list = ModelStations.objects.filter(station=station).values_list('model', flat=True)
					models = models.filter(base_models=base).filter(id__in=set(models_list))
				else:
					models = models.filter(base_models=base)
		else:
			if model != '':
				if station != '':
					models_list = ModelStations.objects.filter(station=station).filter(model=model).values_list('model', flat=True)
					models = models.filter(id__in=models_list)
				else:
					models = models.filter(id=model)
		return Market.objects.filter(id__in=models.values_list('market', flat=True))
	else:
		if base != '':
			if model != '':
				models = Models.objects.filter(base_models=base).filter(id=model)
			else:
				models = Models.objects.filter(base_models=base)
			return Market.objects.filter(id__in=models.values_list('market', flat=True))
		else:
			if model != '':
				models = Models.objects.filter(id=model)
				return Market.objects.filter(id__in=models.values_list('market', flat=True))
			else:
				return Market.objects.all()

def get_shift_list(plant=''):
	if plant != '':
		return Shifts.objects.filter(plants=plant)
	else:
		return Shifts.objects.all()

def get_base_list(plant='', market='', model='', station=''):
	models = get_model_list(plant)	
	if market != '':
		if model != '':
			if station != '':
				model_list= ModelStations.objects.filter(station=station).filter(model=model).values_list('model', flat=True)
				models = models.filter(market=market).filter(id__in=set(model_list))
			else:
				models = models.filter(market=market).filter(id=model)
		else:
			if station != '':
				model_list= ModelStations.objects.filter(station=station).values_list('model', flat=True)
				models = models.filter(market=market).filter(id__in=set(model_list))
			else:
				models = models.filter(market=market)

	return BaseModels.objects.filter(id__in=models.values_list('base_models', flat=True))
	
def get_model_list(plant='', market='', base='', station=''):
	if plant != '':
		model_stations = ModelStations.objects.filter(station__cells__plants=plant)
		models = model_stations.values_list('model', flat=True)
		if market != '':
			if base != '':
				if station != '':
					models = model_stations.filter(station=station).values_list('model', flat=True)
					return Models.objects.filter(id__in=set(models)).filter(market=market).filter(base_models=base)
				else:
					return Models.objects.filter(id__in=set(models)).filter(market=market).filter(base_models=base)
			else:
				if station != '':
					models = model_stations.filter(station=station).values_list('model', flat=True)
					return Models.objects.filter(id__in=set(models)).filter(market=market)
				else:
					return Models.objects.filter(id__in=set(models)).filter(market=market)
		else:
			if base != '':
				if station != '':
					models = model_stations.filter(station=station).values_list('model', flat=True)
					return Models.objects.filter(id__in=set(models)).filter(base_models=base)
				else:
					return Models.objects.filter(id__in=set(models)).filter(base_models=base)
			else:
				if station != '':
					models = model_stations.filter(station=station).values_list('model', flat=True)
					return Models.objects.filter(id__in=set(models))
				else:
					return Models.objects.filter(id__in=set(models))
	else:
		if market != '':
			return Models.objects.filter(market=market)
		else:
			return Models.objects.all()

def get_station_list(plant='', market='', base='', model=''):
	if plant != '':
		if market != '':
			models = Models.objects.filter(market=market)
			if base != '':
				if model != '':
					models = models.filter(base_models=base)
					stations = ModelStations.objects.filter(model__in=models.filter(id=model)).values_list('station', flat=True)		
				else:
					stations = ModelStations.objects.filter(model__in=models.filter(base_models=base)).values_list('station', flat=True)
			else:
				if model != '':
					models = models.filter(id=model)
					stations = ModelStations.objects.filter(model__in=models).values_list('station', flat=True)
				else:
					stations = ModelStations.objects.filter(model__in=models).values_list('station', flat=True)
			return Stations.objects.filter(cells__plants=plant).filter(id__in=set(stations))
		else:
			if base != '':
				if model != '':
					model_stations = ModelStations.objects.filter(station__cells__plants=plant)
					station_list = model_stations.filter(model__base_models=base).filter(model=model).values_list('station', flat=True)	
				else:
					model_stations = ModelStations.objects.filter(station__cells__plants=plant)
					station_list = model_stations.filter(model__base_models=base).values_list('station', flat=True)
					return Stations.objects.filter(id__in=set(station_list))
			else:
				return Stations.objects.filter(cells__plants=plant)
	else:
		if market != '':
			stations = ModelStations.objects.filter(model__in=Models.objects.filter(market=market)).values_list('station', flat=True)
			return Stations.objects.filter(id__in=set(stations))
		else:
			return Stations.objects.all()

def get_sourcegate_list():
    return SourceGates.objects.all()

class PlantChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.plant_name

class MarketChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class ShiftChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class BaseModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class ModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class StationChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class SourceGatesChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s" % obj.description

class RftRolldownFilterForm(forms.Form):

	rft_rolldown_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	rft_rolldown_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	rft_rolldown_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	rft_rolldown_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	rft_rolldown_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	rft_rolldown_stations = StationChoiceField(
		queryset=Stations.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(RftRolldownFilterForm, self).__init__(*args)
		self.fields['rft_rolldown_plants'].widget.attrs = {'id': 'id_rft_rolldown_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['rft_rolldown_markets'].widget.attrs = {'id': 'id_rft_rolldown_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['rft_rolldown_shifts'].widget.attrs = {'id': 'id_rft_rolldown_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['rft_rolldown_base_models'].widget.attrs = {'id': 'id_rft_rolldown_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['rft_rolldown_models'].widget.attrs = {'id': 'id_rft_rolldown_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['rft_rolldown_stations'].widget.attrs = {'id': 'id_rft_rolldown_stations', 'class': 'form-control','help_texts':'Choose Stations', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['rft_rolldown_plants'].queryset = get_plant_list(plant.id)
				self.fields['rft_rolldown_plants'].initial = plant.id
				self.fields['rft_rolldown_plants'].disabled = True
				self.fields['rft_rolldown_markets'].queryset = get_market_list(plant.id, initial['rft_rolldown_base_models'], initial['rft_rolldown_models'], initial['rft_rolldown_stations'])
				self.fields['rft_rolldown_shifts'].queryset = get_shift_list(plant.id)
				self.fields['rft_rolldown_base_models'].queryset = get_base_list(plant.id, initial['rft_rolldown_markets'], initial['rft_rolldown_models'], initial['rft_rolldown_stations'])
				self.fields['rft_rolldown_models'].queryset = get_model_list(plant.id, initial['rft_rolldown_markets'], initial['rft_rolldown_base_models'], initial['rft_rolldown_stations'])
				self.fields['rft_rolldown_stations'].queryset = get_station_list(plant.id, initial['rft_rolldown_markets'], initial['rft_rolldown_base_models'], initial['rft_rolldown_models'])
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['rft_rolldown_plants'].queryset = get_plant_list(plant)
			self.fields['rft_rolldown_plants'].initial = plant
			self.fields['rft_rolldown_plants'].disabled = True
			self.fields['rft_rolldown_markets'].queryset = get_market_list(plant)
			self.fields['rft_rolldown_shifts'].queryset = get_shift_list(plant)
			self.fields['rft_rolldown_base_models'].queryset = get_base_list(plant)
			self.fields['rft_rolldown_models'].queryset = get_model_list(plant)
			self.fields['rft_rolldown_stations'].queryset = get_station_list(plant)
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				self.fields['rft_rolldown_plants'].queryset = get_plant_list()
				self.fields['rft_rolldown_plants'].initial = initial['rft_rolldown_plants']

				if initial['rft_rolldown_plants'] == '':
					self.fields['rft_rolldown_markets'].disabled = True
					self.fields['rft_rolldown_shifts'].disabled = True
					self.fields['rft_rolldown_base_models'].disabled = True
					self.fields['rft_rolldown_models'].disabled = True
					self.fields['rft_rolldown_stations'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['rft_rolldown_markets'].queryset = get_market_list(initial['rft_rolldown_plants'], initial['rft_rolldown_base_models'], initial['rft_rolldown_models'], initial['rft_rolldown_stations'])
						self.fields['rft_rolldown_shifts'].queryset = get_shift_list(initial['rft_rolldown_plants'])
						self.fields['rft_rolldown_base_models'].queryset = get_base_list(initial['rft_rolldown_plants'], initial['rft_rolldown_markets'], initial['rft_rolldown_models'], initial['rft_rolldown_stations'])
						self.fields['rft_rolldown_models'].queryset = get_model_list(initial['rft_rolldown_plants'], initial['rft_rolldown_markets'], initial['rft_rolldown_base_models'], initial['rft_rolldown_stations'])
						self.fields['rft_rolldown_stations'].queryset = get_station_list(initial['rft_rolldown_plants'], initial['rft_rolldown_markets'], initial['rft_rolldown_base_models'], initial['rft_rolldown_models'])
					else:
						self.fields['rft_rolldown_markets'].enabled = True
						self.fields['rft_rolldown_markets'].queryset = get_market_list(initial['rft_rolldown_plants'])
						self.fields['rft_rolldown_shifts'].enabled = True
						self.fields['rft_rolldown_shifts'].queryset = get_shift_list(initial['rft_rolldown_plants'])
						self.fields['rft_rolldown_base_models'].enabled = True
						self.fields['rft_rolldown_base_models'].queryset = get_base_list(initial['rft_rolldown_plants'])
						self.fields['rft_rolldown_models'].enabled = True
						self.fields['rft_rolldown_models'].queryset = get_model_list(initial['rft_rolldown_plants'])
						self.fields['rft_rolldown_stations'].enabled = True
						self.fields['rft_rolldown_stations'].queryset = get_station_list(initial['rft_rolldown_plants'])
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['rft_rolldown_plants'].queryset = get_plant_list()
			self.fields['rft_rolldown_markets'].queryset = get_market_list()
			self.fields['rft_rolldown_markets'].disabled = True
			self.fields['rft_rolldown_shifts'].queryset = get_shift_list()
			self.fields['rft_rolldown_shifts'].disabled = True
			self.fields['rft_rolldown_base_models'].queryset = get_base_list()
			self.fields['rft_rolldown_base_models'].disabled = True
			self.fields['rft_rolldown_models'].queryset = get_model_list()
			self.fields['rft_rolldown_models'].disabled = True
			self.fields['rft_rolldown_stations'].queryset = get_station_list()
			self.fields['rft_rolldown_stations'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			for field in ['rft_rolldown_markets', 'rft_rolldown_shifts', 'rft_rolldown_base_models', 'rft_rolldown_models', 'rft_rolldown_stations']:
				self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass

class RftFinalFilterForm(forms.Form):

	rft_final_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	rft_final_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	rft_final_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	rft_final_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	rft_final_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	rft_final_stations = StationChoiceField(
		queryset=Stations.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(RftFinalFilterForm, self).__init__(*args)
		self.fields['rft_final_plants'].widget.attrs = {'id': 'id_rft_final_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['rft_final_markets'].widget.attrs = {'id': 'id_rft_final_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['rft_final_shifts'].widget.attrs = {'id': 'id_rft_final_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['rft_final_base_models'].widget.attrs = {'id': 'id_rft_final_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['rft_final_models'].widget.attrs = {'id': 'id_rft_final_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['rft_final_stations'].widget.attrs = {'id': 'id_rft_final_stations', 'class': 'form-control','help_texts':'Choose Stations', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['rft_final_plants'].queryset = get_plant_list(plant.id)
				self.fields['rft_final_plants'].initial = plant.id
				self.fields['rft_final_plants'].disabled = True
				self.fields['rft_final_markets'].queryset = get_market_list(plant.id, initial['rft_final_base_models'], initial['rft_final_models'])
				self.fields['rft_final_shifts'].queryset = get_shift_list(plant.id)
				self.fields['rft_final_base_models'].queryset = get_base_list(plant.id, initial['rft_final_markets'], initial['rft_final_models'])
				self.fields['rft_final_models'].queryset = get_model_list(plant.id, initial['rft_final_markets'], initial['rft_final_base_models'])
				self.fields['rft_final_stations'].queryset = get_station_list(plant.id, initial['rft_final_markets'], initial['rft_final_base_models'], initial['rft_final_models'])
				self.fields['rft_final_stations'].disabled = True
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['rft_final_plants'].queryset = get_plant_list(plant)
			self.fields['rft_final_plants'].initial = plant
			self.fields['rft_final_plants'].disabled = True
			self.fields['rft_final_markets'].queryset = get_market_list(plant)
			self.fields['rft_final_shifts'].queryset = get_shift_list(plant)
			self.fields['rft_final_base_models'].queryset = get_base_list(plant)
			self.fields['rft_final_models'].queryset = get_model_list(plant)
			self.fields['rft_final_stations'].queryset = get_station_list(plant)
			self.fields['rft_final_stations'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				self.fields['rft_final_plants'].queryset = get_plant_list()
				self.fields['rft_final_plants'].initial = initial['rft_final_plants']

				if initial['rft_final_plants'] == '':
					self.fields['rft_final_markets'].disabled = True
					self.fields['rft_final_shifts'].disabled = True
					self.fields['rft_final_base_models'].disabled = True
					self.fields['rft_final_models'].disabled = True
					self.fields['rft_final_stations'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['rft_final_markets'].queryset = get_market_list(initial['rft_final_plants'], initial['rft_final_base_models'], initial['rft_final_models'])
						self.fields['rft_final_shifts'].queryset = get_shift_list(initial['rft_final_plants'])
						self.fields['rft_final_base_models'].queryset = get_base_list(initial['rft_final_plants'], initial['rft_final_markets'], initial['rft_final_models'])
						self.fields['rft_final_models'].queryset = get_model_list(initial['rft_final_plants'], initial['rft_final_markets'], initial['rft_final_base_models'])
						self.fields['rft_final_stations'].queryset = get_station_list(initial['rft_final_plants'], initial['rft_final_markets'], initial['rft_final_base_models'], initial['rft_final_models'])
						self.fields['rft_final_stations'].disabled = True
					else:
						self.fields['rft_final_markets'].enabled = True
						self.fields['rft_final_markets'].queryset = get_market_list(initial['rft_final_plants'])
						self.fields['rft_final_shifts'].enabled = True
						self.fields['rft_final_shifts'].queryset = get_shift_list(initial['rft_final_plants'])
						self.fields['rft_final_base_models'].enabled = True
						self.fields['rft_final_base_models'].queryset = get_base_list(initial['rft_final_plants'])
						self.fields['rft_final_models'].enabled = True
						self.fields['rft_final_models'].queryset = get_model_list(initial['rft_final_plants'])
						self.fields['rft_final_stations'].queryset = get_station_list(initial['rft_final_plants'])
						self.fields['rft_final_stations'].disabled = True
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['rft_final_plants'].queryset = get_plant_list()
			self.fields['rft_final_markets'].queryset = get_market_list()
			self.fields['rft_final_markets'].disabled = True
			self.fields['rft_final_shifts'].queryset = get_shift_list()
			self.fields['rft_final_shifts'].disabled = True
			self.fields['rft_final_base_models'].queryset = get_base_list()
			self.fields['rft_final_base_models'].disabled = True
			self.fields['rft_final_models'].queryset = get_model_list()
			self.fields['rft_final_models'].disabled = True
			self.fields['rft_final_stations'].queryset = get_station_list()
			self.fields['rft_final_stations'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			if len(initial) > 2:
				for field in ['rft_final_markets', 'rft_final_shifts', 'rft_final_base_models', 'rft_final_models']:
					self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass			

class RftOverallFilterForm(forms.Form):

	rft_overall_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	rft_overall_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	rft_overall_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	rft_overall_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	rft_overall_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	rft_overall_stations = StationChoiceField(
		queryset=Stations.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(RftOverallFilterForm, self).__init__(*args)
		self.fields['rft_overall_plants'].widget.attrs = {'id': 'id_rft_overall_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['rft_overall_markets'].widget.attrs = {'id': 'id_rft_overall_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['rft_overall_shifts'].widget.attrs = {'id': 'id_rft_overall_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['rft_overall_base_models'].widget.attrs = {'id': 'id_rft_ovarall_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['rft_overall_models'].widget.attrs = {'id': 'id_rft_overall_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['rft_overall_stations'].widget.attrs = {'id': 'id_rft_overall_stations', 'class': 'form-control','help_texts':'Choose Stations', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['rft_overall_plants'].queryset = get_plant_list(plant.id)
				self.fields['rft_overall_plants'].initial = plant.id
				self.fields['rft_overall_plants'].disabled = True
				self.fields['rft_overall_markets'].queryset = get_market_list(plant.id, initial['rft_overall_base_models'], initial['rft_overall_models'])
				self.fields['rft_overall_shifts'].queryset = get_shift_list(plant.id)
				self.fields['rft_overall_base_models'].queryset = get_base_list(plant.id, initial['rft_overall_markets'], initial['rft_overall_models'])
				self.fields['rft_overall_models'].queryset = get_model_list(plant.id, initial['rft_overall_markets'], initial['rft_overall_base_models'])
				self.fields['rft_overall_stations'].queryset = get_station_list(plant.id, initial['rft_overall_markets'], initial['rft_overall_base_models'], initial['rft_overall_models'])
				self.fields['rft_overall_stations'].disabled = True
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['rft_overall_plants'].queryset = get_plant_list(plant)
			self.fields['rft_overall_plants'].initial = plant
			self.fields['rft_overall_plants'].disabled = True
			self.fields['rft_overall_markets'].queryset = get_market_list(plant)
			self.fields['rft_overall_shifts'].queryset = get_shift_list(plant)
			self.fields['rft_overall_base_models'].queryset = get_base_list(plant)
			self.fields['rft_overall_models'].queryset = get_model_list(plant)
			self.fields['rft_overall_stations'].queryset = get_station_list(plant)
			self.fields['rft_overall_stations'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				self.fields['rft_overall_plants'].queryset = get_plant_list()
				self.fields['rft_overall_plants'].initial = initial['rft_overall_plants']

				if initial['rft_overall_plants'] == '':
					self.fields['rft_overall_markets'].disabled = True
					self.fields['rft_overall_shifts'].disabled = True
					self.fields['rft_overall_base_models'].disabled = True
					self.fields['rft_overall_models'].disabled = True
					self.fields['rft_overall_stations'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['rft_overall_markets'].queryset = get_market_list(initial['rft_overall_plants'], initial['rft_overall_base_models'], initial['rft_overall_models'])
						self.fields['rft_overall_shifts'].queryset = get_shift_list(initial['rft_overall_plants'])
						self.fields['rft_overall_base_models'].queryset = get_base_list(initial['rft_overall_plants'], initial['rft_overall_markets'], initial['rft_overall_models'])
						self.fields['rft_overall_models'].queryset = get_model_list(initial['rft_overall_plants'], initial['rft_overall_markets'], initial['rft_overall_base_models'])
						self.fields['rft_overall_stations'].queryset = get_station_list(initial['rft_overall_plants'], initial['rft_overall_markets'], initial['rft_overall_base_models'])
						self.fields['rft_overall_stations'].disabled = True
					else:
						self.fields['rft_overall_markets'].enabled = True
						self.fields['rft_overall_markets'].queryset = get_market_list(initial['rft_overall_plants'])
						self.fields['rft_overall_shifts'].enabled = True
						self.fields['rft_overall_shifts'].queryset = get_shift_list(initial['rft_overall_plants'])
						self.fields['rft_overall_base_models'].enabled = True
						self.fields['rft_overall_base_models'].queryset = get_base_list(initial['rft_overall_plants'])
						self.fields['rft_overall_models'].enabled = True
						self.fields['rft_overall_models'].queryset = get_model_list(initial['rft_overall_plants'])
						self.fields['rft_overall_stations'].queryset = get_station_list(initial['rft_overall_plants'])
						self.fields['rft_overall_stations'].disabled = True
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['rft_overall_plants'].queryset = get_plant_list()
			self.fields['rft_overall_markets'].queryset = get_market_list()
			self.fields['rft_overall_markets'].disabled = True
			self.fields['rft_overall_shifts'].queryset = get_shift_list()
			self.fields['rft_overall_shifts'].disabled = True
			self.fields['rft_overall_base_models'].queryset = get_base_list()
			self.fields['rft_overall_base_models'].disabled = True
			self.fields['rft_overall_models'].queryset = get_model_list()
			self.fields['rft_overall_models'].disabled = True
			self.fields['rft_overall_stations'].queryset = get_station_list()
			self.fields['rft_overall_stations'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			if len(initial) > 2:
				for field in ['rft_overall_markets', 'rft_overall_shifts', 'rft_overall_base_models', 'rft_overall_models']:
					self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass						

class DpuRolldownFilterForm(forms.Form):

	dpu_rolldown_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	dpu_rolldown_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	dpu_rolldown_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	dpu_rolldown_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	dpu_rolldown_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	dpu_rolldown_sourcegates = SourceGatesChoiceField(
		queryset=SourceGates.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(DpuRolldownFilterForm, self).__init__(*args)
		self.fields['dpu_rolldown_plants'].widget.attrs = {'id': 'id_dpu_rolldown_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['dpu_rolldown_markets'].widget.attrs = {'id': 'id_dpu_rolldown_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['dpu_rolldown_shifts'].widget.attrs = {'id': 'id_dpu_rolldown_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['dpu_rolldown_base_models'].widget.attrs = {'id': 'id_dpu_rolldown_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['dpu_rolldown_models'].widget.attrs = {'id': 'id_dpu_rolldown_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['dpu_rolldown_sourcegates'].widget.attrs = {'id': 'id_dpu_rolldown_sourcegates', 'class': 'form-control','help_texts':'Choose SourceGates', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['dpu_rolldown_plants'].queryset = get_plant_list(plant.id)
				self.fields['dpu_rolldown_plants'].initial = plant.id
				self.fields['dpu_rolldown_plants'].disabled = True
				self.fields['dpu_rolldown_markets'].queryset = get_market_list(plant.id, initial['dpu_rolldown_base_models'], initial['dpu_rolldown_models'], initial['dpu_rolldown_sourcegates'])
				self.fields['dpu_rolldown_shifts'].queryset = get_shift_list(plant.id)
				self.fields['dpu_rolldown_base_models'].queryset = get_base_list(plant.id, initial['dpu_rolldown_markets'], initial['dpu_rolldown_models'], initial['dpu_rolldown_sourcegates'])
				self.fields['dpu_rolldown_models'].queryset = get_model_list(plant.id, initial['dpu_rolldown_markets'], initial['dpu_rolldown_base_models'], initial['dpu_rolldown_sourcegates'])
				self.fields['dpu_rolldown_sourcegates'].queryset = get_sourcegate_list()
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['dpu_rolldown_plants'].queryset = get_plant_list(plant)
			self.fields['dpu_rolldown_plants'].initial = plant
			self.fields['dpu_rolldown_plants'].disabled = True
			self.fields['dpu_rolldown_markets'].queryset = get_market_list(plant)
			self.fields['dpu_rolldown_shifts'].queryset = get_shift_list(plant)
			self.fields['dpu_rolldown_base_models'].queryset = get_base_list(plant)
			self.fields['dpu_rolldown_models'].queryset = get_model_list(plant)
			self.fields['dpu_rolldown_sourcegates'].queryset = get_sourcegate_list()
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				# import pdb;pdb.set_trace()
				self.fields['dpu_rolldown_plants'].queryset = get_plant_list()
				self.fields['dpu_rolldown_plants'].initial = initial['dpu_rolldown_plants']
                
				if initial['dpu_rolldown_plants'] == '':
					self.fields['dpu_rolldown_markets'].disabled = True
					self.fields['dpu_rolldown_shifts'].disabled = True
					self.fields['dpu_rolldown_base_models'].disabled = True
					self.fields['dpu_rolldown_models'].disabled = True
					self.fields['dpu_rolldown_sourcegates'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['dpu_rolldown_markets'].queryset = get_market_list(initial['dpu_rolldown_plants'], initial['dpu_rolldown_base_models'], initial['dpu_rolldown_models'], initial['dpu_rolldown_sourcegates'])
						self.fields['dpu_rolldown_shifts'].queryset = get_shift_list(initial['dpu_rolldown_plants'])
						self.fields['dpu_rolldown_base_models'].queryset = get_base_list(initial['dpu_rolldown_plants'], initial['dpu_rolldown_markets'], initial['dpu_rolldown_models'], initial['dpu_rolldown_sourcegates'])
						self.fields['dpu_rolldown_models'].queryset = get_model_list(initial['dpu_rolldown_plants'], initial['dpu_rolldown_markets'], initial['dpu_rolldown_base_models'], initial['dpu_rolldown_sourcegates'])
						self.fields['dpu_rolldown_sourcegates'].queryset = get_sourcegate_list()
					else:
						self.fields['dpu_rolldown_markets'].enabled = True
						self.fields['dpu_rolldown_markets'].queryset = get_market_list(initial['dpu_rolldown_plants'])
						self.fields['dpu_rolldown_shifts'].enabled = True
						self.fields['dpu_rolldown_shifts'].queryset = get_shift_list(initial['dpu_rolldown_plants'])
						self.fields['dpu_rolldown_base_models'].enabled = True
						self.fields['dpu_rolldown_base_models'].queryset = get_base_list(initial['dpu_rolldown_plants'])
						self.fields['dpu_rolldown_models'].enabled = True
						self.fields['dpu_rolldown_models'].queryset = get_model_list(initial['dpu_rolldown_plants'])
						self.fields['dpu_rolldown_sourcegates'].enabled = True
						self.fields['dpu_rolldown_sourcegates'].queryset = get_sourcegate_list()
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['dpu_rolldown_plants'].queryset = get_plant_list()
			self.fields['dpu_rolldown_markets'].queryset = get_market_list()
			self.fields['dpu_rolldown_markets'].disabled = True
			self.fields['dpu_rolldown_shifts'].queryset = get_shift_list()
			self.fields['dpu_rolldown_shifts'].disabled = True
			self.fields['dpu_rolldown_base_models'].queryset = get_base_list()
			self.fields['dpu_rolldown_base_models'].disabled = True
			self.fields['dpu_rolldown_models'].queryset = get_model_list()
			self.fields['dpu_rolldown_models'].disabled = True
			self.fields['dpu_rolldown_sourcegates'].queryset = get_sourcegate_list()
			self.fields['dpu_rolldown_sourcegates'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			for field in ['dpu_rolldown_markets', 'dpu_rolldown_shifts', 'dpu_rolldown_base_models', 'dpu_rolldown_models', 'dpu_rolldown_sourcegates']:
				self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass			


class DpuFinalFilterForm(forms.Form):

	dpu_final_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	dpu_final_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	dpu_final_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	dpu_final_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	dpu_final_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	dpu_final_sourcegates = SourceGatesChoiceField(
		queryset=SourceGates.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(DpuFinalFilterForm, self).__init__(*args)
		self.fields['dpu_final_plants'].widget.attrs = {'id': 'id_dpu_final_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['dpu_final_markets'].widget.attrs = {'id': 'id_dpu_final_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['dpu_final_shifts'].widget.attrs = {'id': 'id_dpu_final_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['dpu_final_base_models'].widget.attrs = {'id': 'id_dpu_final_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['dpu_final_models'].widget.attrs = {'id': 'id_dpu_final_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['dpu_final_sourcegates'].widget.attrs = {'id': 'id_dpu_final_sourcegates', 'class': 'form-control','help_texts':'Choose SourceGates', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['dpu_final_plants'].queryset = get_plant_list(plant.id)
				self.fields['dpu_final_plants'].initial = plant.id
				self.fields['dpu_final_plants'].disabled = True
				self.fields['dpu_final_markets'].queryset = get_market_list(plant.id, initial['dpu_final_base_models'], initial['dpu_final_models'])
				self.fields['dpu_final_shifts'].queryset = get_shift_list(plant.id)
				self.fields['dpu_final_base_models'].queryset = get_base_list(plant.id, initial['dpu_final_markets'], initial['dpu_final_models'])
				self.fields['dpu_final_models'].queryset = get_model_list(plant.id, initial['dpu_final_markets'], initial['dpu_final_base_models'])
				self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
				#self.fields['dpu_final_sourcegates'].disabled = True
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['dpu_final_plants'].queryset = get_plant_list(plant)
			self.fields['dpu_final_plants'].initial = plant
			self.fields['dpu_final_plants'].disabled = True
			self.fields['dpu_final_markets'].queryset = get_market_list(plant)
			self.fields['dpu_final_shifts'].queryset = get_shift_list(plant)
			self.fields['dpu_final_base_models'].queryset = get_base_list(plant)
			self.fields['dpu_final_models'].queryset = get_model_list(plant)
			self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
			#self.fields['dpu_final_sourcegates'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				self.fields['dpu_final_plants'].queryset = get_plant_list()
				self.fields['dpu_final_plants'].initial = initial['dpu_final_plants']

				if initial['dpu_final_plants'] == '':
					self.fields['dpu_final_markets'].disabled = True
					self.fields['dpu_final_shifts'].disabled = True
					self.fields['dpu_final_base_models'].disabled = True
					self.fields['dpu_final_models'].disabled = True
					self.fields['dpu_final_sourcegates'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['dpu_final_markets'].queryset = get_market_list(initial['dpu_final_plants'], initial['dpu_final_base_models'], initial['dpu_final_models'])
						self.fields['dpu_final_shifts'].queryset = get_shift_list(initial['dpu_final_plants'])
						self.fields['dpu_final_base_models'].queryset = get_base_list(initial['dpu_final_plants'], initial['dpu_final_markets'], initial['dpu_final_models'])
						self.fields['dpu_final_models'].queryset = get_model_list(initial['dpu_final_plants'], initial['dpu_final_markets'], initial['dpu_final_base_models'])
						self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
						self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
					else:
						self.fields['dpu_final_markets'].enabled = True
						self.fields['dpu_final_markets'].queryset = get_market_list(initial['dpu_final_plants'])
						self.fields['dpu_final_shifts'].enabled = True
						self.fields['dpu_final_shifts'].queryset = get_shift_list(initial['dpu_final_plants'])
						self.fields['dpu_final_base_models'].enabled = True
						self.fields['dpu_final_base_models'].queryset = get_base_list(initial['dpu_final_plants'])
						self.fields['dpu_final_models'].enabled = True
						self.fields['dpu_final_models'].queryset = get_model_list(initial['dpu_final_plants'])
						self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
						self.fields['dpu_final_sourcegates'].enabled = True
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['dpu_final_plants'].queryset = get_plant_list()
			self.fields['dpu_final_markets'].queryset = get_market_list()
			self.fields['dpu_final_markets'].disabled = True
			self.fields['dpu_final_shifts'].queryset = get_shift_list()
			self.fields['dpu_final_shifts'].disabled = True
			self.fields['dpu_final_base_models'].queryset = get_base_list()
			self.fields['dpu_final_base_models'].disabled = True
			self.fields['dpu_final_models'].queryset = get_model_list()
			self.fields['dpu_final_models'].disabled = True
			self.fields['dpu_final_sourcegates'].queryset = get_sourcegate_list()
			self.fields['dpu_final_sourcegates'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			if len(initial) > 2:
				for field in ['dpu_final_markets', 'dpu_final_shifts', 'dpu_final_base_models', 'dpu_final_models','dpu_final_sourcegates']:
					self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass			

class DpuOverallFilterForm(forms.Form):

	dpu_overall_plants = PlantChoiceField(
		queryset=get_plant_list(),
		empty_label="All"
	)
	dpu_overall_markets = MarketChoiceField(
		queryset=Market.objects.none(),
		empty_label="All"
	)
	dpu_overall_shifts = ShiftChoiceField(
		queryset=Shifts.objects.none(),
		empty_label="All"
	)
	dpu_overall_base_models = BaseModelChoiceField(
		queryset=BaseModels.objects.none(),
		empty_label="All"
	)
	dpu_overall_models = ModelChoiceField(
		queryset=Models.objects.none(),
		empty_label="All"
	)
	dpu_overall_sourcegates = SourceGatesChoiceField(
		queryset=SourceGates.objects.none(),
		empty_label="All"
	)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		initial = kwargs.get('initial', {})
		super(DpuOverallFilterForm, self).__init__(*args)
		self.fields['dpu_overall_plants'].widget.attrs = {'id': 'id_dpu_overall_plants', 'class': 'form-control','help_texts':'Choose Plants', 'data-live-search': "true"}
		self.fields['dpu_overall_markets'].widget.attrs = {'id': 'id_dpu_overall_markets', 'class': 'form-control','help_texts':'Choose Markets', 'data-live-search': "true"}
		self.fields['dpu_overall_shifts'].widget.attrs = {'id': 'id_dpu_overall_shifts', 'class': 'form-control','help_texts':'Choose Shifts', 'data-live-search': "true"}
		self.fields['dpu_overall_base_models'].widget.attrs = {'id': 'id_dpu_ovarall_base_models', 'class': 'form-control','help_texts':'Choose Base Models', 'data-live-search': "true"}
		self.fields['dpu_overall_models'].widget.attrs = {'id': 'id_dpu_overall_models', 'class': 'form-control','help_texts':'Choose Models', 'data-live-search': "true"}
		self.fields['dpu_overall_sourcegates'].widget.attrs = {'id': 'id_dpu_overall_sourcegates', 'class': 'form-control','help_texts':'Choose SourceGates', 'data-live-search': "true"}
		self.form_initialize(user, initial)

	def form_initialize(self, user, initial):
		if user["plant"] != '':
			self.initiate_form_plant(user, initial)
		else:
			self.initiate_form_tafe(initial)
		self.set_initial_value(user, initial)

	def initiate_form_plant(self, user, initial):
		try:
			plant = Plants.objects.get(
				id=user['plant']
			)
			if initial != {}:
				self.fields['dpu_overall_plants'].queryset = get_plant_list(plant.id)
				self.fields['dpu_overall_plants'].initial = plant.id
				self.fields['dpu_overall_plants'].disabled = True
				self.fields['dpu_overall_markets'].queryset = get_market_list(plant.id, initial['dpu_overall_base_models'], initial['dpu_overall_models'])
				self.fields['dpu_overall_shifts'].queryset = get_shift_list(plant.id)
				self.fields['dpu_overall_base_models'].queryset = get_base_list(plant.id, initial['dpu_overall_markets'], initial['dpu_overall_models'])
				self.fields['dpu_overall_models'].queryset = get_model_list(plant.id, initial['dpu_overall_markets'], initial['dpu_overall_base_models'])
				self.fields['dpu_overall_sourcegates'].queryset = get_sourcegate_list()
				self.fields['dpu_overall_sourcegates'].disabled = True
			else:
				self.initiate_plant(plant.id)
		except KeyError:
			pass
		except ValueError:
			pass
		except Plants.DoesNotExist:
			pass

	def initiate_plant(self, plant):
		try:
			self.fields['dpu_overall_plants'].queryset = get_plant_list(plant)
			self.fields['dpu_overall_plants'].initial = plant
			self.fields['dpu_overall_plants'].disabled = True
			self.fields['dpu_overall_markets'].queryset = get_market_list(plant)
			self.fields['dpu_overall_shifts'].queryset = get_shift_list(plant)
			self.fields['dpu_overall_base_models'].queryset = get_base_list(plant)
			self.fields['dpu_overall_models'].queryset = get_model_list(plant)
			self.fields['dpu_overall_sourcegates'].queryset = get_sourcegate_list()
			self.fields['dpu_overall_sourcegates'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def initiate_form_tafe(self, initial):
		try:
			if initial != {}:
				# import pdb;pdb.set_trace()
				self.fields['dpu_overall_plants'].queryset = get_plant_list()
				self.fields['dpu_overall_plants'].initial = initial['dpu_overall_plants']

				if initial['dpu_overall_plants'] == '':
					self.fields['dpu_overall_markets'].disabled = True
					self.fields['dpu_overall_shifts'].disabled = True
					self.fields['dpu_overall_base_models'].disabled = True
					self.fields['dpu_overall_models'].disabled = True
					self.fields['dpu_overall_sourcegates'].disabled = True
				else:
					if len(initial) > 2:
						self.fields['dpu_overall_markets'].queryset = get_market_list(initial['dpu_overall_plants'], initial['dpu_overall_base_models'], initial['dpu_overall_models'])
						self.fields['dpu_overall_shifts'].queryset = get_shift_list(initial['dpu_overall_plants'])
						self.fields['dpu_overall_base_models'].queryset = get_base_list(initial['dpu_overall_plants'], initial['dpu_overall_markets'], initial['dpu_overall_models'])
						self.fields['dpu_overall_models'].queryset = get_model_list(initial['dpu_overall_plants'], initial['dpu_overall_markets'], initial['dpu_overall_base_models'])
						self.fields['dpu_overall_sourcegates'].queryset = get_sourcegate_list()
						#self.fields['dpu_overall_sourcegates'].disabled = True
					else:
						self.fields['dpu_overall_markets'].enabled = True
						self.fields['dpu_overall_markets'].queryset = get_market_list(initial['dpu_overall_plants'])
						self.fields['dpu_overall_shifts'].enabled = True
						self.fields['dpu_overall_shifts'].queryset = get_shift_list(initial['dpu_overall_plants'])
						self.fields['dpu_overall_base_models'].enabled = True
						self.fields['dpu_overall_base_models'].queryset = get_base_list(initial['dpu_overall_plants'])
						self.fields['dpu_overall_models'].enabled = True
						self.fields['dpu_overall_models'].queryset = get_model_list(initial['dpu_overall_plants'])
						self.fields['dpu_overall_sourcegates'].queryset = get_sourcegate_list()
						self.fields['dpu_overall_sourcegates'].enabled = True
			else:
				self.initiate_tafe()
		except KeyError:
			pass
		except ValueError:
			pass
	def initiate_tafe(self):
		try:
			self.fields['dpu_overall_plants'].queryset = get_plant_list()
			self.fields['dpu_overall_markets'].queryset = get_market_list()
			self.fields['dpu_overall_markets'].disabled = True
			self.fields['dpu_overall_shifts'].queryset = get_shift_list()
			self.fields['dpu_overall_shifts'].disabled = True
			self.fields['dpu_overall_base_models'].queryset = get_base_list()
			self.fields['dpu_overall_base_models'].disabled = True
			self.fields['dpu_overall_models'].queryset = get_model_list()
			self.fields['dpu_overall_models'].disabled = True
			self.fields['dpu_overall_sourcegates'].queryset = get_sourcegate_list()
			self.fields['dpu_overall_sourcegates'].disabled = True
		except KeyError:
			pass
		except ValueError:
			pass

	def set_initial_value(self, user, initial):
		try:
			if len(initial) > 2:
				for field in ['dpu_overall_markets', 'dpu_overall_shifts', 'dpu_overall_base_models', 'dpu_overall_models','dpu_overall_sourcegates']:
					self.fields[field].initial = initial[field]
		except KeyError:
			pass
		except ValueError:
			pass						
