from django.shortcuts import render, redirect
from django.urls import reverse
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

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    if query in entries:
        return redirect(reverse('entry', args=[query]))
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results
        })
    
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if the entry already exists
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "message": f"Page '{title}' already exists."
                })
            else:
                # Save the new entry
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })