from django.shortcuts import render
import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def entry(request, title):
    html_content = convert(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "message": "Ooops, looks like this specific entry does not exist, try looking for a different one!:)"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html",{
                "title": entry_search,
                "content": html_content
            })
        else:
            entries = util.list_entries()
            recommendation = []
            for entry in entries:
                if entry.lower in entry_search():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists!"
            })
        else:
            util.save_entry(title, content)
            html_content = convert(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = (title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
        

def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert(rand_entry)
    return render(request, "encyclopedia/entry.html",{
                  "title": rand_entry,
                  "content": html_content
    })

