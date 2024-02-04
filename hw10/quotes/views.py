from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . models import Author, Tag, Quote
from . forms import TagForm , QuoteForm, AuthorForm


def main_view(request, page=1):
    quotes = Quote.objects.all()
    row_cnt = 10
    paginator = Paginator(list(quotes), row_cnt)
    page_quotes = paginator.page(page)
    
    return render(request, "quotes/main.html", context={'quotes': page_quotes})


def main_view_tag(request, page=1, tag_name=''):
    req = request.POST.getlist('tags')
    print(f"req={req!r}")
    choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), quote=request.user)
    print(f"choice_tags= {choice_tags!r}")

    quotes = Quote.objects.all()
    row_cnt = 10
    paginator = Paginator(list(quotes), row_cnt)
    page_quotes = paginator.page(page)
    
    return render(request, "quotes/main.html", context={'quotes': page_quotes})


@login_required
def tag_change(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def author_change(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


@login_required
def quote_change(request):
    tags = Tag.objects.all().order_by("name")    #.filter(user=request.user)
    auths = Author.objects.all().order_by("fullname")

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            # choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), quote=request.quote)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, "auths": auths, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, "auths": auths, 'form': QuoteForm()})
    

def author_show(request, author_id):
    author = get_object_or_404(Author, pk=author_id)        
    return render(request, 'quotes/authorshow.html', {"author": author})
