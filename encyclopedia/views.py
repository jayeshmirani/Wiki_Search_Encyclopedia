from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class SearchForm(forms.Form):
    search= forms.CharField(label="Search Encyclopedia")

class NewPageForm(forms.Form):
    title= forms.CharField(label="Title")
    content=forms.CharField(widget=forms.Textarea(), label="Markdown Content")

class EditForm(forms.Form):
    content=forms.CharField(widget=forms.Textarea(), label="Markdown Content")

def index(request):
    if request.method=="POST":
        form= SearchForm(request.POST)
        if form.is_valid():
            # return render(request,"wiki/index.html",{
            #     "form":form
            # })
            return HttpResponseRedirect(reverse('search'))
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchform":SearchForm()
    })

def entry(request,title):
    if request.method=="POST":
        form= SearchForm(request.POST)
        if form.is_valid():
            # return render(request,"wiki/entry.html",{
            #     "form":form
            # })
            return HttpResponseRedirect(reverse('search'))
    entries= util.list_entries()
    available=True
    if title.upper() in entries:
        title=title.upper()
    elif title.capitalize() in entries:
        title=title.capitalize()
    else:
        available=False
        data=False
    if available:
        md_data=util.get_entry(title)
        data= Markdown().convert(md_data)
    # if data==None:
    #     return render(request,"encyclopedia/error.html")
    return render(request,"encyclopedia/entry.html",{
        "data":data,
        "title":title,
        "searchform":SearchForm()
    })

def search(request):
    form= SearchForm(request.POST)
    if form.is_valid():
        entries= util.list_entries()
        title=form.cleaned_data["search"]
        found=False
        if title.capitalize() in entries:
            found=True
            title=title.capitalize()
        elif title.upper() in entries:
            found=True
            title=title.upper()
        if found:
            return render(request,"encyclopedia/entry.html",{
                "data":Markdown().convert(util.get_entry(title)),
                "title":title,
                "searchform":SearchForm()
            })
        sub_entries=[]
        for entry in entries:
            if title.upper() in entry.upper():
                sub_entries.append(entry)
        if sub_entries==[]:
            return render(request,"encyclopedia/error.html",{
                "searchform":SearchForm()
            })
        return render(request,"encyclopedia/sub_entries.html",{
            "sub_entries":sub_entries,
            "searchform":SearchForm()
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchform":SearchForm()
    })    

def newpage(request):
    if request.method == "POST":
        form= NewPageForm(request.POST)
        if form.is_valid():
            title= form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            if(util.get_entry(title.upper())==None and util.get_entry(title.capitalize())==None):
                if(title==title.upper()):
                    util.save_entry(title,content)
                else:
                    title=title.capitalize()
                    util.save_entry(title,content)
                md_data=util.get_entry(title)
                data=Markdown().convert(md_data)
                return render(request,"encyclopedia/entry.html",{
                    "data":data,
                    "title":title,
                    "searchform":SearchForm()
                })
            return render(request,"encyclopedia/newpage_error.html")
    return render(request,"encyclopedia/newpage.html",{
        "newpageform": NewPageForm()
    })

def editpage(request,title):
    if request.method== "POST":
        form= EditForm(request.POST)
        if form.is_valid():
            content= form.cleaned_data["content"]
            util.save_entry(title,content)
            return render(request,"encyclopedia/entry.html",{
                            "title":title,
                            "data":Markdown().convert(content),
                            "searchform":SearchForm()
                        })
    md_data= util.get_entry(title)
    return render(request,"encyclopedia/editpage.html",{
        "title": title,
        "editform": EditForm(initial={"content": md_data}),
        "searchform":SearchForm() 
    })
    
def randompage(request):
    entries= util.list_entries()
    title=random.choice(entries)
    return render(request,"encyclopedia/entry.html",{
                            "title":title,
                            "data":Markdown().convert(util.get_entry(title)),
                            "searchform":SearchForm()
                        })