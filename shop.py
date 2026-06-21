class Product:
    def __init__(self, name: str, price: int, discount: float):
        self._name = name
        self._price = price
        self._discount = discount
    
    @property
    def name(self):
        return self._name
    
    @property
    def discount(self):
        return self._discount
    
    @property
    def price(self):
        return int (self._price - self._price * self._discount)
    
    def __str__(self):
        return f"{self.name}: {self.price} руб"
    
class DigitalProduct(Product):
    def __init__(self, name: str, price: int, discount: float, file_size: int):
        super().__init__(name, price, discount)
        self.file_size = file_size

    def download_info(self):
        return f"Скачать: {self.name} ({self.file_size} МБ)"
    
class PhysicalProduct(Product):
    def __init__(self, name: str, price: int, discount: float, weight: int):
        super().__init__(name, price, discount)
        self.weight = weight

    def shipping_cost(self):
        return self.weight * 50
    
    def total_price(self):
        return self.price + self.weight * 50
    
class Cart:
    def __init__(self, lst: list = []):
        self.lst = lst

    def add(self, product):
        return self.lst.append(product)
    
    def __len__(self):
        return len(self.lst)
    
    def remove(self, name: str):
        for i in range(len(self.lst)):
            if self.lst[i].name == name:
                self.lst.pop(i)
                break

    def total(self):
        sum=0
        for i in range(len(self)):
            if type(self.lst[i]).__name__ == "PhysicalProduct":
                sum += self.lst[i].total_price()
            else:
                sum += self.lst[i].price()
        return sum

    def __str__(self):
        a=""
        for i in range(len(self)):
            a += str(self.lst[i]) + "\n"
        return a