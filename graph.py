import sys
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import argparse as agp


### Further implementations :
# parse and using json too

        
def error(strerr):
    print(strerr)
    exit(-1)
    
known_addr = ["127.0.0.1", "0.0.0.0", "::"]

## Filters
# --remote
# --local
# --tcp_con < LISTEN | ESTABLISHED | CLOSED | CLOSE_WAIT >
# --udp_con
# --ip <ADDR>
# --pid <SOMETHING>
# --service_name=

# --uncentered

def atoi(string : str):
    ret = 0
    for i in range(len(string)):
        ret = ret * 10 + i
    return ret

def itoa(num : int):
    ret = str()
    while num > 0:
        ret += str(num % 10)
        num /= 10
    return ret

def find_local_addr(df : pd.DataFrame):
    local_addr = df["LocalAddr"]
    resume = set()

    for addr in local_addr:
        for known in known_addr:
            if known == addr:
                resume.add(addr)

    for addr in local_addr:
        addr_num = list(map(atoi, addr.split(".")))
        if addr_num[0] == 10:
            resume.add(".".join(map(itoa(), addr_num)))
        elif addr_num[0] == 198 and addr_num[1] == 168:
            resume.add(".".join(map(itoa(), addr_num)))
        elif addr_num[0] == 172 and addr_num[1] >= 16 and addr_num[1] <= 31:
            resume.add(".".join(map(itoa(), addr_num)))
    return resume
    
if __name__ == '__main__':
    center = "machine"
    lst_source_attr = ["LocalAddr", "LocalPort", "PID", "Owner"]
    lst_target_attr = ["ForeignAddr", "ForeignPort"]
    lst_edge_attr = ["Proto", "State", "Created"]
    source_ep = "LocalPort"
    target_ep = "ForeignAddr"

    if sys.argv.__len__() != 2:
        error("Wrong arguments : please enter the name of the file only.")
    filename = sys.argv[1]
    if filename.__len__() < 5 and filename.count(".") != 1 and filename.find(".csv") != 1:
        error("Wrong file name.")

    net_df = pd.read_csv(filename, header=0)
    local_addr = find_local_addr(net_df)

    graph = nx.from_pandas_edgelist(net_df, source=source_ep, target=target_ep, edge_attr=lst_edge_attr)
    graph = nx.contracted_nodes(graph, "0.0.0.0", "::")
    
    nx.draw_networkx(graph, with_labels=True)
    plt.show()