from django.shortcuts import render

from . import util

import markdown2

from django.http import HttpResponseRedirect

from django import forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "content": "Sorry but the requested page was not found. The requested entry may not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": title
        })

def search(request):
    if not util.get_entry(request.GET['q']) is None:
        return entry(request, request.GET['q'])
    else:
        entries = []
        for e in util.list_entries():
            if request.GET['q'].lower() in e.lower():
                entries.append(e)
        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })

def add(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST['entry']
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "content": "Sorry but this entry already exists."
            })
        else:
            util.save_entry(title, entry)
            return HttpResponseRedirect(f"/{title}")
    return render(request, "encyclopedia/add.html")