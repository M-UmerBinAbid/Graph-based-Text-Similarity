import os
import numpy as np
import matplotlib.pyplot as plt


# Function: Clean text by keeping only lowercase letters and digits

def clean_text_basic(text):
    cleaned = ""
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789 "
    text = text.lower()
    for ch in text:
        if ch in allowed:
            cleaned += ch
        else:
            cleaned += " "
    final_text = ""
    previous_space = False
    for ch in cleaned:
        if ch == " " and previous_space:
            continue
        if ch == " ":
            previous_space = True
        else:
            previous_space = False
        final_text += ch
    final_text = final_text.strip()
    return final_text


# Function: Tokenize text into words using spaces

def tokenize_basic(text):
    tokens = []
    current = ""
    for ch in text:
        if ch == " ":
            if current != "":
                tokens.append(current)
                current = ""
        else:
            current += ch
    if current != "":
        tokens.append(current)
    return tokens


# Function: Remove common English stopwords from token list

def remove_stopwords_basic(tokens):
    stopwords = [
        # pronouns
        "i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves",
        "he","him","his","himself","she","her","hers","herself","it","its","itself",
        "they","them","their","theirs","themselves",
        # articles
        "a","an","the",
        # conjunctions
        "and","but","or","nor","so","for","yet",
        # prepositions
        "about","above","across","after","against","along","among","around","at","before","behind","below","beneath",
        "beside","between","beyond","by","despite","down","during","except","for","from","in","inside","into",
        "like","near","of","off","on","onto","out","outside","over","past","since","through","throughout","to",
        "toward","under","underneath","until","up","upon","with","within","without",
        # auxiliary verbs
        "am","is","are","was","were","be","been","being","do","does","did","have","has","had","having",
        "will","would","shall","should","can","could","may","might","must",
        # adverbs
        "again","almost","already","also","always","even","ever","just","never","not","only","perhaps","really",
        "sometimes","soon","still","then","there","thus","very","yet",
        # determiners
        "all","any","both","each","few","many","more","most","other","several","some","such",
        # other common words
        "that","this","these","those","here","how","why","what","which","who","whom","whose","where","when","after",
        "before","because","as","if","while","though","although","once","since","until"
    ]
    filtered = []
    for t in tokens:
        if t not in stopwords:
            filtered.append(t)
    return filtered


# Function: Build a co-occurrence graph from tokens

def build_graph_basic(tokens, window_size=4):
    nodes = {}
    edges = {}
    # count nodes
    for t in tokens:
        if t in nodes:
            nodes[t] += 1
        else:
            nodes[t] = 1
    n = len(tokens)
    for i in range(n):
        window = []
        for j in range(i, i + window_size):
            if j < n:
                window.append(tokens[j])
        for a in range(len(window)):
            for b in range(a+1, len(window)):
                t1 = window[a]
                t2 = window[b]
                if t1 == t2:
                    continue
                pair = tuple(sorted((t1, t2)))
                if pair in edges:
                    edges[pair] += 1
                else:
                    edges[pair] = 1
    return {"nodes": nodes, "edges": edges}


# Function: Plot a graph of top tokens and their co-occurrences

def plot_graph_basic(G, title="Graph", max_nodes=20):
    tokens = list(G["nodes"].keys())
    # manual sorting by frequency
    for i in range(len(tokens)):
        for j in range(i+1,len(tokens)):
            if G["nodes"][tokens[j]] > G["nodes"][tokens[i]]:
                temp = tokens[i]
                tokens[i] = tokens[j]
                tokens[j] = temp
    top_tokens = tokens[:max_nodes]
    theta = np.linspace(0,2*np.pi,len(top_tokens))
    xs = []
    ys = []
    for t in theta:
        xs.append(np.cos(t))
        ys.append(np.sin(t))
    plt.figure(figsize=(7,7))
    for i in range(len(top_tokens)):
        plt.scatter(xs[i], ys[i])
        plt.text(xs[i], ys[i], top_tokens[i])
    edges = list(G["edges"].keys())
    for k in range(len(edges)):
        a,b = edges[k]
        if a in top_tokens and b in top_tokens:
            i1 = top_tokens.index(a)
            i2 = top_tokens.index(b)
            plt.plot([xs[i1], xs[i2]], [ys[i1], ys[i2]], alpha=0.4)
    plt.title(title)
    plt.axis("off")
    plt.show()


# Function: Load BBC News dataset from folder structure

def load_bbc_news(folder_path):
    categories = ["sport","politics","business","entertainment","tech"]
    data = {}
    for cat in categories:
        cat_folder = os.path.join(folder_path, cat)
        texts = []
        fnames = os.listdir(cat_folder)
        sorted_fnames = []
        for fname in fnames:
            if fname.endswith(".txt"):
                sorted_fnames.append(fname)
        sorted_fnames.sort()
        for fname in sorted_fnames:
            path = os.path.join(cat_folder, fname)
            try:
                f = open(path,"r",encoding="utf-8")
                content = f.read()
                f.close()
            except UnicodeDecodeError:
                f = open(path,"r",encoding="latin-1")
                content = f.read()
                f.close()
            texts.append(content)
        data[cat] = texts
    return data


# Function: Run the pipeline to create and plot graphs for each news category

def run_category_graphs():
    folder_path = r"D:\SEMESTER 5\GT\Project\BBC News Summary\News Articles"
    data = load_bbc_news(folder_path)
    categories = ["sport","politics","business","entertainment","tech"]
    
    for cat in categories:
        if cat in data:
            texts = data[cat]
            print(f"\nProcessing category: {cat} ({len(texts)} articles)")
            
            # merge all articles in the category
            merged_text = " ".join(texts)
            
            # clean, tokenize, remove stopwords, and build graph
            cleaned_text = clean_text_basic(merged_text)
            tokens = tokenize_basic(cleaned_text)
            filtered_tokens = remove_stopwords_basic(tokens)
            graph = build_graph_basic(filtered_tokens)
            
            print(f"Plotting graph for category: {cat}","[23K-0009 &23K-0048]-Sec:5C")
            plot_graph_basic(graph, title=f"{cat.capitalize()} Category Graph-[23K-0009 &23K-0048]-Sec:5C")

if __name__=="__main__":
    run_category_graphs()
