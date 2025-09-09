import turtle


class MyCanvas:
    def __init__(self):
        self.show_circle = True
        self.show_square = True
        self.show_triangle = True

        self.screen = turtle.Screen()
        self.screen.title("Геометрические примитивы")
        self.screen.setup(600, 500)
        self.screen.bgcolor("white")

        self.artist = turtle.Turtle()
        self.artist.speed(0)
        self.artist.penup()
        self.artist.hideturtle()

        self.setup_key_bindings()

        self.redraw()

        self.show_instructions()

        self.screen.mainloop()

    def setup_key_bindings(self):
        self.screen.onkey(lambda: self.toggle_figure('circle'), '1')
        self.screen.onkey(lambda: self.toggle_figure('square'), '2')
        self.screen.onkey(lambda: self.toggle_figure('triangle'), '3')
        self.screen.onkey(self.screen.bye, 'q')
        self.screen.listen()

    def toggle_figure(self, figure_type):
        if figure_type == 'circle':
            self.show_circle = not self.show_circle
        elif figure_type == 'square':
            self.show_square = not self.show_square
        elif figure_type == 'triangle':
            self.show_triangle = not self.show_triangle

        self.redraw()

    def show_instructions(self):
        instructions = turtle.Turtle()
        instructions.speed(0)
        instructions.penup()
        instructions.color("black")
        instructions.goto(-250, 200)
        instructions.write("Управление:", align="left", font=("Arial", 12, "normal"))
        instructions.goto(-250, 180)
        instructions.write("1 - круг", align="left", font=("Arial", 10, "normal"))
        instructions.goto(-250, 160)
        instructions.write("2 - квадрат", align="left", font=("Arial", 10, "normal"))
        instructions.goto(-250, 140)
        instructions.write("3 - треугольник", align="left", font=("Arial", 10, "normal"))
        instructions.hideturtle()

    def draw_circle(self, x, y):
        self.artist.goto(x, y - 40)
        self.artist.pendown()
        self.artist.color("red")
        self.artist.circle(40)
        self.artist.penup()

    def draw_square(self, x, y):
        self.artist.goto(x - 40, y - 40)
        self.artist.pendown()
        self.artist.color("blue")
        for _ in range(4):
            self.artist.forward(80)
            self.artist.left(90)
        self.artist.penup()

    def draw_triangle(self, x, y):
        self.artist.goto(x, y + 40)
        self.artist.pendown()
        self.artist.color("green")
        for _ in range(3):
            self.artist.forward(80)
            self.artist.left(120)
        self.artist.penup()

    def redraw(self):
        self.artist.clear()

        if self.show_circle:
            self.draw_circle(x=-100, y=0)

        if self.show_square:
            self.draw_square(x=0, y=0)

        if self.show_triangle:
            self.draw_triangle(x=100, y=0)

if __name__ == "__main__":
    canvas = MyCanvas()