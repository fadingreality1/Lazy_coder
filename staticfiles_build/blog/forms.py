from typing import Any
from django import forms
from .models import Post, Category
from ckeditor.fields import RichTextFormField

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
            label="Title",
            max_length=100, 
            required=True,
            widget=forms.TextInput(attrs={"class": "full-width", "placeholder":"Title"}),
        )
    description = forms.CharField(
            label="Description",
            max_length=250, 
            required=True,
            widget=forms.TextInput(attrs={"class": "full-width", "placeholder":"Description of Post",}),
        )
    proxyimage = forms.ImageField(
            label="Image",
            required=True,
            help_text="for front view",
        )
    content = RichTextFormField()
    category = forms.ModelMultipleChoiceField(
        label = "Category",
        queryset = Category.objects.all(),
        widget = forms.SelectMultiple(attrs={"class":"full-width", "multiple":True, "style":"height:10em;", "size":"3",})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'description', 'proxyimage', 'category', 'content',]
        
    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'full-width'
