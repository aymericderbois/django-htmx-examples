from django import forms

from todomvc.core.models import Todo


class TodoForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "new-todo",
                "placeholder": "What needs to be done?",
                "autofocus": "",
            }
        ),
        label="",
    )

    class Meta:
        model = Todo
        fields = ["title"]


class TodoUpdateForm(TodoForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "edit"})
