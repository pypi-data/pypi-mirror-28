from .base import Collect
from .products import product_main
from .diary import diary_main
from .transaction import transaction_main



def main():
    c = raw_input('get product(p) or diary(d) or transaction(t):  p/d/t? ')
    if c.lower()=='p':
        product_main()
    elif c.lower()=='d':
        diary_main()
    elif c.lower()=='t':
        transaction_main()
