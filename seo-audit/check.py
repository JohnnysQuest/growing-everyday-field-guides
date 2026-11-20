"""Inspect a fictional HTML snapshot. No network or external crawl is required."""
import argparse
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import shutil
from urllib.parse import urljoin

BASE = Path(__file__).parent / 'site'
INTENDED = {'/', '/workshops/', '/workshops/bookbinding/', '/workshops/letterpress/', '/booking/'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ''
        self.links = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'a':
            self.links.append(data['href'])
        if tag == 'meta' and data.get('name') == 'robots':
            self.noindex = 'noindex' in data.get('content','').lower().split(',')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def inspect(root):
    findings = set()
    titles = defaultdict(list)
    pending = ['/']
    seen = set()
    excluded = set()
    while pending:
        url = pending.pop()
        if url in seen:
            continue
        seen.add(url)
        page = Page()
        page.feed((root / url.strip('/') / 'index.html').read_text())
        if page.noindex:
            if url in INTENDED:
                findings.add(('indexing', url))
            else:
                excluded.add(url)
        if url in INTENDED:
            titles[page.title].append(url)
        for href in page.links:
            dest = urljoin(url, href)
            if (root / dest.strip('/') / 'index.html').is_file():
                pending.append(dest)
            else:
                findings.add(('missing destination', url, dest))
    for title, urls in titles.items():
        if len(urls) > 1:
            findings.add(('shared title', title, *sorted(urls)))
    return seen, findings, excluded


def patch_fixture(root, url, before, after):
    path = root / url.strip('/') / 'index.html'
    content = path.read_text()
    assert content.count(before) == 1
    path.write_text(content.replace(before, after))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retest', action='store_true')
    args = parser.parse_args()
    seen, findings, excluded = inspect(BASE)
    print('HTML pages examined:', len(seen), '| Intentional exclusions:', sorted(excluded))
    for finding in sorted(findings):
        print(' | '.join(finding))
    if args.retest:
        book = '/workshops/bookbinding/'
        press = '/workshops/letterpress/'
        assert len(seen) == 7 and excluded == {'/privacy/', '/archive/'}
        assert findings == {('indexing',book), ('missing destination',book,'/reserve/'),
                            ('shared title','Workshop | Folio Bench',book,press)}
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp) / 'site'
            shutil.copytree(BASE, staged)
            patch_fixture(staged, book, '<meta name="robots" content="noindex">', '')
            patch_fixture(staged, book, 'href="/reserve/"', 'href="/booking/"')
            patch_fixture(staged, book, 'Workshop | Folio Bench', 'Beginner bookbinding | Folio Bench')
            patch_fixture(staged, press, 'Workshop | Folio Bench', 'Letterpress for beginners | Folio Bench')
            checked, remaining, deliberate = inspect(staged)
            assert checked == seen and not remaining and deliberate == excluded
        print('PASS: all three repairs verified on a temporary copy. Both intentional exclusions retained.')


if __name__ == '__main__':
    main()
