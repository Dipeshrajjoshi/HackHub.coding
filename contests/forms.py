from django import forms
from django.forms import inlineformset_factory
from .models import Contest, ProblemLink


# form used by organizers to input contest details
class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'rules', 'start_time', 'end_time']
        # making sure the inputs look like modern bootstrap controls
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contest Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    # custom validation to ensure the contest duration makes sense
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data


# form for individual coding problem links (LeetCode, etc.)
class ProblemLinkForm(forms.ModelForm):
    class Meta:
        model = ProblemLink
        fields = ['title', 'url', 'platform']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
        }


# using a formset so organizers can add multiple problems to one contest on the same page
ProblemLinkFormSet = inlineformset_factory(
    Contest, ProblemLink,
    form=ProblemLinkForm,
    extra=1, # start with one empty row
    can_delete=True,
)


from .models import ContactMessage

# simple form for the contact us page
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How can we help?'}),
        }
