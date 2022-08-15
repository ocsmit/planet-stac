import requests
from auth import Authenticate
from order import Order
from search import Search
from consts import ORDER_URL

TEST_ID = "c936e57a-b3a5-402f-95a4-0a2980a1ba37"

auth = Authenticate()

r = requests.get(f"{ORDER_URL}/{TEST_ID}", auth=auth.authentication)

res = r.json()
res.keys()
