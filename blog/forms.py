from typing import Any
from django import forms
from .models import Post, Category
from ckeditor.fields import RichTextFormField

# ! below code is to make dynamic choices but i don't plan on adding any more categories and they are enough

class PostCreateForm(forms.ModelForm):
    # ! all parameter defined to apply styling over the page
    
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
            widget=forms.TextInput(attrs={"class": "full-width", "placeholder":"Description of Post", "multiple":"multiple"}),
        )
    
    image = forms.ImageField(
            label="Image",
            required=True,
            help_text="for front view"
        )

    content = RichTextFormField()
    
    # ! many to many field m aise hota h insertions
    category = forms.ModelMultipleChoiceField(
        label = "Category (Hold the Ctrl key to select multiple options from the list box. Maximum 3 are allowed, anymore, will be ignored)",
        queryset = Category.objects.all(),
        widget = forms.SelectMultiple(attrs={"class":"full-width", "multiple":True, "style":"height:15em;", "size":"3",})
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category', 'content',]
        
