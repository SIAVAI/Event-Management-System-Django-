from django import forms
from .models import Event, Participant, Category

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500"
    checkbox_classes = "form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out"
    select_date_input_classes = "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-blue-500 focus:ring-blue-500 mr-2" 

    def widget_er_upor_style(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 4
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxInput): 
                 field.widget.attrs.update({
                    'class': self.checkbox_classes
                 })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2" 
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                for i, sub_widget in enumerate(field.widget.widgets):
                    sub_widget.attrs.update({
                        'class': self.select_date_input_classes
                    })
            else: 
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_er_upor_style()

class ParticipantForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_er_upor_style()

class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}), 
            'time': forms.TimeInput(attrs={'type': 'time'}), 
            'description': forms.Textarea(attrs={'rows': 4}),
            'participants': forms.CheckboxSelectMultiple, 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_er_upor_style()