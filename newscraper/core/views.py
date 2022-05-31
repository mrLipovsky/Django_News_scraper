from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def get_html_content(new):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    new = new.replace(' ', '+')
    html_content = session.get(f'https://tech.eu/search/?q={new}').text
    
    # html_content = session.get(f'https://newsapi.org/v2/everything?q=tesla&from=2022-04-29&sortBy=publishedAt&apiKey=a6aba2d161234810abdf29e32db175dd').text
    # html_content = session.get(f'https://www.esky.cz/flights/select/roundtrip/ap/prg/ap/tbs?departureDate=2022-09-03&returnDate=2022-09-10&pa=1&py=0&pc=0&pi=0&sc=economy')
    return html_content

# @api_view(['GET', 'POST'])

def home(request):
    new_data = None
    if 'new' in request.GET:
        new = request.GET.get('new')
        html_content = get_html_content(new)

        from bs4 import BeautifulSoup   
        soup = BeautifulSoup(html_content, 'html5lib')
        new_data = dict()
        # news = soup.find('div', attrs={'class': 'post-title'}).select_one('h2').text
        # news_one = soup.find('div', attrs={'class': 'post-sd'}).text
        # print(news)
        # print(news_one)
        post = soup.find_all('div', attrs={'class': 'post-title'})
        print(len(post))
        new_data['header'] = soup.find('div', attrs={'class': 'post-title'}).select_one('h2').text
        new_data['link'] = soup.find('div', attrs={'class':'post-title'}).select_one('a',href=True)['href']
        new_data['text'] = soup.find('div', attrs={'class': 'post-sd'}).text
        new_data['author'] = soup.find('a', attrs={'class': 'post-author-name'}).text
        new_data['date'] = soup.find('span', attrs={'class': 'post-date'}).text
    
    # return render(request, 'core/home.html', {'new': new_data})
    
    return render(request, 'core/home.html', {'new': new_data})
