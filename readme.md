### DeepWalk   1阶

采用完全随机游走生成结点序列，使用word2vec方法训练结点嵌入向量。skip-gram和CBOW。

缺点：仅能反映相邻结点的社群相似信息，无法反映结点之间的功能与关系。

### Node2Vec

是Deepwalk的增强版。下一个移动的位置不仅取决于当前结点的位置，并且取决于上一个结点。不同的p、q值代表了不同的采样策略和探索范围。

p大q小：DFS倾向于向更远处的结点移动

p小q大：BFS倾向于向源节点临近结点移动

![](C:\Users\oyjl\AppData\Roaming\Typora\typora-user-images\image-20220824163737074.png)

#### Node2Vec中的Alias采样算法：

​	Alias以空间换时间进行采样。

##### （1）做表。

![image-20220825104640913](C:\Users\oyjl\AppData\Roaming\Typora\typora-user-images\image-20220825104640913.png)

##### （2）根据表采样。

![image-20220825104736347](C:\Users\oyjl\AppData\Roaming\Typora\typora-user-images\image-20220825104736347.png)

