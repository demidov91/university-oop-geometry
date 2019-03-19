from copy import copy

from geometry.figures import Circle, Elipse, Line
from geometry.graphics import draw
from geometry.core import Point, Container



def run():
    head = Container(Circle(2), Point(5, 5))
    body = Container(Elipse(2, 4), Point(5, 9))
    arm_1 = Container([
        Line(Point(0, 0), Point(3, 3)),
        Line(Point(1, 0), Point(1, 1)),
        Line(Point(0, 1), Point(1, 1)),
    ], Point(1, 4))
    arm_2 = Container([
        Line(Point(0, 3), Point(3, 0)),
        Line(Point(2, 0), Point(2, 1)),
        Line(Point(3, 1), Point(2, 1)),
    ], Point(6, 4))
    leg_1 = Container([
        Line(Point(3, 0), Point(1, 4)),
        Line(Point(1, 4), Point(0, 4)),
    ], Point(1, 12))
    leg_2 = Container([
        Line(Point(0, 0), Point(2, 4)),
        Line(Point(2, 4), Point(3, 4)),
    ], Point(6, 12))


    human1 = Container([
        head, body, arm_1, arm_2, leg_1, leg_2
    ])

    human2 = copy(human1)
    human2.coordinates.x = 10

    draw(Container([human1, human2]))


if __name__ == '__main__':
    run()