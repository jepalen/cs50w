from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category (models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    lowest_bid = models.DecimalField(decimal_places=2, max_digits=10)
    actual_bid = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    image = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_amount =  models.DecimalField(decimal_places=2, max_digits=10)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bidder} bid {self.bid_amount} on {self.date}"


class Comment(models.Model):
    comenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.comenter} commented {self.comment} on {self.listing}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is watching {self.listing}"