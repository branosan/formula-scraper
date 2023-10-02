from . import *

def main():
    # contents of target page
    page = requests.get(START_SITE)
    soup = bs(page.text, 'html.parser')
    # find all hrefs and put them into a list
    links = soup.find_all('a')


if __name__ == '__main__':
    main()