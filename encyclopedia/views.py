
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import util
from django import forms
    
class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    title = entry_name
    entry = util.get_entry(f"{entry_name}")
    return render(request, "encyclopedia/entry.html", {"entry" : entry, "title":title})

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            current = util.list_entries()
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in current:
                
                if entry.lower() == title.lower():
                    return HttpResponse("Wiki entry with that name already exist.")
                else:
                    continue
            
        util.save_entry(title,content)
    return render(request, "encyclopedia/create.html", {"form": NewPageForm()})

