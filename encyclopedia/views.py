from django.shortcuts import render
from django import forms
import markdown2

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Get the content of the entry
    content = util.get_entry(title)

    # If the entry does not exist, render a 404 page
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page '{title}' not found."
        })

    # Render the entry page with the content
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

