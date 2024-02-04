from django.forms import ModelForm, CharField, TextInput, DateTimeField, Textarea
from . models import Author, Tag, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    born_date = CharField(min_length=5, max_length=50)
    born_location = CharField(min_length=5, max_length=150)
    description = CharField(min_length=5, widget=Textarea())
    created_at = DateTimeField()

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, required=True, widget=Textarea())
    author = CharField(min_length=5, required=True, widget=TextInput())
    created_at = DateTimeField()

    class Meta:
        model = Quote
        fields = ['author', 'quote']
        exclude = ['tags']
