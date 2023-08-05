from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from .models import Url
from .views import MOST_POPULAR_COUNT


def create_url(full_url, redirects=0):
    """
    Create a url with the given `full_url` and optional `redirects`
    numbers.
    """
    return Url.objects.create(full_url=full_url, redirects=redirects)


class UrlModelTests(TestCase):

    def test_url_create(self):
        """
        test url create process
        """
        create_url(full_url="example.com")
        self.assertIs(len(Url.objects.all()), 1)

    def test_generate_short_id(self):
        """
        gen_short_id() returns randomly generated base62 id with
        length equals to ` settings.SHORT_ID_LEN`
        """
        short_id = Url.gen_short_id()
        self.assertIs(len(short_id), settings.SHORT_ID_LEN)


class UrlIndexViewTests(TestCase):

    def test_no_urls(self):
        """
        If no urls exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('url_simplify:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No simplified urls are available.")
        self.assertQuerysetEqual(response.context['popular_url_list'], [])

    def test_one_url(self):
        """
        Url displayed on the index page.
        """
        create_url(full_url="example.com")
        response = self.client.get(reverse('url_simplify:index'))
        self.assertQuerysetEqual(
            response.context['popular_url_list'],
            ['<Url: example.com, 0>']
        )

    def test_urls_order(self):
        """
        Url displayed based on `redirects` count and `created_at`
        on the index page.
        """
        create_url(full_url="example.com", redirects=20)
        create_url(full_url="example1_second_created.com", redirects=10)
        create_url(full_url="example1_last_created.com", redirects=10)
        response = self.client.get(reverse('url_simplify:index'))
        self.assertQuerysetEqual(
            response.context['popular_url_list'],
            ['<Url: example.com, 20>',
             '<Url: example1_last_created.com, 10>',
             '<Url: example1_second_created.com, 10>']
        )

    def test_most_popular_full_url(self):
        """
        Max number of most popular urls displayed on the index page.
        """
        for x in range(MOST_POPULAR_COUNT):
            create_url(full_url="example.com")
        response = self.client.get(reverse('url_simplify:index'))
        self.assertQuerysetEqual(
            response.context['popular_url_list'],
            ['<Url: example.com, 0>' for n in range(MOST_POPULAR_COUNT)]
        )

    def test_most_popular_plus_one_url(self):
        """
        Max number of most popular urls displayed on the index page.
        Even though there are max+1 urls.
        """
        for x in range(MOST_POPULAR_COUNT+1):
            create_url(full_url="example.com")
        response = self.client.get(reverse('url_simplify:index'))
        self.assertQuerysetEqual(
            response.context['popular_url_list'],
            ['<Url: example.com, 0>' for n in range(MOST_POPULAR_COUNT)]
        )


class UrlDetailViewTests(TestCase):

    def test_empty_url(self):
        """
        The url which has not created yet, should
        returns a 404 not found.
        """
        url = reverse('url_simplify:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
