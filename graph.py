import sys
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import argparse as agp


### Further implementations :
# parse and using json too

### Filters
# --remote
# --local
# --tcp_con < LISTENING | ESTABLISHED | CLOSED | CLOSE_WAIT >
# --udp_con
# --ip <ADDR>
# --pid <SOMETHING>
# --service_name=
        
def error(strerr):
    print(strerr)
    exit(-1)

def find_local_addr(df : pd.DataFrame):
    local_addr = df["LocalAddr"]
    resume = set()

    for addr in local_addr:
        if "::" in addr:
            continue
        if addr.startswith('192.168')\
            or addr.startswith('10'):
            resume.add(addr)
        elif addr.startswith('172'):
            for i in range(16, 31):
                if addr.startswith('172' + str(i)):
                    resume.add(addr)
    print(resume)
    return resume

def get_local_conn(df : pd.DataFrame):
    local_df = df[(df["LocalAddr"].isin(["127.0.0.1"])) & (df["State"] != 'LISTENING')]
    return nx.from_pandas_edgelist(local_df, source='LocalPort', target='ForeignPort')

def get_private_conn(df : pd.DataFrame, addr:list):
    priv_df = df[(df["ForeignAddr"].isin(addr)) & (df["State"] != 'LISTENING')]
    graph_local = nx.from_pandas_edgelist(priv_df, source='LocalAddr', target='LocalPort')
    graph_port = nx.from_pandas_edgelist(priv_df, source='LocalPort', target='ForeignPort')
    graph_remote = nx.from_pandas_edgelist(priv_df, source='ForeignAddr', target='ForeignPort')
    graph = nx.compose_all([graph_local, graph_remote, graph_port])
    return graph

def get_remote_conn(df : pd.DataFrame):
    remote_df = df[(df["LocalAddr"] != '127.0.0.1') & (df["State"] != 'LISTENING')]
    graph_local = nx.from_pandas_edgelist(remote_df, source='LocalAddr', target='LocalPort')
    graph_foreign = nx.from_pandas_edgelist(remote_df, source='LocalPort', target='ForeignAddr')
    graph = nx.compose_all([graph_local, graph_foreign])
    return graph
    
    
if __name__ == '__main__':

    center = "machine"
    lst_source_attr = ["LocalAddr", "LocalPort", "PID", "Owner"]
    lst_target_attr = ["ForeignAddr", "ForeignPort"]
    lst_edge_attr = ["Proto", "State", "Created"]
    source_ep = "Owner"
    target_ep = "ForeignAddr"
    
    if sys.argv.__len__() != 2:
        error("Wrong arguments : please enter the name of the file only.")
    filename = sys.argv[1]
    if filename.__len__() < 5 and filename.count(".") != 1 and filename.find(".csv") != 1:
        error("Wrong file name.")

    net_df = pd.read_csv(filename, header=0)
    graph_local = get_local_conn(net_df)
    graph_priv = get_private_conn(net_df, find_local_addr(net_df))
    graph_remote = get_remote_conn(net_df)
    G = nx.compose_all([graph_local,graph_priv, graph_remote])
    nx.draw_networkx(G, with_labels=True)
    plt.show()