from bs4 import BeautifulSoup

def extract_text_from_html(html_page):
  soup = BeautifulSoup(html_page, 'html.parser')
  text = soup.find_all(text=True)

  output = ''
  blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script'
  ]

  for t in text:
    if t.parent.name not in blacklist:
      output += '{} '.format(t)

  return output