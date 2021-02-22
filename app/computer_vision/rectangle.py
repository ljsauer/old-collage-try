class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x+w
        self.y2 = y+h

    def collides(self, other) -> bool:
        if self == other:
            return False
        collision = (
                self.x2 >= other.x1 and
                self.x1 <= other.x2 and
                self.y2 >= other.y1 and
                self.y1 <= other.y2
        )
        contains = (
            self.x1 > other.x1 and
            self.x2 < other.x2 and
            self.y1 > other.y1 and
            self.y2 < other.y2
        )
        return collision or contains
