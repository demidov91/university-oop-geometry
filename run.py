from geometry.figures import Circle
from geometry.graphics import Point, draw_figure



def run():
    draw_figure(Circle(Point(0, 0), 1))


if __name__ == '__main__':
    run()