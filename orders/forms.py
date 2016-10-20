from django import forms
import datetime

MENU_ITEM_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class OrderAddMenuItemForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=MENU_ITEM_QUANTITY_CHOICES,
                                      coerce=int)
    date = forms.DateField(initial=datetime.date.today(),
                           widget=forms.TextInput(attrs={'type': 'date'}))
    comments = forms.CharField(
        max_length=200, required=False, label="Comments for vendor")

    def clean_date(self):
        cd = self.cleaned_data
        if cd['date'] <= datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past.")
        # Cut off orders after 2:30pm
        if (cd['date'] == datetime.date.today() and
            datetime.datetime.now().hour >= 14 and
            datetime.datetime.now().minute >= 30):
                raise forms.ValidationError("The orders have already been sent today.")
        # Don't allow orders on weekends
        if (cd['date'].weekday() > 3):
            raise forms.ValidationError("You can only order for Monday to Thursday.")
        return cd['date']


class FilterDateForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def clean(self):
        self.send_email = False
        cleaned_data = super(FilterDateForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if not (start_date and end_date):
            raise forms.ValidationError(
                "Hold your horses! Enter in some dates first.")
        if end_date < start_date:
            raise forms.ValidationError(
                "Zoicks! The start date needs to be greater than the end date.")
        if 'Send email to vendors' in self.data:
            self.send_email = True
