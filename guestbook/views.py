from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .models import Entry
from .forms import EntryForm
from .constants import SMILIES


def index(request):
    entries = Entry.objects.order_by("-published")
    paginator = Paginator(entries, 10)

    page_number = request.GET.get("page")
    is_posted = request.GET.get("posted", False)

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "guest/index.html",
        {"entries": entries, "is_posted": is_posted, "page_obj": page_obj},
    )


def sign(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("index_view") + "?posted=yes")
    else:
        form = EntryForm()

    return render(request, "guest/sign.html", {"form": form, "smilies": SMILIES})
