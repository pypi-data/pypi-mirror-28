from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,  Http404
from django.urls import reverse
from django.views import generic
from .models import Url


URLS_PAGINATION = 10
MOST_POPULAR_COUNT = 20


class IndexView(generic.ListView):
    template_name = 'url_simplify/index.html'
    context_object_name = 'popular_url_list'

    def get_queryset(self):
        """
        Return the most popular `MOST_POPULAR_COUNT` objects,
        based on redirects and created_at
        """
        return get_most_popular()[:MOST_POPULAR_COUNT]


class DetailView(generic.DetailView):
    model = Url
    template_name = 'url_simplify/detail.html'


class UrlsView(generic.ListView):
    template_name = 'url_simplify/urls_list.html'
    context_object_name = 'url_list'
    paginate_by = URLS_PAGINATION

    def get_queryset(self):
        """
        Pass most popular urls based on `get_most_popular()`
        """
        return get_most_popular()


def short_redirect(request, short_id):
    """
    Handles redirects for shortened urls, every time user request this,
    force redirect and increment redirect count for particular `Url` object
    """
    url = get_object_or_404(Url, short_id=short_id)
    url.redirects += 1
    url.save()
    redirect_url = url.full_url
    if not redirect_url.startswith('http://'):
        if not redirect_url.startswith('https://'):
            redirect_url = 'http://' + redirect_url
    return HttpResponseRedirect(redirect_url)


def add_url(request):
    """
    Url shortener form action
    """
    input_url = request.POST.get('input_url', '')
    # in case 'input_url' is not provided by POST request
    if not input_url:
        return HttpResponseRedirect(reverse('url_simplify:index'))
    short_id = Url.gen_short_id()
    # check if already exists, if so, try one to generate one more time
    tmp = Url.objects.filter(short_id=short_id)
    if tmp:
        return Http404("Something went wrong. Please, try one more time")
    url = Url(full_url=input_url, short_id=short_id)
    url.save()
    return HttpResponseRedirect(reverse('url_simplify:detail',
                                        args=(url.id,)))


def delete_url(request, url_id):
    """
    Url remove handler
    """
    p = Url.objects.get(pk=url_id)
    p.delete()
    return HttpResponseRedirect(reverse('url_simplify:urls'))


def get_most_popular():
    """
    Helper which retrieves most popular urls based on `redirects`(desc) and
    `created_at`(desc)
    """
    return Url.objects.order_by('-redirects', '-created_at')
