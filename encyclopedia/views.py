from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
from markdown import Markdown 
from . import util
import random


class NewWikiForm(forms.Form):
    title =  forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus','weight':'15px','name':'title','style': 'width: 80%;'}))
    
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'content', 
                                                        'style': 'height: 15em;'}))


def convert(title):
     entry = util.get_entry(title)
     markdowner = Markdown()
     if entry == None:
        return None
     else:
        return markdowner.convert(entry)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries
    })


def find(request, title):
     entry = convert(title)
     if entry == None:
        msg = "Request page not find"
        return render(request, "encyclopedia/error.html",{
            "msg" : msg
        })
     else:
         
        return render(request , "encyclopedia/wiki.html", {
            "entry": entry,
            "title": title
        })


def search(request):

    entry = request.POST['q']
   
    for item in util.list_entries():
        if entry.lower() == item.lower():
            return redirect(reverse('encyclopedia:wiki', args=[entry]))
    else:
        list = []
        for item in util.list_entries():
            if entry.upper() in item.upper():
                list.append(item)
        if list == []:
            msg = "Request page not find"
            return render(request, "encyclopedia/error.html",{
            "msg" : msg
        }) 
        else:

             return render(request , "encyclopedia/index.html", {
             "entries": list
        })


def create(request):

    return render(request, "encyclopedia/new.html", {
        "form": NewWikiForm()
    })



def create_wiki(request):
    title = request.POST['title'].capitalize()
    content = request.POST['content']
    
    for item in util.list_entries():
            if title.upper() == item.upper():
                msg = "Encyclopedia entry already exists with the provided title"
                return render(request, "encyclopedia/error.html", {
            "msg" : msg
                })
            
    util.save_entry(title,content)


    return redirect(reverse('encyclopedia:wiki', args=[title]))


def rand(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{title}")

def edit(request,title):
    form = NewWikiForm()
    if request.method == "GET":
        entry = util.get_entry(title)
        form.fields['title'].initial = title
        form.fields['content'].initial = entry
        
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content":entry,
            "form": form
        })
    elif request.method == "POST":
        form = NewWikiForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect(reverse('encyclopedia:wiki', args=[title]))
