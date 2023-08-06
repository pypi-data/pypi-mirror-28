import datetime
import io

import pytest

from mir.frelia import sitemap


def test_url_repr():
    url = sitemap.URL('http://localhost/')
    got = repr(url)
    assert got == ("<URL with loc='http://localhost/',"
                   " lastmod=None, changefreq=None, priority=None>")


def test_url_invalid_lastmod():
    url = sitemap.URL('http://localhost/')
    with pytest.raises(sitemap.ValidationError):
        url.lastmod = datetime.time(1, 2, 3)


def test_url_invalid_changefreq():
    url = sitemap.URL('http://localhost/')
    with pytest.raises(sitemap.ValidationError):
        url.changefreq = 'foo'


def test_url_invalid_changefreq_capitalization():
    url = sitemap.URL('http://localhost/')
    with pytest.raises(sitemap.ValidationError):
        url.changefreq = 'DAILY'


def test_url_invalid_priority_range():
    url = sitemap.URL('http://localhost/')
    with pytest.raises(sitemap.ValidationError):
        url.priority = 1.1


def test_complete_url_to_etree():
    url = sitemap.URL('http://localhost/')
    url.lastmod = datetime.datetime(2010, 1, 2)
    url.changefreq = 'daily'
    url.priority = 0.5

    got = url.to_etree()
    assert got.find('loc').text == 'http://localhost/'
    assert got.find('lastmod').text == '2010-01-02T00:00:00'
    assert got.find('changefreq').text == 'daily'
    assert got.find('priority').text == '0.5'


def test_minimal_url_to_etree():
    url = sitemap.URL('http://localhost/')

    got = url.to_etree()
    assert got.find('loc').text == 'http://localhost/'
    assert got.find('lastmod') is None
    assert got.find('changefreq') is None
    assert got.find('priority') is None


def test_render():
    """Test rendering a sitemap urlset."""
    url = sitemap.URL('http://localhost/')
    url.lastmod=datetime.date(2010, 1, 2)
    url.changefreq = 'daily'
    url.priority = 0.7

    file = io.StringIO()
    sitemap.write_sitemap_urlset(file, [url])
    assert file.getvalue() == (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9'
        ' http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
        '<url><loc>http://localhost/</loc><lastmod>2010-01-02</lastmod>'
        '<changefreq>daily</changefreq><priority>0.7</priority></url>'
        '</urlset>')
