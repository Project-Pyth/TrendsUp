from django import forms
from post.models import Post


# Post Creation Form
class CreatePostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 100}))

    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'category']


# Post Update Form
class UpdatePostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 100}))
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

    def save(self, commit=True):
        post = self.instance
        post.title = self.cleaned_data['title']
        post.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            post.image = self.cleaned_data['image']

        if commit:
            post.save()
        return post
