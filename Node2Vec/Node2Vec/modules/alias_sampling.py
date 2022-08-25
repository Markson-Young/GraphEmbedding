import numpy as np
from Node2Vec.utils.args import arg_utils
import networkx as nx
import matplotlib.pyplot as plt
#获取超参数
args = arg_utils()

def load_graph():
    # 载入图
    # 连接带权重
    if args.weighted:
        G = nx.read_edgelist(args.input, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    # 连接不带权重
    else:
        G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = np.abs(np.random.randn())
    # 无向图
    if not args.directed:
        G = G.to_undirected()
    return G

def alias_setup(probs):
    '''
    Compute utility lists for non-uniform sampling from discrete distributions.
    Refer to https://hips.seas.harvard.edu/blog/2013/03/03/the-alias-method-efficient-sampling-with-many-discrete-outcomes/
    for details
    '''
    K = len(probs)
    # q corrsespond to Prob
    q = np.zeros(K)
    # J Alias
    J = np.zeros(K, dtype=np.int64)

    smaller = []
    larger = []

    # 将各个概率分成两组，一组的概率值大于1，另一组的概率值小于1
    for kk, prob in enumerate(probs):
        q[kk] = K* prob  # 每类事件的概率 乘 事件个数

        # 判定”劫富”和“济贫“的对象
        if q[kk] < 1.0:
            smaller.append(kk)
        else:
            larger.append(kk)

    # 使用贪心算法，将概率值小于1的不断填满
    # pseudo code step 3
    while len(smaller) > 0 and len(larger) > 0:
        small = smaller.pop()
        large = larger.pop()

        J[small] = large
        # 更新概率值，劫富济贫，削峰填谷
        q[large] = q[large] - (1 - q[small])
        if q[large] < 1.0:
            smaller.append(large)  # 把被打倒的土豪归为贫农
        else:
            larger.append(large)

    return J, q

def alias_draw(J, q):
    '''
    Draw sample from a non-uniform discrete distribution using alias sampling.
    O(1)的采样
    '''
    K = len(J) # 事件个数
    kk = int(np.floor(np.random.rand()*K)) # 生成1到K的随机整数
    if np.random.rand() < q[kk]:
        return kk # 取自己本来就对应的事件
    else:
        return J[kk] # 取alias事件

def get_alias_edge(src, dst):
    G = load_graph()
    p = args.p
    q = args.q
    unnormalized_probs = []
    # 论文3.2.2节核心算法，计算各条边的转移权重
    for dst_nbr in sorted(G.neighbors(dst)):
        if dst_nbr == src:
            unnormalized_probs.append(G[dst][dst_nbr]['weight'] / p)
        elif G.has_edge(dst_nbr, src):
            unnormalized_probs.append(G[dst][dst_nbr]['weight'])
        else:
            unnormalized_probs.append(G[dst][dst_nbr]['weight'] / q)

    # 归一化各条边的转移权重
    norm_const = sum(unnormalized_probs)
    normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]

    # 执行 Alias Sampling
    return alias_setup(normalized_probs)

def alias_nodes():
    G = load_graph()
    is_directed = args.directed
    alias_node = {}
    # 节点概率alias sampling和归一化
    for node in G.nodes():
        unnormalized_probs = [G[node][nbr]['weight'] for nbr in sorted(G.neighbors(node))]
        norm_const = sum(unnormalized_probs)
        normalized_probs = [float(u_prob) / norm_const for u_prob in unnormalized_probs]
        alias_node[node] = alias_setup(normalized_probs)
    return alias_node

def alias_edges():
    G = load_graph()
    alias_edges = {}
    triads = {}
    is_directed = args.directed
    # 边概率alias sampling和归一化
    if is_directed:
        for edge in G.edges():
            alias_edges[edge] = get_alias_edge(edge[0], edge[1])
    else:
        for edge in G.edges():
            alias_edges[edge] = get_alias_edge(edge[0], edge[1])
            alias_edges[(edge[1], edge[0])] = get_alias_edge(edge[1], edge[0])

