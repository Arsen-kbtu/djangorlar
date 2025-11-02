# Simple order utilities
from dataclasses import dataclass, field
from typing import List

@dataclass
class OrderItem:
	name: str
	price: float
	quantity: int = 1

	def line_total(self) -> float:
		return self.price * self.quantity

	def __str__(self) -> str:
		return f"{self.quantity} x {self.name} @ ${self.price:.2f}"

@dataclass
class Order:
	id: int
	items: List[OrderItem] = field(default_factory=list)

	def add(self, item: OrderItem) -> None:
		self.items.append(item)

	def subtotal(self) -> float:
		return sum(i.line_total() for i in self.items)

	def total(self, discount: float = 0.0) -> float:
		sub = self.subtotal()
		return max(0.0, sub - discount)

	def __str__(self) -> str:
		lines = [str(i) for i in self.items]
		return "\n".join(lines) + f"\nSubtotal: ${self.subtotal():.2f}"

if __name__ == "__main__":
	o = Order(id=1)
	o.add(OrderItem(name="Margherita", price=8.5, quantity=2))
	o.add(OrderItem(name="Fries", price=3.0, quantity=1))
	print(o)
	print("Total with $2 discount:", o.total(2.0))

# End of order utilities

# exported: Order, OrderItem

def pretty_total(order: Order) -> str:
	return f"Order {order.id} total: ${order.total():.2f}"
