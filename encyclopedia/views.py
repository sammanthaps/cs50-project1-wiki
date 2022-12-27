from django.shortcuts import render, redirect, reverse
from django import forms
from markdown2 import Markdown
from re import search

import secrets

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Encyclopedia",
        "header": "Contents:"
    })


def entry(request, value):
    mdfile = util.get_entry(value)

    if mdfile is None:
        return render(request, "encyclopedia/NO_entry.html", {
            "title": value.upper()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(mdfile),
            "title": value
        })


def search_form(request):
    searchform = request.GET.get('q', '').upper() # Gets the value of the parameter in a GET request. 'q' is the parameter. '' is the default value if None.
    if util.get_entry(searchform) is not None:
        return redirect(reverse("entry", kwargs={"value": searchform}))
    else:
        search_str = []

        for substring in util.list_entries():
            if search(searchform.upper(), substring.upper()):
                search_str.append(substring)
        
        if len(search_str) == 0: # if the list of strings is empty it'll return a "Not Found" error page.
            return render(request, "encyclopedia/NO_entry.html", {
                "title": searchform
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": search_str,
                "title": "Encyclopedia/search",
                "header": "Search Results:"
            })


class new_form(forms.Form):
    form_title = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form_title', 'placeholder': 'Title', 'autofocus': True}))
    form_content = forms.CharField(label="", min_length=27, widget=forms.Textarea(attrs={'class': 'form_content', 'placeholder': 'Write Your Content Here.'}))
    edit_form = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

def new_page(request):
    # POST = the data's gonna change the server's database.
    if request.method == 'POST': # if this is a POST request, then process the Form data.
        form = new_form(request.POST) # create a form instance and populate it with data from the request.          
        
        if form.is_valid(): # will validate the data submitted with a form. Check if the form is valid.
            # process the validated form data in the "form.cleaned_data" dictionary.
            form_title = form.cleaned_data["form_title"] 
            form_content = form.cleaned_data["form_content"]

            if util.get_entry(form_title) is None or form.cleaned_data["edit_form"] is True : # if the "form_title" does NOT exist in "util.get_entry".
                util.save_entry(form_title, form_content) # it will save the new entry.
                return redirect(reverse("entry", kwargs={'value': form_title})) # it will redirect to the new entry page.
            
            else: # if the "form_title" DOES exist in "util.get_entry" a error message will appear to inform the user.
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "saveError": True,
                    "entry": form_title
                })
        else: # if the form is NOT valid, the current page will remain, until the user fix the error.
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    else: # if this is a GET method or any other method, create the default form.
        return render(request, "encyclopedia/new_page.html", {
            "form": new_form(auto_id=False)
        })


def edit_form(request, value):
    if util.get_entry(value) is None:
        return render(request, "encyclopedia/NO_entry.html", {
            "title": value
        })
    
    else:
        form = new_form()
        form.fields["form_title"].initial = value # display an "empty" form in which a field is initialized to a particular value.
        form.fields["form_title"].widget = forms.HiddenInput()
        form.fields["form_content"].initial = util.get_entry(value)
        form.fields["edit_form"].initial = True

        return render(request, "encyclopedia/editing_page.html", {
            "form": form,
            "edit": form.fields["edit_form"].initial,
            "title": form.fields["form_title"].initial,

        })


def random_page(request):
    return redirect(reverse("entry", kwargs={'value': secrets.choice(util.list_entries())}))

