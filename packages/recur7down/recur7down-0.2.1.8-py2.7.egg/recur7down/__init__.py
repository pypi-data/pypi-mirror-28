from .base import Collect
from .products import product_main
from .diary import diary_main
from .transaction import transaction_main
from .html import html_main
from .parse_diary import parse_diary_main

import sys

def main():
    """
    entrypoint, if with first input 'raw', then taking input instead of read
    get product(p) or diary(d) or transaction(t) or html(h) or parse diary(pd):  \np/d/t/h/pd? 
    """
    if sys.argv[1]=='raw':
        c = str(sys.argv[2]).strip()
    else:
        c = raw_input('get product(p) or diary(d) or transaction(t) or html(h) or parse diary(pd):  \np/d/t/h/pd? ')
        
    if c.lower()=='p':
        product_main()
    elif c.lower()=='d':
        diary_main()
    elif c.lower()=='t':
        transaction_main()
    elif c.lower()=='h':
        html_main()
    elif c.lower()=='pd':
        parse_diary_main()
