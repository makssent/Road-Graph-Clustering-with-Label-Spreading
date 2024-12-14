import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import osmnx as ox

def create_graph_osm(place_name="Murom, Russia"):
    G = ox.graph_from_place(place_name, network_type='drive')
    G = G.to_undirected()
    return G

def label_spreading_data(G, fixed_labels, alpha=0.99, num_iterations=10):
    A = nx.adjacency_matrix(G).todense()  # Матрица смежности
    d = np.array(A.sum(axis=1)).flatten()  # Степени узлов
    D = np.diagflat(1 / np.sqrt(d))  # Диагональная матрица со значениями 1/√d
    S = D @ A @ D  # Нормализованная матрица похожести

    node_to_index = {node: idx for idx, node in enumerate(G.nodes())}

    # Инициализация меток
    Y0 = np.zeros((len(G.nodes), 2))
    Y0[node_to_index[fixed_labels[0]], 0] = 1
    Y0[node_to_index[fixed_labels[1]], 1] = 1

    #обновление меток формулой Y=αSY+(1−α)Y
    Y = np.array(Y0)
    Y_history = [Y.copy()]
    for _ in range(num_iterations):
        Y = alpha * S @ Y + (1 - alpha) * Y0 # @ - умножение матриц.
        Y_history.append(np.array(Y))

    return Y_history

def normalize(y):
    total = np.sum(y)
    if total == 0:
        return [0, 0]
    return y / total

def plot_graph_live(G, Y_history, interval=100, initial_node_size=50, edge_color='gray'):
    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
    fig, ax = plt.subplots(figsize=(12, 8))

    def update(frame):
        ax.clear()
        Y = Y_history[frame]
        node_colors = [
            (normalize(y)[0], 0, normalize(y)[1])
            for y in Y
        ]
        nx.draw(
            G,
            pos,
            node_color=node_colors,
            node_size=initial_node_size,
            with_labels=False,
            edge_color=edge_color,
            ax=ax
        )
        ax.set_title(f'Label Spreading. Iteration: {frame + 1}')

    anim = FuncAnimation(fig, update, frames=len(Y_history), interval=interval, repeat=False)
    plt.show()


def plot_graph_final(G, Y, initial_node_size=50, edge_color='gray'):
    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
    node_colors = [
        (normalize(y)[0], 0, normalize(y)[1])
        for y in Y
    ]
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=initial_node_size,
        with_labels=False,
        edge_color=edge_color
    )
    plt.title("Final Label Spreading Result")
    plt.show()

# def plot_graph_live(G, Y_history):
#     pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}  # Географические координаты узлов
#     fig, ax = plt.subplots(figsize=(12, 8))
#
#     def update(frame):
#         ax.clear()
#         Y = Y_history[frame]
#         node_colors = [
#             (normalize(y)[0], 0, normalize(y)[1])  # Нормализация и преобразование в цвет
#             for y in Y
#         ]
#         node_sizes = (500 * np.max(Y, axis=1)).tolist()  # Увеличиваем размеры узлов
#         nx.draw(
#             G,
#             pos,
#             node_color=node_colors,
#             node_size=node_sizes,  # Используем увеличенный массив размеров
#             with_labels=False,
#             edge_color='gray',
#             ax=ax
#         )
#         ax.set_title(f'Label Spreading. Iteration: {frame + 1}')
#
#     anim = FuncAnimation(fig, update, frames=len(Y_history), interval=1000, repeat=False)
#     plt.show()


def interactive_selection(G, initial_node_size=50, edge_color='gray'):
    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw(G, pos, ax=ax, node_size=initial_node_size, edge_color=edge_color)

    selected_nodes = []

    def onclick(event):
        if event.xdata is None or event.ydata is None:
            return

        min_dist = float('inf')
        closest_node = None
        for node, (x, y) in pos.items():
            dist = (x - event.xdata) ** 2 + (y - event.ydata) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_node = node

        if closest_node not in selected_nodes:
            selected_nodes.append(closest_node)
            ax.scatter(*pos[closest_node], color='red', s=initial_node_size * 2)
            fig.canvas.draw()

        if len(selected_nodes) == 2:
            plt.close(fig)

    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    return selected_nodes

def main():
    G = create_graph_osm()

    print("Выберите две точки на графе для инициализации кластеризации.")
    fixed_labels = interactive_selection(G)

    print(f"Выбранные узлы: {fixed_labels}")
    print("\nВыберите режим работы:")
    print("1. Кластеризация по итерациям.")
    print("2. Готовая кластеризация.")
    choice = input("Введите номер выбора (1 или 2): ")

    if choice == "1":
        num_iterations = input("Введите количество итераций: ")
        try:
            num_iterations = int(num_iterations)
            if num_iterations <= 0:
                raise ValueError("Количество итераций должно быть положительным числом.")
        except ValueError as e:
            print(f"Ошибка: {e}. Установлено значение по умолчанию: 10.")
            num_iterations = 10

        interval = input("Введите интервал для анимации (в миллисекундах): ")
        try:
            interval = int(interval)
            if interval <= 0:
                raise ValueError("Интервал должен быть положительным числом.")
        except ValueError as e:
            print(f"Ошибка: {e}. Установлено значение по умолчанию: 100.")
            interval = 100

        Y_history = label_spreading_data(G, fixed_labels=fixed_labels, num_iterations=num_iterations)
        plot_graph_live(G, Y_history, interval=interval)

    elif choice == "2":
        num_iterations = 100  # По умолчанию
        Y_history = label_spreading_data(G, fixed_labels=fixed_labels, num_iterations=num_iterations)
        plot_graph_final(G, Y_history[-1])

    else:
        print("Неверный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()