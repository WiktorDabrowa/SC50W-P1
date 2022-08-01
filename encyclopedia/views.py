
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from . import util
from django import forms
import random

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
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            #Checking if a wiki entry with the 
            #same name already exists
            current = util.list_entries()
            for entry in current:
                if entry.lower() == title.lower():
                    return HttpResponse("Wiki entry with that name already exist.")
                else:
                    continue
        util.save_entry(title,content)
        return redirect('/')
    return render(request, "encyclopedia/create.html", {"form": NewPageForm()})

def random_page(request):
    list = util.list_entries()
    length = len(list)
    random_number = random.randrange(1, length+1)
    entries=[]
    i=1
    for entry in list:
        pair=[]
        pair.append(entry)
        pair.append(i)
        i += 1
        entries.append(pair)
    for pair in entries:
        if pair[1] == random_number:
            correct_entry = pair[0]
            title = pair[0]
        else:
            continue        
    entry = util.get_entry(correct_entry)
    return render(request, "encyclopedia/entry.html", {"entry" : entry, "title":title})
    #return render(request, "encyclopedia/entry.html", {"entry": context, "title":"title"})
    
