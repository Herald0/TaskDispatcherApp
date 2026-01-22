class ColoredPencil:
    def __init__(self, color, length, width):

        self.color = color
        self.length = length
        self.width = width
        
    def write(self, symb, num):
        if num // 10 <= self.length and self.length > 0:
            self.length -= num // 10
            return symb * num

        count = 0
        st = ""
        for i in range(num):
            if self.length == 0:
                break
            st += symb
            count += 1
            if count == 10:    
                if self.length > 0:
                    self.length -= 1
                    count = 0
        return st   
        
    def sharpen(self):
        self.length -= 3
        if self.length < 0:
            self.length = 0
    
    def info(self):
        return f"This is a {self.color} pencil with a length of {self.length} and a thickness of {self.width}"
    

cp = ColoredPencil('gray', 13, 3)
print(cp.write('$', 23))
print(cp.info())
print(cp.write('0', 43))
print(cp.info())
cp.sharpen()
print(cp.info())
cp.sharpen()
print(cp.info())
print(cp.write('&', 16))
print(cp.info())
print(cp.write('@', 30))
print(cp.info())