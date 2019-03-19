import tkinter as tk

from geometry.figures import Circle, Elipse, Line, Triangle, Rectangle, Square
from geometry.graphics import GenericInterface, GUI, TextBoard
from geometry.core import Point, Container


def create_two_people():
    head = Container(Circle(20), Point(50, 30))
    body = Container(Elipse(20, 40), Point(50, 90))
    arm_1 = Container([
        Line(Point(0, 0), Point(30, 30)),
        Line(Point(10, 0), Point(10, 10)),
        Line(Point(0, 10), Point(10, 10)),
    ], Point(10, 40))
    arm_2 = Container([
        Line(Point(0, 30), Point(30, 0)),
        Line(Point(20, 0), Point(20, 10)),
        Line(Point(30, 10), Point(20, 10)),
    ], Point(60, 40))
    leg_1 = Container([
        Line(Point(30, 0), Point(10, 40)),
        Line(Point(10, 40), Point(0, 40)),
    ], Point(10, 120))
    leg_2 = Container([
        Line(Point(0, 0), Point(20, 40)),
        Line(Point(20, 40), Point(30, 40)),
    ], Point(60, 120))

    human = Container([
        head, body, arm_1, arm_2, leg_1, leg_2
    ])

    human2 = Container(human, Point(100, 0))

    return Container([human, human2])


def create_seesaw():
    basement = Triangle(Point(40, 20), Point(30, 60), Point(50, 60))
    line = Rectangle(80, 10)
    figure = Square(10)

    return Container([
        basement,
        Container(line, Point(0, 10)),
        Container(figure, Point(0, 0)),
        Container(figure, Point(70, 0)),
    ])


def run():
    people = create_two_people()
    GenericInterface(TextBoard()).draw(people)

    root = tk.Tk()
    gui = GenericInterface(GUI(master=root))
    gui.draw(people)

    seesaw = create_seesaw()
    seesaw.coordinates.x = 350
    seesaw.coordinates.y = 50
    gui.draw(seesaw)

    root.mainloop()


if __name__ == '__main__':
    run()