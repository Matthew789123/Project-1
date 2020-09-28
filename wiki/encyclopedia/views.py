from django.shortcuts import render

from . import util

import markdown2

from django.http import HttpResponseRedirect

from django import forms

import random

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
        return HttpResponseRedirect(f"/{request.GET['q']}")
    else:
        entries = []
        for entry in util.list_entries():
            if request.GET['q'].lower() in entry.lower():
                entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })

def add(request):
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST['entry']
        if title.lower() in [x.lower() for x in util.list_entries()]:
            return render(request, "encyclopedia/error.html", {
                "content": "Sorry but this entry already exists."
            })
        else:
            util.save_entry(title, entry)
            return HttpResponseRedirect(f"/{title}")
    return render(request, "encyclopedia/add.html")

def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST['entry'])
        return HttpResponseRedirect(f"/{title}")
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": entry
    })

def rand(request):
    random.seed()
    return HttpResponseRedirect(f"/{util.list_entries()[random.randrange(len(util.list_entries()))]}")