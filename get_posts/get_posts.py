import os
import re
import sys
import codecs
import HTMLParser
import urllib2

m2k2_base = 'https://m2k2.taigaforum.com/allposts/'
sda_base = 'https://forum.speeddemosarchive.com/allposts/'

h = HTMLParser.HTMLParser()
post_line_begin = '<div class="highlight"><span class="highlightlabel">' + \
                  'Post preview:</span><span class="highlighttext">'
quote_tags = ['<div class="quotearea"><div class="quotelabel">', '</div></div>']
date_tag = '<div class="relevantpostdate"><a class="relevantpostdatelink" href='

def download_html(site, username, page):
    if   site == 'm2k2': url_base = m2k2_base
    elif site == 'sda':  url_base = sda_base
    url = '%s%s-%u.html' % (url_base, username, page)
    html = urllib2.urlopen(url).read()
    html = unicode(html, 'utf-8')
    html = html.split('\n')
    return html

def parse_html(html):
    paragraphs = []
    dates = []
    for line in html:
        # Get date
        if date_tag in line:
            date = line.replace(date_tag, '').replace('</a></div>', '')
            date = date.split('>')[1]

        if post_line_begin not in line: continue

        # Remove the line beginning (Post preview:)
        line = line.replace(post_line_begin, ' ')

        # Remove quoted text
        while quote_tags[0] in line:
            tag_start_inds = [x.start() for x in
                              re.finditer(quote_tags[0], line)]
            tag_end_inds = [x.start() + len(quote_tags[1]) for x in
                            re.finditer(quote_tags[1], line)]
            inds = sorted(tag_start_inds + tag_end_inds)
            depth = 0
            tag_start_ind = tag_start_inds[0]
            for ind in inds:
                if ind in tag_start_inds: depth += 1
                elif ind in tag_end_inds: depth -= 1
                if depth == 0:
                    break
            tag_end_ind = ind
            line = line[:tag_start_ind] + line[tag_end_ind:]

        # Convert HTML entities to ASCII (i.e. "&amp;" --> "&")
        line = h.unescape(line)

        # Split line into paragraphs
        for paragraph in reversed(line.split('<br /><br />')):
            # Remove everything between brackets
            paragraph = re.sub(r'\<[^>]*\>', ' ', paragraph)
            # Remove hyperlinks
            paragraph = re.sub(r'http?:\/\/\S+', ' ', paragraph)
            paragraph = re.sub(r'https?:\/\/\S+', ' ', paragraph)
            # Remove extraneous spaces
            paragraph = re.sub(' +',' ',paragraph)
            paragraph = paragraph.strip()
            # Make sure the paragraph isn't blank
            if not paragraph: continue
            # Processing paragraph is complete
            paragraphs.append(paragraph)
            dates.append(date)

    paragraphs.reverse()
    dates.reverse()

    return paragraphs, dates

def get_num_pages(site, username):
    html = download_html(site, username, 1)
    found_line = False
    for line in html:
        if 'currentpagenum' in line:
            found_line = True
            break
    if found_line:
        line = re.sub(r'\<[^>]*\>', ' ', line)
        line = line.replace('&nbsp', '')
        line = line.replace(',', '').replace(';', '')
        num_pages = int(line.split()[-1])
        return num_pages
    for line in html:
        if 'go to the last page' in line.lower():
            found_line = True
            break
    if found_line:
        line = re.sub(r'\<[^>]*\>', ' ', line)
        num_pages = int(line.split()[1])
        return num_pages

def process_page(site, username, page, writer):
    # Download HTML from the internet
    html = download_html(site, username, page)

    # Parse HTML
    paragraphs, dates = parse_html(html)
    num_paragraphs = len(paragraphs)

    # Write paragraphs to file
    for i, paragraph in enumerate(paragraphs):
        date = dates[i]
        writer.write('%s: %s\n' % (date, paragraph))
    print 'Read page %3u: %3u paragraphs found' % (page, num_paragraphs)

def main():
    if len(sys.argv) != 3:
        print "Usage: python get_posts.py <site> <username>"
        exit(-1)
    site = sys.argv[1].lower()
    username = sys.argv[2].lower()
    if site not in ['m2k2', 'sda']:
        print 'Invalid site chosen. Valid options are "m2k2" and "sda".'
        exit(-1)

    # Open output file
    fout = os.path.join('posts_raw', site, '%s.txt' % (username))
    if not os.path.isdir(os.path.join('posts_raw', site)):
        os.makedirs(os.path.join('posts_raw', site))
    writer = codecs.open(fout, 'wb', 'utf-8')

    # Get number of pages in user's post history
    num_pages = get_num_pages(site, username)

    # Loop over all pages in user's post history
    for page in range(num_pages, 0, -1):
        process_page(site, username, page, writer)

    writer.close()

if __name__ == '__main__':
    main()
