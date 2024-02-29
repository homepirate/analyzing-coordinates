from haversine import haversine
import pandas as pd


class Point:
    """Класс точек"""
    def __init__(self, name, coords):
        self.name = name.strip()
        self.latitude = float(coords.split(',')[0].strip())
        self.longitude = float(coords.split(',')[1].strip())

    def coords(self):
        return self.latitude, self.longitude

    def __repr__(self):
        class_name = self.__class__.__name__
        fields = ', '.join([f'{key}={value}' for key, value in self.__dict__.items()])
        return f'{class_name}({fields})'


class MainPoint(Point):
    """Класс точки, для которой находят ближайшие"""
    def __init__(self, name, cords):
        super().__init__(name, cords)
        self.bst = BST(self.coords())

    def make_bst(self, points: list[Point]):
        for point in points:
            self.bst.add(Node(data=point))

    def get_nears(self, limit):
        return self.bst.postorder(limit)


class Node:
    """Вспомогательный класс для работы с BST"""

    def __init__(self, data: Point):
        self.data = data
        self.left_child = None
        self.right_child = None


class BST:
    """Реализуем стандартое бинардное дерево поиска для сортировки по расстоянию от нужной точеи"""

    def __init__(self, coords):
        self.root = None
        self.main_coords = coords

    def add(self, new_item: Node):
        dist_new = haversine(self.main_coords, new_item.data.coords())  # раастояние  от MainPoint до точки, которую добавдяем в BSTж использует функцию для подсчета расстояние по геогр. координатам
        if not self.root:
            self.root = new_item
        else:
            current = self.root
            while True:
                dist_current = haversine(self.main_coords, current.data.coords()) # определяем расстояние текущее точки
                if dist_new < dist_current:
                    if current.left_child: # стандартное добавление если значение меньше, то проверяем левого потомка, если значение больше проверяем правого и так пока не дойдем до пустого потомка
                        current = current.left_child
                    else:
                        current.left_child = new_item
                        break
                else:
                    if current.right_child:
                        current = current.right_child
                    else:
                        current.right_child = new_item
                        break

    def postorder(self, limit):
        """Метод обхода  postorder сначала проверяем самого левого потомка (он самый маленький) потом проверяем центрального, потом правого
        Так происхожит сортировка по возрастанию в BST"""

        stack = []
        result = []
        current = self.root
        last_visited = None

        while stack or current:
            if current:
                stack.append(current)
                current = current.left_child
            else:
                peek_node = stack[-1]
                if peek_node.right_child and last_visited != peek_node.right_child:
                    current = peek_node.right_child
                else:
                    node = stack.pop()
                    result.append(node.data)
                    limit -= 1
                    last_visited = node
            if limit == 0:
                break

        return result


def open_files(file_path):
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path, delimiter=';', header=None)
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, header=None)
    else:
        print("Unsupported file format. Please provide a CSV, XLS, or XLSX file.")
        return []

    points = []
    for index, row in data.iterrows():
        new_point = Point(row.iloc[0], row.iloc[1])
        points.append(new_point)

    return points


def main():
    # mn = MainPoint("fff", "1.2, 3.4")
    # points = [Point("point1", "34.1, 14.2"), Point("point2", "1.1, 3.4"), Point("point3", "1.2, 3.3"),
    #           Point("point4", "44.1, 44.2"),]
    # mn.make_bst(points)
    # print(mn.get_nears(limit=2))
    # print(haversine((1.2, 3.4), (34.1, 14.2)))
    # print(haversine((1.2, 3.4), (1.1, 3.4)))
    # print(haversine((1.2, 3.4), (1.2, 3.3)))
    # print(haversine((55.613305, 37.604573), (55.612314, 37.589143)))
    print(open_csv("test_data/A.csv"))
    print(open_csv("test_data/A.xlsx"))


if __name__ == '__main__':
    main()
