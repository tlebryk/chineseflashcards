class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width
rect = Rectangle(2,3)
# Here we declare that the Square class inherits from the Rectangle class
class Square(Rectangle):
    def __init__(self, length):
        super().__init__(length, length)
sq = Square(2)

print(sq.length)

class Cube(Square):
    def surface_area(self):
        face_area = super().area()
        return face_area * 6

    def volume(self):
        face_area = super().area()
        s = super()
        # print("self", self)
        # print("super", dir(s.area())) #.__getattribute__("length"))
        return face_area * self.length


print(Cube(2).volume())
