from django import forms
from .models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0', 'max': '100', 'step': '0.5',
                'placeholder': '0 - 100'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': 'Write your evaluation feedback here...'
            }),
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is None or score < 0 or score > 100:
            raise forms.ValidationError('Score must be between 0 and 100.')
        return score
