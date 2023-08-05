from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from mc2.controllers.base.models import (
    Controller, EnvVariable, MarathonLabel, AdditionalLink)
from mc2.organizations.models import Organization


class ControllerForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(optional)'}),
        required=False)
    marathon_cmd = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    marathon_cpus = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': settings.MESOS_DEFAULT_CPU_SHARE}))
    marathon_mem = forms.FloatField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': settings.MESOS_DEFAULT_MEMORY_ALLOCATION}))
    marathon_instances = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': settings.MESOS_DEFAULT_INSTANCES}))
    webhook_token = forms.UUIDField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}))
    postgres_db_needed = forms.BooleanField(
        required=False,
        label="Do you need a Postgres database? (Not yet functional)",
        initial=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]))
    rabbitmq_vhost_needed = forms.BooleanField(
        required=False,
        label="Do you need a RabbitMQ Vhost?",
        initial=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]))
    rabbitmq_vhost_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        model = Controller
        fields = (
            'name', 'marathon_cpus', 'marathon_mem', 'marathon_instances',
            'marathon_cmd', 'webhook_token', 'description', 'organization',
            'postgres_db_needed', 'rabbitmq_vhost_needed',
            'rabbitmq_vhost_name')

    def clean_rabbitmq_vhost_name(self):
        rabbitmq_vhost_needed = self.cleaned_data.get('rabbitmq_vhost_needed')
        rabbitmq_vhost_name = self.cleaned_data.get('rabbitmq_vhost_name')
        if rabbitmq_vhost_needed:
            if not rabbitmq_vhost_name:
                raise forms.ValidationError("vhost name is required.")
        return rabbitmq_vhost_name


class CustomInlineFormset(forms.BaseInlineFormSet):
    """
    Custom formset that support initial data
    """

    def initial_form_count(self):
        """
        set 0 to use initial_extra explicitly.
        """
        if self.initial_extra:
            return 0
        else:
            return forms.BaseInlineFormSet.initial_form_count(self)

    def total_form_count(self):
        """
        here use the initial_extra len to determine needed forms
        """
        if self.initial_extra:
            count = len(self.initial_extra) if self.initial_extra else 0
            count += self.extra
            return count
        else:
            return forms.BaseInlineFormSet.total_form_count(self)


class EnvVariableForm(forms.ModelForm):
    key = forms.RegexField(
        "^[0-9a-zA-Z_]+$", required=True, error_messages={
            'invalid':
                _("You did not enter a valid key. Please try again.")},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def has_changed(self):
        """
        Returns True if we have initial data.
        """
        has_changed = forms.ModelForm.has_changed(self)
        return bool(self.initial or has_changed)

    class Meta:
        model = EnvVariable
        fields = ('key', 'value')


EnvVariableInlineFormSet = forms.inlineformset_factory(
    Controller,
    EnvVariable,
    form=EnvVariableForm,
    formset=CustomInlineFormset,
    extra=1,
    can_delete=True,
    can_order=False
)


class MarathonLabelForm(forms.ModelForm):
    name = forms.RegexField(
        "^[0-9a-zA-Z_.]+$", required=True, error_messages={
            'invalid':
                _("You did not enter a valid key. Please try again.")},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def has_changed(self):
        """
        Returns True if we have initial data.
        """
        has_changed = forms.ModelForm.has_changed(self)
        return bool(self.initial or has_changed)

    class Meta:
        model = MarathonLabel
        fields = ('name', 'value')


MarathonLabelInlineFormSet = forms.inlineformset_factory(
    Controller,
    MarathonLabel,
    form=MarathonLabelForm,
    formset=CustomInlineFormset,
    extra=1,
    can_delete=True,
    can_order=False
)


class AdditionalLinkForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    link = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def has_changed(self):
        """
        Returns True if we have initial data.
        """
        has_changed = forms.ModelForm.has_changed(self)
        return bool(self.initial or has_changed)

    class Meta:
        model = AdditionalLink
        fields = ('name', 'link')


AdditionalLinkInlineFormSet = forms.inlineformset_factory(
    Controller,
    AdditionalLink,
    form=AdditionalLinkForm,
    formset=CustomInlineFormset,
    extra=1,
    can_delete=True,
    can_order=False
)


class ControllerFormHelper(object):

    def __init__(self, data=None, files=None, instance=None,
                 prefix=None, initial={}):
        self.instance = instance
        self.controller_form = ControllerForm(
            data, files,
            instance=instance, initial=initial)

        initial_env = initial.get('envs', [])
        initial_label = initial.get('labels', [])
        initial_link = initial.get('links', [])

        self.env_formset = EnvVariableInlineFormSet(
            data, files,
            instance=instance,
            prefix='env',
            initial=initial_env)

        self.label_formset = MarathonLabelInlineFormSet(
            data, files,
            instance=instance,
            prefix='label',
            initial=initial_label)

        self.link_formset = AdditionalLinkInlineFormSet(
            data, files,
            instance=instance,
            prefix='link',
            initial=initial_link)

    def __iter__(self):
        yield self.controller_form
        yield self.env_formset
        yield self.label_formset
        yield self.link_formset

    def is_valid(self):
        return all(form.is_valid() for form in self)

    def save(self):
        return [form.save() for form in self]
