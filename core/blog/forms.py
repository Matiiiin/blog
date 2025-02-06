from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 3}
        )
    )
