from alias_sampling import alias_draw,alias_edges,alias_nodes,load_graph

def node2vec_walk(walk_length, start_node):
    '''
    从指定的起始节点，生成一个随机游走序列
    '''
    # 上一步计算出的alias table，完成O(1)的采样
    G = load_graph()
    walk = [start_node]
    alias_edge = alias_edges()
    alias_node = alias_nodes()
    #  直到生成长度为walk_length的节点序列位为止
    while len(walk) < walk_length:
        cur = walk[-1]
        # 对邻居节点排序，目的是和alias table计算时的顺序对应起来
        cur_nbrs = sorted(G.neighbors(cur))
        if len(cur_nbrs) > 0:
            # 节点序列只有一个节点的情况
            if len(walk) == 1:
                walk.append(cur_nbrs[alias_draw(alias_node[cur][0], alias_node[cur][1])])
            # 节点序列大于一个节点的情况
            else:
                # 看前一个节点,prev是论文中的节点t
                prev = walk[-2]
                next = cur_nbrs[alias_draw(alias_edge[(prev, cur)][0],
                    alias_edge[(prev, cur)][1])]
                walk.append(next)
        else:
            break
    return walk




if __name__ == '__main__':
    node2vec_walk(7,4)