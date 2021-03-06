from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from .choices import state_choices, bedroom_choices, price_choices


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_listings = Listing.objects.order_by('-list_date')

    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_listings = queryset_listings.filter(description__icontains=keywords)

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_listings = queryset_listings.filter(city__iexact=city)

    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_listings = queryset_listings.filter(state__iexact=state)

    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_listings = queryset_listings.filter(bedrooms__lte=bedrooms)

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_listings = queryset_listings.filter(price__lte=price)

    context = {
        'listings': queryset_listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
