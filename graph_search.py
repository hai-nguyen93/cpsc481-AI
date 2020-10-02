class Node:
    def __init__(self, name, children=None):
        if children is None:
            children = []
        self.name = name
        self.children = children
        self.visited = False


def bfs(node):
    queue = []
    node.visited = True
    queue.append(node)

    while queue:
        current_node = queue.pop(0)
        print(current_node.name, end=' ')
        for child_node in current_node.children:
            if not child_node.visited:
                child_node.visited = True
                queue.append(child_node)


def dfs(node):
    if not node.visited:
        print(node.name, end=' ')
        node.visited = True
        for child in node.children:
            dfs(child)


def best_first_search(start, goal):
    # Each element in open_list and closed_list is a 4-tuple
    # x = (node, g(n), h(n), path)
    open_list = [[start, 0, 0, str("")]]
    closed_list = []
    iter_num = 0
    found = False
    path = ""
    while open_list:
        iter_num += 1
        x = open_list.pop(0)
        print(x[0].name, end=' ')
        if x[0].name == goal:
            found = True
            path = x[3] + str(x[0].name)
            break

        else:
            for child_index, child in enumerate(x[0].children):

                # evaluate g(n) and h(n)
                # g(n) = depth
                # h(n) = 1 if left or right child; 0 if center child;
                # center child exists only if there are 3 children
                g_n = x[1] + 1
                h_n = 0
                if len(x[0].children) == 3:
                    if child_index == 1:  # middle child
                        h_n = 1

                # get the names of the nodes in open and closed lists for easier reference
                open_nodes = [n[0].name for n in open_list]
                closed_nodes = [n[0].name for n in closed_list]

                # if child node is not in closed_list and not in open_list
                if (child.name not in open_nodes) and (child.name not in closed_nodes):
                    open_list.append([child, g_n, h_n, x[3] + str(x[0].name)])

                # if child node is on open_list
                elif child.name in open_nodes:
                    index = open_nodes.index(child.name)
                    if g_n < open_list[index][2]:   # g_n = depth, which also equals the length of the path
                        open_list[index] = [child, g_n, h_n, x[3] + str(x[0].name)]

                # if child node is on closed_list
                elif child.name in closed_nodes:
                    index = closed_nodes.index(child.name)
                    if g_n < open_list[index][2]:
                        closed_list.pop(index)
                        open_list[index] = [child, g_n, h_n, x[3] + str(x[0].name)]

            closed_list.append(x)

            # sort open and closed lists by heuristic merit (smaller f(n)=g(n)+h(n) first)
            open_list.sort(key=lambda e: e[1]+e[2], reverse=False)
            closed_list.sort(key=lambda e: e[1]+e[2], reverse=False)

    if not found:
        path = "Cannot find the destination " + str(goal)
    return found, iter_num, path


A = Node('A')
B = Node('B')
C = Node('C')
D = Node('D')
E = Node('E')
F = Node('F')
G = Node('G')
H = Node('H')
I = Node('I')
J = Node('J')
K = Node('K')
L = Node('L')
M = Node('M')
N = Node('N')
O = Node('O')
P = Node('P')
R = Node('R')

graph = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R]

# Graph definition
A.children = [B, C, D]
B.children = [E, F, G]
C.children = [G]
D.children = [H, I]
E.children = [J, K, L]
F.children = [L, A]
G.children = [M, N, H]
H.children = [A, O, P]
I.children = [P, R]

print("Breadth-First Visitation Order: ", end=' ')
bfs(A)

# Reset visited for each node
for graph_node in graph:
    graph_node.visited = False

print("\nDepth-First Visitation Order: ", end=' ')
dfs(A)

destination = input("\n\nEnter a goal node: ")
print("\nBest-First-Search Visitation Order: ", end=' ')
r, i, p = best_first_search(A, destination)
print("\nStatus: ", r, "\nNumber of iterations: ", i, "\nPath: ", p)
