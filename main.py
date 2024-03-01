import json

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
        """Сторит BST для точки"""
        for point in points:
            self.bst.add(Node(data=point))

    def get_nears(self, limit):
        """Находит ближайшие точки с указанными лимитом """
        return self.bst.inorder(limit)

    def make_json(self, limit):
        """Метод записывает данные в json формате для каждой точки и ее ближайших"""
        near_points = self.get_nears(limit)
        points_list = []

        for point in near_points:
            point_data = {
                'name': point.name,
                'coords': point.coords(),
                'dist':  haversine(self.coords(), point.coords())
            }
            points_list.append(point_data)

        json_data = {
            'main_point': {
                'name': self.name,
                'coords': self.coords()
            },
            'near_points': points_list
        }

        json_string = json.dumps(json_data, indent=4, ensure_ascii=False)
        return json_string


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

    def inorder(self, limit):
        """Метод обхода inorder сначала проверяем самого левого потомка (он самый маленький) потом проверяем центрального, потом правого
        Так происхожит сортировка по возрастанию в BST"""

        stack = []
        result = []
        current = self.root

        while stack or current:
            if current:
                stack.append(current)
                current = current.left_child
            else:
                node = stack.pop()
                result.append(node.data)
                limit -= 1
                if limit == 0:
                    break
                current = node.right_child

        return result


def open_files(file_path):
    """Открывает файл в форматах csv xls xlsx"""
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path, delimiter=';', header=None)
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path, header=None)
    else:
        print("Unsupported file format. Please provide a CSV, XLS, or XLSX file.")
        return

    return data


def make_arrays(file_a, file_b) -> tuple[list[MainPoint], list[Point]]:
    """Функция которая создает и возвращает два массива"""
    data_a = open_files(file_a)
    data_b = open_files(file_b)
    main_points = []
    for index, row in data_a.iterrows():
        new_point = MainPoint(row.iloc[0], row.iloc[1])
        main_points.append(new_point)

    points = []
    for index, row in data_b.iterrows():
        new_point = Point(row.iloc[0], row.iloc[1])
        points.append(new_point)

    return main_points, points


def create_xlsx_from_json(result_json_array, file_path):
    """Функция для сохранения итоговых данных"""
    all_data = []

    for js in result_json_array:
        json_data = json.loads(js)
        main_point_name = json_data['main_point']['name']
        main_point_coords = ', '.join(map(str, json_data['main_point']['coords'])) # Координаты преобразуем в строку в формате XX.xxx, XX.xxx

        near_points_data = []
        for near_point in json_data['near_points']:
            near_point_name = near_point['name']
            near_point_coords = ', '.join(map(str, near_point['coords']))
            near_point_dist = near_point['dist']
            near_points_data.extend([near_point_coords, near_point_name, near_point_dist]) # Добавляем в итоговый массив с данными всех ближайших точек для конкретной точки

        all_data.append([main_point_name, main_point_coords] + near_points_data)

    columns = ['Main Point Name', 'Main Point Coords']
    for i in range(len(json_data['near_points'])):
        columns += [f"Near Point Coords_{i+1}", f"Near Point Name_{i+1}", f"Distance_{i+1}"] # Создаем дополнительные колонки для каждой из ближайших точек они имеют индексы

    df = pd.DataFrame(all_data, columns=columns)
    df.to_excel(file_path, index=False)


def main():
    LIMIT = 3
    # mn = MainPoint("fff", "1.2, 3.4")
    # points = [Point("point1", "34.1, 14.2"), Point("point2", "1.1, 3.4"), Point("point3", "1.2, 3.3"),
    #           Point("point4", "44.1, 44.2"),]
    # mn.make_bst(points)
    # print(mn.get_nears(limit=2))
    # print(haversine((1.2, 3.4), (34.1, 14.2)))
    # print(haversine((1.2, 3.4), (1.1, 3.4)))
    # print(haversine((1.2, 3.4), (1.2, 3.3)))
    # print(haversine((55.613305, 37.604573), (55.612314, 37.589143)))

    result_json_array = []
    main_points, points = make_arrays("test_data/A.xlsx", "test_data/B.xlsx")
    for mp in main_points:
        mp.make_bst(points)

        result_json_array.append(mp.make_json(LIMIT))

    create_xlsx_from_json(result_json_array, "test_data/res.xlsx")

    # print(make_arrays("test_data/A.xlsx", "test_data/B.xlsx"))


if __name__ == '__main__':
    main()
