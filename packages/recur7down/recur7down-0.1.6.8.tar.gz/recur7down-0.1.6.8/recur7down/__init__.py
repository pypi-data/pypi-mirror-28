from .base import Collect
from .products import product_main
from .diary import diary_main
import sys
sys.path.append(os.getcwd())

def main():
    c = raw_input('get product(p) or diary(d):  p/d? ')
    if c.lower()=='p':
        product_main()
    elif c.lower()=='d':
        diary_main()
