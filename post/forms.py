from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'type': 'text',
            'placeholder': 'Tên',
            'class': 'form-control'
        })

        self.fields['email'].widget.attrs.update({
            'type': 'email',
            'placeholder': 'Email',
            'class': 'form-control'
        })

        self.fields['body'].widget.attrs.update({
            'placeholder': 'Bình Luận',
            'class': 'textarea form-control',
            'id': 'form-message',
            'rows': '8',
            'cols': '20'
        })
