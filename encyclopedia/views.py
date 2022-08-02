
from asyncio.windows_events import NULL
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from . import util
from django import forms
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    all_entries = util.list_entries()
    entry_name_lower = entry_name.lower()
    for entry in all_entries:
        entry_lower = entry.lower()
        if entry_lower == entry_name_lower:
            title = entry_name
            entry = util.get_entry(f"{entry_name}")
            return render(request, "encyclopedia/entry.html", {"entry" : entry, "title":title})
        else:
            continue
    raise Http404("Given query not found.")

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

def search(request):
    entries = util.list_entries()
    if request.method == "POST":
        query = request.POST['q']
        query = query.lower()
        possible_positions=[]
        for entry in entries:
            entry_lower = entry.lower()
            if entry_lower == query:
                entry = util.get_entry(entry)           
                return HttpResponseRedirect(f"wiki/{query}")
            elif entry_lower.find(query) >= 0:
                possible_positions.append(entry)
        if len(possible_positions) == 0:
            alert = "No Matching entries found"
        else:
            alert = ""
        return render(request, "encyclopedia/index.html", {
        "entries": possible_positions, "alert": alert
    })

def edit(request, entry_name):
    entry = util.get_entry(entry_name)
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry_name,content)
            return HttpResponseRedirect(f"/wiki/{entry_name}")
        else:
            return render(request, "encyclopedia/edit.html", { 
                "form": EditPageForm(initial={'content':entry}), 
                "action":"Please fill out all fields!",
                "title":entry_name })

    return render(request, "encyclopedia/edit.html",{ 
        "form": EditPageForm(initial={'content':entry}),
        "action":"Edit existing page",
        "title":entry_name })
    
                
            

    
