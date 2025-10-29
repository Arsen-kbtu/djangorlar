# Small standalone demo script (does not import files named with digits)
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MenuItem:
	id: int
	name: str
	base_price: float

	def __str__(self):
		return f"{self.name} (${self.base_price:.2f})"

@dataclass
class Restaurant:
	id: int
	name: str
	menu: List[MenuItem]

def build_demo():
	r = Restaurant(id=1, name="Demo Place", menu=[])
	r.menu.append(MenuItem(id=1, name="Pizza", base_price=9.99))
	r.menu.append(MenuItem(id=2, name="Salad", base_price=4.5))
	return r

def summarize_menu(restaurant: Restaurant) -> str:
	return f"{restaurant.name}: {len(restaurant.menu)} items"

def most_expensive(restaurant: Restaurant):
	if not restaurant.menu:
		return None
	return max(restaurant.menu, key=lambda m: m.base_price)

if __name__ == "__main__":
	restaurant = build_demo()
	print("Menu:")
	for item in restaurant.menu:
		print(" *", item)
	print("Summary:", summarize_menu(restaurant))
	print("Most expensive:", most_expensive(restaurant))

# Quick assertions
assert len(restaurant.menu) == 2
assert most_expensive(restaurant).name == "Pizza"

# End of demo script

# Notes: standalone helpers
