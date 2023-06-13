from django import forms
from .models import Post, Category
from ckeditor.fields import RichTextFormField

# ! below code is to make dynamic choices but i don't plan on adding any more categories and they are enough
# def get_categories():
#     ch = Category.objects.all().values_list('title', 'title')
#     choices = []
#     for i in ch:
#         choices += [i]
#     print(choices)
#     return choices

choices = [('Uncategorized', 'Uncategorized'), ('Sports', 'Sports'), ('Food', 'Food'), ('Travel', 'Travel'), ('Health and Fitness', 'Health and Fitness'), ('Lifestyle', 'Lifestyle'), ('Fashion and Beauty', 'Fashion and Beauty'), ('Photography', 'Photography'), ('Personal', 'Personal'), ('DIY', 'DIY'), ('Art and Crafts', 'Art and Crafts'), ('Parenting', 'Parenting'), ('Music', 'Music'), ('Business', 'Business'), ('Stock market', 'Stock market'), ('Art and Design', 'Art and Design'), ('Books', 'Books'), ('Literature', 'Literature'), ('Book and writing', 'Book and writing'), ('Personal Finance', 'Personal Finance'), ('Interior Design', 'Interior Design'), ('News', 'News'), ('Movie', 'Movie'), ('Religion', 'Religion'), ('Political', 'Political'),]

class PostCreateForm(forms.ModelForm):
    # ! all parameter defined to apply styling over the page
    
    title = forms.CharField(label="Title" ,max_length=100, required=True,widget=forms.TextInput(attrs={"class": "full-width", "placeholder":"Title"}),)
    
    description = forms.CharField(label="Description" ,max_length=100, required=True,widget=forms.TextInput(attrs={"class": "full-width", "placeholder":"Description of Post", "multiple":"multiple"}),)

    content = RichTextFormField()
    
    # ! many to many field m aise hota h insertions
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={"class":"full-width", "multiple":True,})
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category', 'content',]
        
