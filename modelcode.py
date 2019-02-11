import pandas as pd
import numpy as np
import networkx as nx
import random
import efficient_apriori
from pyvis.network import Network
# import apyori
# import matplotlib.pyplot as plt
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
    # ----------------------------------------------------------------------------------------------------------

    records = []
    for i in range(0, len(df_i)):
        records.append([str(df_i.values[i, j]) for j in range(0, 20) if df_i.loc[i, j] != 'nan'])

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
    # ----------------------------------------------------------------------------------------------------------

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



    col = ['#e6194b', 'orangered', '#46f0f0', '#bcf60c', '#808080', '#911eb4',
           '#000000', '#46f0f0', '#f032e6', '#bcf60c', '#3cb44b', '#ffe119',
           '#4363d8', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8',
           '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#e6194b',
           '#bcf60c', '#808080', '#911eb4', '#46f0f0', '#f032e6',
           '#bcf60c', '#3cb44b', '#ffe119', '#4363d8', '#fabebe', '#008080', '#e6beff',
           '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075']

    # ----------------------------------------------------------------------------------------------------------

    con_vars = [x * 0.10 for x in range(1, 11)]
    con_vars = np.round(con_vars, 2)

    allrules = {}
    lenrules = []
    for var in con_vars:
        _, rules = efficient_apriori.apriori(records, min_support=0.01, min_confidence=var)
        allrules[var] = rules
        lenrules.append(len(allrules[var]))
    #
    # figcon, axcon = plt.subplots(1, 1)  # , figsize=(8, 6)
    # ax = axcon
    # ax.plot(con_vars, lenrules, '-o', label='numer of association rules ', color=(0.2, 0.7, 0.9, 0.9))
    # plt.legend(fontsize=35, loc='upper right')
    # plt.xlabel('Min required confidence level based on support of 1%', fontsize=35)
    # plt.ylabel('Number of association rules', fontsize=35)
    # plt.tick_params(axis='both', labelsize=35)
    # mpld3.save_html(figcon, 'static/confidence.html')

    # ------------------------------------------------------------
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
    # ------------------------------------------------------------
    com = community.girvan_newman(g)
    communities = list(com)
    node_com = {}
    nb_com = len(communities)
    cl = np.ceil(nb_com / 4)
    clusters = communities[int(cl)]
    for i in range(len(list(clusters))):
        for j in list(clusters)[i]:
            node_com[j] = i

    node_colors = []
    node_colorsg = {}
    for node in g.nodes():
        for j in range(len(clusters)):
            if node_com[node] == j:
                node_colors.append(col[j])
                node_colorsg[node] = col[j]
    # ------------------------
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
    # ------------------------------------------------------------

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


    # ------------------------
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
    # ------------------------
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

    final_package = cc[count]
    # final_package_df = pd.DataFrame.from_dict(final_package)
    soft_clusters = soft_clusters.dropna(axis=0)
    # clusters_out_df = clusters_out_df.drop([0], axis=1)

    # ------------------------
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