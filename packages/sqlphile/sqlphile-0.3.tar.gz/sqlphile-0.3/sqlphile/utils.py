import datetime
from .d import D
from .f import F

def toD (dict, engine):	
	d = D (**dict)
	d.encode (engine)
	return d

def make_orders (order_by, keyword = "ORDER"):
	if isinstance (order_by, str):
		order_by = [order_by]
	orders = []
	for f in order_by:
		if f[0] == "-":
			orders.append (f[1:] + " DESC")
		else:
			orders.append (f)	
	return "{} BY {}".format (keyword, ", ".join (orders))
	