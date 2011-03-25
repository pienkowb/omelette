class Layouter(object):
    @staticmethod
    def layout(diagram):
        x = y = highest = 0;
        for node in diagram.nodes.values():
            node.moveBy(x, y)
            x += 20 + node.boundingRect().size().width()
            if node.boundingRect().size().height() > highest:
                    highest = node.boundingRect().size().height()
            if x > 400:
                x = 0
                y += highest + 20
                highest = 0

