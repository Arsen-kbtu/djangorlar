# Utilities for restaurants and menu items
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MenuItem:
	id: int
	name: str
	base_price: float
	is_available: bool = True

	def price(self) -> float:
		return float(self.base_price)

	def __str__(self) -> str:
		return f"{self.name} (${self.price():.2f})"

@dataclass
class Restaurant:
	id: int
	name: str
	menu: List[MenuItem] = field(default_factory=list)

	def add_item(self, item: MenuItem) -> None:
		self.menu.append(item)

	def available_items(self) -> List[MenuItem]:
		return [i for i in self.menu if i.is_available]

	def find(self, name: str) -> Optional[MenuItem]:
		for item in self.menu:
			if item.name == name:
				return item
		return None

# small demonstration when run as script
if __name__ == "__main__":
	r = Restaurant(id=1, name="Demo Eatery duplicate 2")
	r.add_item(MenuItem(id=1, name="Margherita", base_price=8.5))
	r.add_item(MenuItem(id=2, name="Cock", base_price=1.5, is_available=False))
	print("Available items:")
	for it in r.available_items():
		print(" -", it)
	found = r.find("Coke")
	print("Found:", found)

# Utilities exported: MenuItem, Restaurant
