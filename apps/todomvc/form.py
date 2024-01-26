from django import forms

from apps.todomvc.models import Todo



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

    def save(self, session_uuid: str, *args, **kwargs):
        self.instance.session_uuid = session_uuid
        return super().save(*args, **kwargs)


class TodoUpdateForm(TodoForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "edit"})
