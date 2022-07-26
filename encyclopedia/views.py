from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    title = entry_name
    entry = util.get_entry(f"{entry_name}")
    return render(request, "encyclopedia/entry.html", {"entry" : entry, "title":title})

def create(request):
    return render(request, "encyclopedia/create.html")

