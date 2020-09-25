from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entryTitles": util.list_entries()
    })        

def randomPage(request):
    entries_list = util.list_entries()
    random.shuffle(entries_list)
    random_title = entries_list[0]
    return entryPage(request, random_title)

def searchResults(request):
    title = searchValue = request.GET['q']
    
    # Would it be faster to just render the entryPage template, instead of taking another route?
    # But since I don't want to replicate code, let's just redirect.
    if util.get_entry(searchValue) is not None:
        return HttpResponseRedirect(reverse("entrypage", args=[title]))
    else:
        results = util.suffix_search(searchValue)
        return render(request, "encyclopedia/searchResults.html", {
            "entriesMatch": results,
            "resultsListLength": len(results)
        })

def savePage(request):
    if request.method == "POST":
        title = request.POST["title"]
        
        if(util.get_entry(title) is not None):
            return render(request, "encyclopedia/errorDisplay.html", {
                "title": title
            })
        else:
            util.save_in_storage(request.POST["newpage"], title)
            
            util.md_to_html(util.get_entry(title), title)
            return render(request, "encyclopedia/entry.html", {
                "title": title
            })

def createNewPage(request):
    return render(request, "encyclopedia/newpage.html")

def saveEdits(request, title):
    if request.method == "POST":
        util.save_in_storage(request.POST["newpage"], title)

        util.md_to_html(util.get_entry(title), title)
        return render(request, "encyclopedia/entry.html", {
            "title": title
        })

def editPage(request, title):
    page_md = util.get_entry(title)
    util.md_to_html(page_md, title)
    return render(request, "encyclopedia/editPage.html", {
        "title": title,
        "page_md": page_md
    })

def entryPage(request, title):
    util.md_to_html(util.get_entry(title), title)
    return render(request, "encyclopedia/entry.html", {
        "title": title
    })

def deletePage(request, title):
    if (util.delete_entry(title)):
        return HttpResponseRedirect(reverse("index"))
    else:
        pass # Show error? What kind of error?
