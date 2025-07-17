from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect


def scrape_view(request):
    headers = {'User-Agent': 'Mozilla/5.0'}

    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "scrape":
            site = request.POST.get('site', '')
            if site:
                try:
                    page = requests.get(site, headers=headers)
                    soup = BeautifulSoup(page.text, 'html.parser')

                    for link in soup.find_all('a'):
                        link_address = link.get('href')
                        link_text = link.get_text(strip=True) or "No Text"
                        if link_address:
                            Link.objects.create(address=link_address, name=link_text)

                except Exception as e:
                    print(f"Error scraping: {e}")
        
        elif action == "delete":
            Link.objects.all().delete()
        
        return HttpResponseRedirect('/')  # Post-redirect-get pattern

    # GET request — show all data
    data = Link.objects.all()
    return render(request, 'myapp/result.html', {'data': data})


# Optional: Separate view to clear all links (not needed if you already handle delete in scrape_view)
def clear(request):
    Link.objects.all().delete()
    return HttpResponseRedirect('/')
