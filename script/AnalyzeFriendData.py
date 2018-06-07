# -*- coding: utf-8 -*-

import pandas as pd
import networkx as nx
from ast import literal_eval
#import matplotlib.pyplot as plt

#đọc dữ liệu từ file csv
df = pd.read_csv('../output/friends_data.csv')

#tao graph networkx
g = nx.Graph()

#nhập node vào đồ thị
for index, row in df.iterrows():
    g.add_node(row['userId'],name = row['userName'], level = row['userLevel'])

#nhập edge vào đồ thị 
for index, row in df.iterrows():
    if row['userFriends'] != []:
        l = literal_eval(row['userFriends'])
        g.add_edges_from(l)


print(g.number_of_nodes())
#in so canh
print(g.number_of_edges())
print('đồ thị bạn bè')
nx.draw(g)

nx.write_gexf(g, '../output/friend_data.gexf')

remove = []
for n in g.nodes():
    if(g.degree(n)<=1):
        remove.append(n)
    
g.remove_nodes_from(remove)
print('Đồ thị bạn bè đã xóa')
nx.draw(g)

nx.write_gexf(g, '../output/friend_data_cleaned.gexf')

#tính độ đo trung tâm
nx.degree_centrality(g)

#tính độ đo trung tâm dựa trên trung gian
nx.betweenness_centrality(g)

#tính độ đo trung tâm theo sự lân cận
nx.closeness_centrality(g)


