import pandas as pd
import numpy as np
import networkx as nx
import random
import efficient_apriori
from pyvis.network import Network
# import apyori
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
# from io import BytesIO
# import base64
import mpld3
# import json


def simulfunc():

    try:
        df_i = pd.read_csv('static/inputfile_arm.csv', header=None)
        df_i = df_i.astype(str)


    except FileNotFoundError:
        df_i = pd.read_csv('static/store_data.csv', header=None)
        df_i = df_i.astype(str)

    # -----------------------------------------------------------------------------------------------------------------

    records = []
    for i in range(0, len(df_i)):
        records.append([str(df_i.values[i, j]) for j in range(0, 20) if df_i.loc[i, j] != 'nan'])
    # -----------------------------------------------------------------------------------------------------------------
    #  Explore the data: use different support and confidence levels to see how number of apssociations
    #  change and what are the associated metrics: support, confidence, conviction,  lift
    itemsets, r = efficient_apriori.apriori(records, min_support=0.02, min_confidence=0.3)

    s = []
    cv = []
    c = []
    lift = []
    nn = []
    nd = {}

    count = 0
    for i in r:
        s.append(i.support) # support measure
        cv.append(i.conviction) # conviction measure
        c.append(i.confidence) # condidence measure
        lift.append(i.lift)
        n = []
        for m in i.lhs:
            n.append(m)

        for l in i.rhs:
            n.append(l)
        nd[count] = n
        count += 1
        nn.append(n)

    figbar, axbar = plt.subplots(1, 1, figsize=(15, 15))
    ax = axbar
    x = range(len(s))
    jn = [', '.join(a) for a in nn]
    x_labels = jn
    y = s
    ax.barh(x, y, color=(0.7, 0.3, 0.3, 0.6), align='center')  # , color=color
    plt.yticks(x, x_labels)
    plt.tick_params(axis='both', labelsize=18)
    plt.xlabel('Support level', fontsize=15)
    plt.legend()
    plt.savefig('static/barchart.png', bbox_inches='tight')
    mpld3.save_html(figbar, 'static/barchart.html')
    # ----------------------------------------------------------------------------------------------------------
    # You can look at the trajectory of number of frequent combinations at different selected support level (normalized frequency):

    cat_vars = [x * 0.01 for x in range(0, 20)]
    allrules = {}
    allsets = {}
    lenrules = []
    lensets = []
    itemsets = {}
    for var in cat_vars[1:]:
        allsets[var] = 0
        ti = efficient_apriori.itemsets_from_transactions(records, min_support=var)
        itemsets[var] = ti
        for ii in range(len(ti[0])):
            allsets[var] = allsets[var] + len(ti[0][ii + 1])
        lensets.append(allsets[var])

    # figsupp, axsupp = plt.subplots(1, 1, figsize=(10, 8))
    # ax = axsupp
    # ax.plot(cat_vars[1:], lensets, '-o', color='#e6194b')
    # plt.legend(fontsize=18, loc='upper right')
    # plt.xlabel('Support Level', fontsize=18)
    # plt.ylabel('Number of Frequent Baskets', fontsize=18)
    # plt.tick_params(axis='both', labelsize=18)
    # plt.xlim(0, 0.2)

    # mpld3.save_html(figsupp, 'support.html')
    # ----------------------------------------------------------------------------------------------------------
    # You can look at the trajectory of number of associations found between combinations at your selected support level:

    #  if you are not sure about entering min_support, min_confidence you can set up support and confidence as a
    #  function of var (in the following for loop) such that a certain level of your desired metric
    #  (conviction, lift, ..) is maintained

    con_vars = [x * 0.10 for x in range(1, 11)]
    con_vars = np.round(con_vars, 2)

    allrules = {}
    lenrules = []
    for var in con_vars:
        _, rules = efficient_apriori.apriori(records, min_support=0.01, min_confidence=var)
        allrules[var] = rules
        lenrules.append(len(allrules[var]))
    # figcon, axcon = plt.subplots(1, 1)  # , figsize=(8, 6)
    # ax = axcon
    # ax.plot(con_vars, lenrules, '-o', label='numer of association rules ', color=(0.2, 0.7, 0.9, 0.9))
    # plt.legend(fontsize=35, loc='upper right')
    # plt.xlabel('Min required confidence level based on support of 1%', fontsize=35)
    # plt.ylabel('Number of association rules', fontsize=35)
    # plt.tick_params(axis='both', labelsize=35)
    # mpld3.save_html(figcon, 'static/confidence.html')
    # -----------------------------------------------------------
    # gall: is the network of items that are associated with low confidence level, in order to see most available associations

    itemsets, r = efficient_apriori.apriori(records, min_support=0.01, min_confidence=0.01)
    Gall = nx.Graph()
    c = 1
    for i in r:
        node_list = []
        for j in i.lhs:
            node_list.append(j)
        for j in i.rhs:
            node_list.append(j)
        for j in range(len(node_list) - 1):
            for k in range(j + 1, len(node_list)):
                Gall.add_edge(node_list[j], node_list[k])

    Gallnodes = list(Gall.nodes)
    gall = Network()
    d = nx.degree(Gall)
    dd = dict(d)
    # ------------------------------------------------------------------------------------------------------------------
    c = 1
    # node_list = []
    for i in r:
        node_list = []
        for j in i.lhs:
            node_list.append(j)
        for j in i.rhs:
            node_list.append(j)
        for j in range(len(node_list) - 1):
            for k in range(j + 1, len(node_list)):
                gall.add_node(node_list[j], value=dd[node_list[j]],
                              color='#e6194b')  # (0.8,0.2,0.8,0.9) 46f0f0'#ffe119' '#f032e6'
                gall.add_node(node_list[k], value=dd[node_list[k]], color='#e6194b')
                gall.add_edge(node_list[j], node_list[k], color='#fabebe')
    # ------------------------------------------------------------------------------------------------------------------
    # choose appropiriate min_support, min_confidence based on data:  elbow in figures support.html and confidence.html
    # min_support=0.01, min_confidence=0.3

    g = nx.Graph()
    c = 1
    algeallrules = list(allrules.keys())[2]
    for i in allrules[algeallrules]:
        node_list = []
        for j in i.lhs:
            node_list.append(j)
        for j in i.rhs:
            node_list.append(j)
        for j in range(len(node_list) - 1):
            for k in range(j + 1, len(node_list)):
                g.add_edge(node_list[j], node_list[k])

    d = nx.degree(g)
    dd = dict(d)
    # -----------------------------------------------------------------------------------------------------------------
    #  if you want to get the red graph in slides:
    # gn = Network()
    # c = 1
    # algeallrules = list(allrules.keys())[2]
    # for i in allrules[algeallrules]:
    #     node_list = []
    #     for j in i.lhs:
    #         node_list.append(j)
    #     for j in i.rhs:
    #         node_list.append(j)
    #     for j in range(len(node_list) - 1):
    #         for k in range(j + 1, len(node_list)):
    #             #             gg.add_edge(node_list[j], node_list[k])
    #             gn.add_node(node_list[j], value=dd[node_list[j]], color='#e6194b')
    #             gn.add_node(node_list[k], value=dd[node_list[k]], color='#e6194b')
    #             gn.add_edge(node_list[j], node_list[k])
    #
    # node_list_g = list(set(node_list))
    # gn.save_graph('static/ggrule3percentconf.html')

    # -----------------------------------------------------------------------------------------------------------------
    # community.girvan_newman uses edgebetween ness to detect communities in graph, and finds hierachical clusters
    # final communities are disjoint clusters, meaning they do not have any common items
    com = community.girvan_newman(g)
    communities = list(com)
    node_com = {}
    nb_com = len(communities)
    cl = np.ceil(nb_com / 4)
    clusters = communities[int(cl)]
    for i in range(len(list(clusters))):
        for j in list(clusters)[i]:
            node_com[j] = i


    col = ['#e6194b', 'orangered', '#46f0f0', '#bcf60c', '#808080','#911eb4','#000000', '#46f0f0', '#f032e6', '#bcf60c',
           '#3cb44b', '#ffe119', '#4363d8', '#fabebe', '#008080', '#e6beff', '#9a6324','#fffac8',  '#800000', '#aaffc3',
           '#808000', '#ffd8b1', '#000075', '#e6194b','#bcf60c', '#808080', '#911eb4', '#46f0f0', '#f032e6','#bcf60c',
           '#3cb44b', '#ffe119', '#4363d8', '#fabebe', '#008080', '#e6beff','#9a6324', '#fffac8', '#800000', '#aaffc3',
           '#808000', '#ffd8b1', '#000075']

    node_colors = []
    node_colorsg = {}
    for node in g.nodes():
        for j in range(len(clusters)):
            if node_com[node] == j:
                node_colors.append(col[j])
                node_colorsg[node] = col[j]
    # -----------------------------------------------------------------------------------------------------------------
    c = 0
    clusters_out = {}
    for i in range(len(clusters)):
        if len(clusters[i]) > 1:
            clusters_out[c] = clusters[i]
            c += 1
    clusters_out_df = pd.DataFrame.from_dict(clusters_out, orient='index')
    clusters_out_df = clusters_out_df.T
    clusters_out_df = clusters_out_df.fillna(' ')

    colnames = []
    for i in clusters_out_df.columns:
        col = 'Recommended Basket ' + str(i + 1)
        colnames.append(col)

    clusters_out_df.columns = colnames

    dg = nx.degree(g)
    ddg = dict(d)
    # -----------------------------------------------------------------------------------------------------------------
    gg = Network()
    c = 1
    algeallrules = list(allrules.keys())[2]
    for i in allrules[algeallrules]:
        node_list = []
        for j in i.lhs:
            node_list.append(j)
        for j in i.rhs:
            node_list.append(j)
        for j in range(len(node_list) - 1):
            for k in range(j + 1, len(node_list)):
                #             gg.add_edge(node_list[j], node_list[k])
                gg.add_node(node_list[j], value=ddg[node_list[j]], color=node_colorsg[node_list[j]])
                gg.add_node(node_list[k], value=ddg[node_list[k]], color=node_colorsg[node_list[k]])
                gg.add_edge(node_list[j], node_list[k])

    node_list_g = list(set(node_list))
    gg.save_graph('static/ggrule3percentconf_c.html')
    # -----------------------------------------------------------------------------------------------------------------
    # if you need nto export graph in json file for better visualization,  here you go:

    # nodes = [{'name': str(i), 'club': gg.node[i]}
    #          for i in g.nodes()]
    # links = [{'source': u[0], 'target': u[1]}
    #          for u in gg.edges()]
    # with open('graph.json', 'w') as f:
    #     json.dump({'nodes': nodes, 'links': links},
    #               f, indent=4,)
    # ------------------------------------------------------------------------------------------------------------------
    cc = {}
    for i in range(3, int(len(g.nodes) / 2)):
        cc[i] = []
        nb_clus = len(list(k_clique_communities(g, i)))
        for c in range(nb_clus):
            tt = list(list(k_clique_communities(g, i))[c])
            cc[i].append(tt)
        cc[i] = sorted(cc[i])

    soft_clusters = pd.DataFrame.from_dict(cc, orient='index')
    soft_clusters.reset_index(inplace=True, drop=True)
    # ------------------------------------------------------------------------------------------------------------------
    #  notice in graph  that mineral water, spagetti  and .. are densly connected woth other clusters:
    #  we may want to construct clusters that allow having shred items
    #  k_clique_communities uses cliques of different size to detect communities in graph,
    #  final communities are overlapping clusters, meaning they are allowed to have common items
    cc = {}
    final_package = {}
    count = 0
    for i in range(3, int(len(g.nodes) / 3)):
        cc[i] = []
        nb_clus = len(list(k_clique_communities(g, i)))
        if count < nb_clus:
            count = i
        for c in range(nb_clus):
            tt = list(list(k_clique_communities(g, i))[c])
            cc[i].append(tt)
        cc[i] = sorted(cc[i])

    # final_package = cc[count]
    soft_clusters = soft_clusters.dropna(axis=0)
    # -----------------------------------------------------------------------------------------------------------------
    overlapping_clusters = pd.DataFrame(columns=[0])
    for i in range(len(soft_clusters)):
        l = []
        temp = soft_clusters.iloc[i]
        for j in temp:
            l.append(j)
        df1 = pd.DataFrame(l).T
        overlapping_clusters = pd.concat([overlapping_clusters, df1], ignore_index=True, axis=1)

    overlapping_clusters = overlapping_clusters.drop([0], axis=1)
    overlapping_clusters = overlapping_clusters.fillna(' ')
    colnames_over = []
    for i in overlapping_clusters.columns:
        col = 'Recommended Basket' + str(i)
        colnames_over.append(col)
    overlapping_clusters.columns = colnames_over
    overlapping_clusters = overlapping_clusters[overlapping_clusters.columns[:3]]

    overlapping_clusters.to_csv('static/soft_clusters.csv', index=False)
    #     final_package_df.to_csv('static/final_package_df.csv')
    clusters_out_df.to_csv('static/clusters_out_df.csv', index=False)