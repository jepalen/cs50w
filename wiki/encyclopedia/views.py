import markdown
import random
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Article")
    edit = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(widget=forms.Textarea, label="markdown content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error_404(request, exception):
    return render(request, "encyclopedia/error.html", status=404)

def article(request, title):
    if request.method == "POST":
        return render(request, "encyclopedia/new.html", {
                 "form": NewTaskForm(
                    initial={
                        'title': title,
                        'edit': True,
                        'content': util.get_entry(title)
                    }
                 )
                })
    
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/article.html", {
            "title": title.title(),
            "error": "Article does not exist"
        })
    return render(request, "encyclopedia/article.html", {
        "title": title.title(),
        "content": markdown.markdown(content)
    })

def random_article(request):
    random_choice = random.choice(util.list_entries())
    return render(request, "encyclopedia/article.html", {
        "title": random_choice.title(),
        "content": markdown.markdown(util.get_entry(random_choice))
    })

def search(request):
    query = request.GET.get('q', '')
    if util.get_entry(query):
        return render(request, "encyclopedia/article.html", {
            "title": query.title(),
            "content": markdown.markdown(util.get_entry(query))
        })

    possible_entries = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            possible_entries.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": possible_entries
    })

def new(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            edit = form.cleaned_data["edit"]
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not content.lower().startswith(f"# {title.lower()}"):
                content = f"# {title.title()}\n\n" + content
            if not util.get_entry(title) or edit:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:article", args=[title]))
            else:
                return render(request, "encyclopedia/new.html", {
                "error": "Error: Article already exists"
            })
    return render(request, "encyclopedia/new.html", {
       "form": NewTaskForm()
    })
