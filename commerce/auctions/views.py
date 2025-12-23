from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
import decimal

from .models import User, Category, Listing, Watchlist, Bid, Comment

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Product Name")
    description = forms.CharField(label="Description")
    lowest_bid = forms.DecimalField(label="Lowest Bid")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Categories")
    image = forms.URLField(label="Image URL")

class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Bid")

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Your comment")

def index(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html",{
            "listings": Listing.objects.exclude(owner=request.user).all(),
            "my_listings": Listing.objects.filter(owner=request.user).all()
        })
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if not username or not email or not password or not confirmation:
            return render(request, "auctions/register.html", {
                "message": "Username, email, password and confirmation are required."
            })


        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    
    if request.method == "POST" and request.user.is_authenticated:
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = request.POST["title"]
            description = request.POST["description"]
            lowest_bid = request.POST["lowest_bid"]
            category = request.POST["category"]
            image = request.POST["image"]
            owner = request.user 
            listing = Listing(title=title, description=description, lowest_bid=lowest_bid, category_id=category, image=image, owner=owner)
            listing.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/create.html",
    {"form": NewTaskForm()
    })


def listing(request, listing_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            action = request.POST.get("action")
            if action == "add":
                watchlist = Watchlist(user=request.user, listing_id=listing_id)
                watchlist.save()
            elif action == "remove":
                watchlist = Watchlist.objects.filter(user=request.user, listing_id=listing_id)
                watchlist.delete()
            elif action == "bid":
                form = NewBidForm(request.POST)
                if form.is_valid():
                    bid_amount = form.cleaned_data["bid"]
                    listing = Listing.objects.get(id=listing_id)
                    if bid_amount > listing.actual_bid and bid_amount >= listing.lowest_bid:
                        bid = Bid(bidder=request.user, bid_amount=bid_amount, listing_id=listing_id)
                        bid.save()
                        listing.actual_bid = bid.bid_amount
                        listing.save()
                    else:
                        messages.error(request, "Your bid must be higher than the current bid.")
            elif action == "close":
                
                    listing = Listing.objects.get(id=listing_id)
                    listing.enabled = False
                    highest_bid = Bid.objects.filter(listing_id=listing_id).order_by("-bid_amount").first()
                    listing.winner = highest_bid.bidder if highest_bid else None
                    listing.save()
                    return HttpResponseRedirect(reverse("auctions:index"))
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing_id=listing_id).exists()
        comments = Comment.objects.filter(listing_id=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(id=listing_id),
            "bid_form": NewBidForm(),
            "is_in_watchlist": is_in_watchlist,
            "comment_form": NewCommentForm(),
            "comments": comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "error": "You must be logged in to view this page.",
        })

def comment(request, listing_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            listing = Listing.objects.get(id=listing_id)
            comment = Comment(comenter=request.user, listing=listing, comment=comment)
            comment.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user)
        listings = Listing.objects.filter(id__in=watchlist.values("listing_id"))
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
    return render(request, "auctions/watchlist.html")   

def category(request, category_id):
        listings = Listing.objects.filter(category_id=category_id)
        return render(request, "auctions/category.html", {
            "listings": listings
        })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })
