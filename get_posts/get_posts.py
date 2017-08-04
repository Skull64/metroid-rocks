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
re_string = '%s(.*)%s' % (quote_tags[0], quote_tags[1])

def download_html(site, username, page):
    if site == 'm2k2': url_base = m2k2_base
    elif site == 'sda': url_base = sda_base
    url = '%s%s-%u.html' % (url_base, username, page)
    html = urllib2.urlopen(url).read()
    html = unicode(html, 'utf-8')
    html = html.split('\n')
    return html

def parse_html(html):
    paragraphs = []
    for line in html:
        if post_line_begin not in line: continue
        # Remove the line beginning (Post preview:)
        line = line.replace(post_line_begin, ' ')
        # Remove quoted text
        if quote_tags[0] in line:
            to_remove = re.search(re_string, line).group(1)
            line = line.replace(to_remove, ' ')
        # Convert HTML entities to ASCII (i.e. "&amp;" --> "&")
        line = h.unescape(line)
        for paragraph in line.split('<br /><br />'):
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
    paragraphs.reverse()
    return paragraphs

def main():
    if len(sys.argv) != 3:
        print "Usage: python get_posts.py <site> <username>"
        exit(-1)
    site = sys.argv[1].lower()
    username = sys.argv[2].lower()

    if site not in ['m2k2', 'sda']:
        print 'Invalid site chosen. Valid options are "m2k2" and "sda".'
        exit(-1)

    fout = os.path.join('posts_raw', site, '%s.txt' % (username))
    if not os.path.isdir(os.path.join('posts_raw', site)):
        os.makedirs(os.path.join('posts_raw', site))
    writer = codecs.open(fout, 'wb', 'utf-8')
    page = 0

    # Loop over all the pages in the user's post history
    while True:
        page += 1
        # Download HTML from the internet
        html = download_html(site, username, page)
        # Parse HTML
        paragraphs = parse_html(html)
        num_paragraphs = len(paragraphs)
        # Write paragraphs to file
        for paragraph in paragraphs: writer.write('%s\n' % (paragraph))
        # Stop if no more posts are found
        if num_paragraphs == 0: break
        print 'Read page %3u: %3u paragraphs found' % (page, num_paragraphs)

    writer.close()

if __name__ == '__main__':
    main()
