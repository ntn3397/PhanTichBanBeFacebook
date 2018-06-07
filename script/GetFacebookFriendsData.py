import networkx as nx
import facebook
import queue
import requests
import csv
import glob
import os

if __name__ == '__main__':
    #tao graph networkx
    g = nx.Graph()
    #tao hang doi xep theo thu tu levels ten q
    q = queue.PriorityQueue()
    #tao graph de lay du lieu facebook
    graph = facebook.GraphAPI(access_token= "EAACEdEose0cBAI1ajhMmopoC7xGOhgsZCNrHJqPhB9iZCMAEjBsdBCqoBCErDjA96Rl1QSCotXtKRICZBubbQkZBmd5AYS6okOCMDG7XGl3lKWh9NslqgCVIBWIBd8UcHpP8N9y9wpeJs3ZBlojqInu4s4QZAWF1QZBsnvGoKjnIMonjQyLdM4yZBzaKNTEen1cZD",version="2.7")
    #tu graph lay du lieu tu me
    me = graph.get_object("me")
    #tao dict levels de danh so uu tien nguoi duyet trong hang doi
    #Thuat toan:
    #- Dau tien se lay danh sach ban be cua minh
    #- Sau do se duyet tiep danh sach ban be cua ban be
    #- Roi lai duyet tiep ban be cua ban be cua ban be
    #- Moi danh sach ban be nhu vay se co cap do
    levels = {}
    #- Dat cap do cua minh la 0
    levels[me['id']] = 0
    #- explored la mot tupe luu tru nhung id da tim thay roi
    explored = []
    explored = [me['id']]
    #- visited la mot tupe luu tru nhung id da duyet roi
    visited = []
    visited = [me['id']]
    #Cho vao hang doi mot tupe gom (level, ten, id) cua minh
    q.put((levels[me['id']],me['name'], me['id']))
    #Dat so dem
    count = 0
    #Tao ra mot Dict co the luu tru List
    #from collections import defaultdict
    #Ten Dict la ds
    #ds=defaultdict(list)
    #tao rows
    rows = []
    #Khi hang doi queue q chua rong thi chay
    while not q.empty():
        #Lay ra phan tu co level thap nhat
        node = q.get();
        #-Ghi chu:
        #node[0] : levels
        #node[1] : name
        #node[2] : id
        
        userLevel= node[0]
        userName = node[1]
        userId = node[2]
        userFriends = []
        
    
        #tang so dem len 1
        count = count + 1
        #in ra lan duyet, id, ten, levels
        print("lan duyet :%s, id:%s, ten:%s, levels:%s"%(count,node[2],node[1], node[0]))
        #them phan tu node do vao explored
        explored.append(node)
        #them vao visited id ban moi tim thay
        visited.append(node[2])
        #Tao str ghi lai "id"/friends
        str = "%s/friends"%node[2]
        try:
            #Lay du lieu ban be tu "id" phia tren
             friends_object = graph.get_object(str)           
        except facebook.GraphAPIError:
            pass
       
        while(True):
            try:
                #moi dong` ban trong friends_object thi lam nhu sau
                for friend in friends_object['data']:
                    #tao canh cho node
                    g.add_edge(node[2],friend['id'])
                    userFriends.append((userId,friend['id']))
                    #neu nhu ban do chua co trong tupe visited
                    if friend['id'] not in visited:
                        #in ra id ban do
                        print(friend['id'])
                        #dat levels cho id do la levels cua node + 1
                        #node o day la nguoi ma minh tim ban cua ho
                        levels[friend['id']] = levels[node[2]] + 1
                        #cho vao hang doi queue q mot tube gom level, ten, id cua ban moi tim
                        q.put((levels[friend['id']], friend['name'], friend['id']))                        
                        #cho vao dict ds, sau do co the in ra thong tin
                        #ds[node[2]].append(friend.copy())
                       
                #next page trong list ban be lay dc tren graph api facebook   
                friends_object=requests.get(friends_object['paging']['next']).json()
            except KeyError:
                break
        #tao kieu du lieu dict để lưu dữ liệu
        row = {"userLevel": userLevel,
               "userName": userName,
               "userId": userId,
               "userFriends": userFriends}
        rows.append(row)
        if node[0]==20:
            break
        
    # make a new csv and export it
    with open('../output/friends_data.csv', "w", encoding='utf8') as csvfile:
        fieldnames = ["userLevel", "userName", "userId","userFriends"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    
    #in ds
    #print(ds)
    #in so dinh
    print(g.number_of_nodes())
    #in so canh
    print(g.number_of_edges())
    
    #Xoa cac node co degree = 1
    remove = []
    for n in g.nodes():
        if(g.degree(n)==1):
            remove.append(n)
    
    g.remove_nodes_from(remove)
    #remove = [node for node,degree in g.degree().items() if degree == 1]
    
    #save_graph(g,'my_graph.png')
    nx.write_gexf(g, 'your_graph.gexf')
    #in tinh degree
    print(nx.degree_centrality(g))
    #in tinh betweenness
    print(nx.betweenness_centrality(g))
    #in tinh closeness
    print(nx.closeness_centrality(g))
    #in tinh eigenvector
    print(nx.eigenvector_centrality(g))
    

    