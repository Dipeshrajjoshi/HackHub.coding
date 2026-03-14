from django import forms
from .models import Submission


# the main form for students to submit their work to a contest
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['contest', 'title', 'description', 'submission_type', 'file', 'image', 'external_link']
        # making the form controls look good with bootstrap classes
        widgets = {
            'contest': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter submission title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'submission_type': forms.Select(attrs={'class': 'form-select', 'id': 'submission_type'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'external_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from contests.models import Contest
        from django.utils import timezone
        # we only want to show contests that are currently running so users don't submit to old ones
        # or ones that haven't started yet
        now = timezone.now()
        self.fields['contest'].queryset = Contest.objects.filter(
            is_published=True,
            start_time__lte=now,
            end_time__gte=now
        )

    # validating the uploaded file for size and type security
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # 5MB limit per file is usually enough for homework/code projects
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")
            import os
            ext = os.path.splitext(file.name)[1].lower()
            # restricting to these formats prevents people from uploading executables or scripts
            allowed_extensions = ['.pdf', '.zip', '.py', '.c', '.cpp', '.doc', '.docx', '.txt']
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Unsupported file extension: {ext}")
        return file

    # making sure images aren't too massive either
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024: # 2MB image limit
                raise forms.ValidationError("Image size must be under 2MB.")
        return image

    # final check to make sure they uploaded the right thing for their submission type
    def clean(self):
        cleaned_data = super().clean()
        submission_type = cleaned_data.get('submission_type')
        file = cleaned_data.get('file')
        image = cleaned_data.get('image')
        external_link = cleaned_data.get('external_link')

        # logic: if they choose 'code', they MUST provide a file, etc.
        if submission_type in ['code', 'document', 'zip'] and not file:
            raise forms.ValidationError(f'Please upload a file for {submission_type} submission.')
        
        if submission_type == 'image' and not image:
            raise forms.ValidationError('Please upload an image.')
            
        if submission_type == 'github' and not external_link:
            raise forms.ValidationError('Please provide a GitHub repository link.')

        return cleaned_data
