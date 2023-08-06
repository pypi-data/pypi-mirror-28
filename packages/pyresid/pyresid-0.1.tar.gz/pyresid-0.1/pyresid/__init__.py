#!/usr/bin/env python3
"""
pyresid
RESTful API docs here - http://europepmc.org/developers
                      - http://europepmc.org/RestfulWebService

author: robert.firth@stfc.ac.uk
"""

import re
import os
import requests
import json
import spacy as spacy
import numpy as np
from collections import OrderedDict
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

__author__ = "Rob Firth"
__all__ = ["request_fulltextXML",
           "parse_request",
           "get_text",
           "reconstruct_fulltext",
           "identify_residues",
           "locate_residues",
           "get_rawcontext",
           "aa_dict",
           "short_aa_dict",
           "setup_plot_defaults",
           "extract",
           ]



aa_dict = {"Ala":{"short_id": "A", "full_id":  "Alanine",},
           "Arg":{"short_id": "R", "full_id": "Arginine",},
           "Asn":{"short_id": "N", "full_id": "Asparagine",},
           "Asp":{"short_id": "D", "full_id": "Aspartic acid (Aspartate)",},
           "Cys":{"short_id": "C", "full_id": "Cysteine",},
           "Gln":{"short_id": "Q", "full_id": "Glutamine",},
           "Glu":{"short_id": "E", "full_id": "Glutamic acid (Glutamate)",},
           "Gly":{"short_id": "G", "full_id": "Glycine",},
           "His":{"short_id": "H", "full_id": "Histidine",},
           "Ile":{"short_id": "I", "full_id": "Isoleucine",},
           "Leu":{"short_id": "L", "full_id": "Leucine",},
           "Lys":{"short_id": "K", "full_id": "Lysine",},
           "Met":{"short_id": "M", "full_id": "Methionine",},
           "Phe":{"short_id": "F", "full_id": "Phenylalanine",},
           "Pro":{"short_id": "P", "full_id": "Proline",},
           "Ser":{"short_id": "S", "full_id": "Serine",},
           "Thr":{"short_id": "T", "full_id": "Threonine",},
           "Trp":{"short_id": "W", "full_id": "Tryptophan",},
           "Tyr":{"short_id": "Y", "full_id": "Tyrosine",},
           "Val":{"short_id": "V", "full_id": "Valine",},
           "Asx":{"short_id": "B", "full_id": "Aspartic acid or Asparagine",},
           "Glx":{"short_id": "Z", "full_id": "Glutamine or Glutamic acid.",},
           "Xaa":{"short_id": "X", "full_id": "Any amino acid.",},
           "TERM":{"short_id": None, "full_id": "termination codon",}
           }

short_aa_dict = {"A" :{"id": "Ala","full_id":  "Alanine",},
                 "R" :{"id": "Arg","full_id": "Arginine",},
                 "N" :{"id": "Asn","full_id": "Asparagine",},
                 "D" :{"id": "Asp","full_id": "Aspartic acid (Aspartate)",},
                 "C" :{"id": "Cys","full_id": "Cysteine",},
                 "Q" :{"id": "Gln","full_id": "Glutamine",},
                 "E" :{"id": "Glu","full_id": "Glutamic acid (Glutamate)",},
                 "G" :{"id": "Gly","full_id": "Glycine",},
                 "H" :{"id": "His","full_id": "Histidine",},
                 "I" :{"id": "Ile","full_id": "Isoleucine",},
                 "L" :{"id": "Leu","full_id": "Leucine",},
                 "K" :{"id": "Lys","full_id": "Lysine",},
                 "M" :{"id": "Met","full_id": "Methionine",},
                 "F" :{"id": "Phe","full_id": "Phenylalanine",},
                 "P" :{"id": "Pro","full_id": "Proline",},
                 "S" :{"id": "Ser","full_id": "Serine",},
                 "T" :{"id": "Thr","full_id": "Threonine",},
                 "W" :{"id": "Trp","full_id": "Tryptophan",},
                 "Y" :{"id": "Tyr","full_id": "Tyrosine",},
                 "V" :{"id": "Val","full_id": "Valine",},
                 "B" :{"id": "Asx","full_id": "Aspartic acid or Asparagine",},
                 "Z" :{"id": "Glx","full_id": "Glutamine or Glutamic acid.",},
                 "X" :{"id": "Xaa","full_id": "Any amino acid.",},
                 "None" :{"id": "TERM", "full_id": "termination codon",}
                 }

extract = lambda x, y: OrderedDict(zip(x, map(y.get, x)))


def setup_plot_defaults():
    """
    """

    plt.rcParams['ps.useafm'] = True
    plt.rcParams['pdf.use14corefonts'] = True
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.size'] = 14
    plt.rcParams['figure.subplot.hspace'] = 0.1
    plt.rc('font', family='sans-serif')
    plt.rc('font', serif='Helvetica')
    pass



class MyEncoder(json.JSONEncoder):
    """
    https://stackoverflow.com/a/27050186
    """
    def default(self, obj):
        if isinstance(obj, OrderedDict):
            return obj
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, spacy.tokens.token.Token):
            return str(obj)
        else:
            return super(MyEncoder, self).default(obj)

def request_fulltextXML(ext_id):
    """

    :param ext_id:
    :return:
    """
    request_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/" + ext_id + "/fullTextXML"

    r = requests.get(request_url)

    return r


def parse_request(ext_id):
    """

    :param ext_id:
    :return:
    """
    r = request_fulltextXML(ext_id=ext_id)
    soup = BeautifulSoup(r.text, "lxml-xml")

    return soup


def get_all_text(ext_id):
    """

    :param ext_id:
    :return:
    """

    return parse_request(ext_id=ext_id).get_text(" ")


def get_sections_text(ext_id, remove_tables=True, fulltext=False):
    """

    :param ext_id:
    :param remove_tables:
    :param fulltext:
    :return:
    """
    soup = parse_request(ext_id=ext_id)

    if remove_tables:
        for i in range(0, len(soup('table'))):  # https://stackoverflow.com/q/18934136
            soup.table.decompose()

    if fulltext:
        return " ".join([sec.get_text(" ") for sec in soup.findAll("sec")])
    else:
        text_dict = OrderedDict()
        for sec in soup.findAll("sec"):
            if not sec.find_parent("sec"):  # https://stackoverflow.com/a/31208775
                try:
                    sec_id = sec["id"]
                    title = sec.find("title")

                    if title:
                        title = title.text

                    text_dict[sec_id] = {"title": title, "text": sec.get_text(" ")}

                except:
                    pass

        return text_dict


def get_text(ext_id):
    """

    :param ext_id:
    :return:
    """

    text_dict = get_sections_text(ext_id=ext_id, remove_tables=True, fulltext=False)

    nlp = spacy.load('en')

    for i, sec in enumerate(text_dict):
        doc = nlp(text_dict[sec]["text"])
        text_dict[sec]["tokens"] = [t for t in doc]
        text_dict[sec]["len"] = len(text_dict[sec]["tokens"])

        if i == 0:
            text_dict[sec]["start"] = 0
        else:
            text_dict[sec]["start"] = text_dict[list(text_dict.keys())[i - 1]]["start"] + text_dict[sec]["len"]

    return text_dict


def reconstruct_fulltext(text_dict, tokenise=True):
    """

    :param text_dict:
    :param tokenise:
    :return:
    """
    fulltext = " ".join([text_dict[sec]["text"]for sec in text_dict])

    if tokenise:
        nlp = spacy.load('en')
        fulldoc = nlp(fulltext)
        fulltext_tokens = [t.text for t in fulldoc]

        return fulltext_tokens
    else:
        return fulltext


def identify_residues(fulltext, prefixes=None, short_prefixes=None, return_mentions=False, short=False):
    """

    :param fulltext:
    :param prefixes:
    :return:
    """

    if not prefixes:
        prefixes = list(aa_dict.keys())
    if not short_prefixes:
        short_prefixes = list(short_aa_dict.keys())
    # pattern = "[a-zA-Z]{3}\d+"
    pattern = "[a-zA-Z]{3}\d+/\d+|[a-zA-Z]{3}\d+"

    p = re.compile(pattern)

    unique_mentions = set([i.strip() for i in p.findall(fulltext) if "".join(filter(str.isalpha, i)) in prefixes])

    if short:
        unique_short_mentions = set([i.strip() for i in p.findall(fulltext) if "".join(filter(str.isalpha, i)) in short_prefixes])

        unique_mentions.update(unique_short_mentions)

    if return_mentions:
        return unique_mentions

    unique_residues = []
    for i in unique_mentions:
        print(i)
        if "/" in i:
            residue_position = ["".join(filter(str.isdigit, j)) for j in i.split("/")]
            aa_residue_id = [j for j in ["".join(filter(str.isalpha, i)) for i in i.split("/")] if j]
            decomposed = [x + y for x in aa_residue_id for y in residue_position]
            unique_residues += decomposed
        else:
            unique_residues.append(i)

    return set(unique_residues)


def decompose_slashed_residue(i):
    """

    :param i:
    :return:
    """
    if "/" in i:
        residue_position = ["".join(filter(str.isdigit, j)) for j in i.split("/")]
        aa_residue_id = [j for j in ["".join(filter(str.isalpha, i)) for i in i.split("/")] if j]
        decomposed = [x + y for x in aa_residue_id for y in residue_position]
        return decomposed
    else:
        return [i,]


def locate_residues(fulltext_tokens, unique_residues, fulldoc=None, offset=False, verbose=False):
    """

    :param fulltext_tokens:
    :param unique_residues:
    :param verbose:
    :return:
    """
    location_dict = OrderedDict()

    for tkn in unique_residues:
        if verbose:
            print(tkn)
        decomposed = decompose_slashed_residue(tkn)

        for newtkn in decomposed:
            if newtkn not in location_dict:
                location_dict[newtkn] = OrderedDict()
                if offset:
                    location_dict[newtkn]["offset"] = []
                location_dict[newtkn]["locations"] = []
                location_dict[newtkn]["string"] = []
                location_dict[newtkn]["freq"] = 0

            if verbose:
                print(newtkn)

            # locations = [word for word in enumerate(fulltext_tokens) if tkn in word[1]]
            locations = [word for word in enumerate(fulltext_tokens) if tkn in str(word[1])]  ## Should make it possible to pass spacy tokens
            if offset:
                location_dict[newtkn]["offset"]+=[word[1].idx for word in locations]

            location_dict[newtkn]["locations"]+=list(np.array(locations).T[0].astype(int))
            location_dict[newtkn]["string"]+=list(np.array(locations).T[1])
            location_dict[newtkn]["freq"]+=len(location_dict[newtkn]["locations"])

            if verbose:
                print(locations)

    return location_dict


def plot_locations(location_dict, text_dict, fulltext_tokens, n=None, title=None):
    """

    :param location_dict:
    :param text_dict:
    :param fulltext_tokens:
    :param n:
    :return:
    """

    keys_freqency_sorted = np.array(list(location_dict.keys()))[
        np.argsort([location_dict[res]["freq"] for res in location_dict])][::-1]

    if n:
        if n > len(keys_freqency_sorted):
            n = len(keys_freqency_sorted)
        plot_dict = extract(keys_freqency_sorted[:n], location_dict)
        keys_freqency_sorted = keys_freqency_sorted[:n]
    else:
        plot_dict = location_dict

    fig = plt.figure(figsize=[8, len(plot_dict.keys()) * 0.5])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    for i, key in enumerate(keys_freqency_sorted[::-1]):  # Frequency sorted
        ax1.scatter(plot_dict[key]["locations"], np.ones(len(plot_dict[key]["locations"])) * i, marker="|")

    orig_ylim = ax1.get_ylim()

    # ax1.plot([text_dict["Sec1"]["start"], text_dict["Sec1"]["start"], ],
    #          [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Introduction
    # ax1.text(text_dict["Sec1"]["start"], orig_ylim[1] - 1, "Introduction", rotation="vertical", ha="left")
    # ax1.plot([text_dict["Sec2"]["start"], text_dict["Sec2"]["start"], ],
    #          [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Results
    # ax1.text(text_dict["Sec2"]["start"], orig_ylim[1] - 1, "Results", rotation="vertical", ha="left")
    # ax1.plot([text_dict["Sec12"]["start"], text_dict["Sec12"]["start"], ],
    #          [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Discussion
    # ax1.text(text_dict["Sec12"]["start"], orig_ylim[1] - 1, "Discussion", rotation="vertical", ha="left")

    for sec in text_dict:
        ax1.plot([text_dict[sec]["start"], text_dict[sec]["start"], ],
                 [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Introduction
        ax1.text(text_dict[sec]["start"], orig_ylim[1] - 1, text_dict[sec]["title"], rotation="vertical", ha="left")


    plt.yticks(np.arange(len(plot_dict)), keys_freqency_sorted[::-1])

    if n:
        ax1.set_ylim([-0.5, n-0.5])
    else:
        ax1.set_ylim(orig_ylim)

    if title:
        ax1.set_title(title)

    ax1.set_xlim(-100, len(fulltext_tokens))
    plt.xlabel("Token Number")
    plt.ylabel("Amino Acid")
    pass


def find_clusters(residue_shortid, locations_dict):
    """

    :param residue_shortid:
    :param locations_dict:
    :return:
    """
    X = np.array([locations_dict[residue_shortid]["locations"],
                  list(np.array(locations_dict[residue_shortid]["locations"])*0+1)]).T  # Assume all are at the same y

    # generate the linkage matrix
    # Z = linkage(X, 'ward')
    # Z = linkage(X, 'single', metric="cosine")
    # Z = linkage(X, 'complete', metric="cosine")
    Z = linkage(X, 'average', metric="cosine")

    return Z


def plot_dendrogram(Z, max_d=None):
    """

    :param Z:
    :return:
    """
    fig = plt.figure(figsize=[10,10])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    # ax1.set_title(r'$\textnormal{Hierarchical Clustering Dendrogram}$')
    # ax1.set_xlabel(r'$\textnormal{sample index}$')
    # ax1.set_ylabel(r'$\textnormal{distance}$')

    ax1.set_title('Hierarchical Clustering Dendrogram')
    ax1.set_xlabel('sample index')
    ax1.set_ylabel('distance')

    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        ax=ax1
    )

    if max_d:
        plt.axhline(y=max_d, c='k')

    plt.show()
    pass


def plot_disthist(Z, bins=None, max_d=None):
    """

    :param Z:
    :param bins:
    :param max_d:
    :return:
    """
    if not bins:
        binsize = np.nanmax(Z.T[2]) / 20.
        bins = np.linspace(0, np.nanmax(Z.T[2]) + binsize, 100)

    fig = plt.figure(figsize=[8, 4])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    #     hist = ax1.hist(Z.T[2], bins=bins, cumulative=True)
    hist = ax1.hist(Z.T[2], bins=bins)

    if max_d:
        plt.axvline(x=max_d, c="k")

    ax1.set_title("Cluster Distance Histogram")
    ax1.set_xlabel("Distance")
    ax1.set_ylabel("Frequency")
    pass


def plot_clusters(X, Z, max_d, text_dict, fulltext_tokens, residue_shortid):
    """

    :param location_dict:
    :param text_dict:
    :param fulltext_tokens:
    :param n:
    :return:
    """

    clusters = fcluster(Z, max_d, criterion='distance')

    fig = plt.figure(figsize=[8,1])
    fig.subplots_adjust(left=0.15, bottom=0.08, top=0.99,
                        right=0.99, hspace=0, wspace=0)

    ax1 = fig.add_subplot(111)

    ax1.scatter(X[:, 0], X[:, 1], c=clusters, cmap='plasma', marker="|", s=100)

    orig_ylim = ax1.get_ylim()

    ax1.plot([text_dict["Sec1"]["start"], text_dict["Sec1"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Introduction
    ax1.text(text_dict["Sec1"]["start"], orig_ylim[1], "Introduction", rotation="vertical", ha="left")
    ax1.plot([text_dict["Sec2"]["start"], text_dict["Sec2"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Results
    ax1.text(text_dict["Sec2"]["start"], orig_ylim[1], "Results", rotation="vertical", ha="left")
    ax1.plot([text_dict["Sec12"]["start"], text_dict["Sec12"]["start"], ],
             [np.nanmin(orig_ylim) - 2, np.nanmax(orig_ylim)+2])  # Discussion
    ax1.text(text_dict["Sec12"]["start"], orig_ylim[1], "Discussion", rotation="vertical", ha="left")

    plt.yticks([1,], [residue_shortid],)


    ax1.set_ylim(orig_ylim)

    ax1.set_xlim(-100, len(fulltext_tokens))
    plt.xlabel("Token Number")
    plt.ylabel("Amino Acid")
    pass


def query_epmc(query):
    """

    :param query:
    :return:
    """
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
    page_term = "&pageSize=999"  ## Usual limit is 25
    request_url = url + query + page_term
    r = requests.get(request_url)

    return r


def query_to_dict(query):
    """

    :param query:
    :return:
    """
    r = query_epmc(query)
    soup = BeautifulSoup(r.text, "lxml-xml")

    results_dict = OrderedDict()

    for result in soup.resultList:
        #     print(result.title)
        results_dict[result.id] = {}

        for i in result:
            results_dict[result.id][i.name] = i.text

    return results_dict


def extract_ids_from_query(query):
    """

    :param query:
    :return:
    """

    results_dict = query_to_dict(query)

    ids = [results_dict[i]["pmcid"] for i in results_dict]

    return ids


def get_rawcontext(location_dict, fulltext, x=50, verbose=False):
    """
    """
    for key in location_dict:
        if verbose:
            print(key)
        for i, offset in enumerate(location_dict[key]["offset"]):
            if i == 0:
                location_dict[key]["rawcontext"] = []

            #             rawcontext = "".join(fulltext[offset-x:offset+x])
            rawcontext = [fulltext[offset - x:offset + x], ]

            location_dict[key]["rawcontext"] += rawcontext

            if verbose:
                print(rawcontext)
    return location_dict


def process(ext_id_list, outdir, verbose=False):
    """

    :param outpath:
    :param ext_id_list:
    :return:
    """
    if isinstance(ext_id_list, str):
        ext_id_list = [ext_id_list,]

    # outdict = OrderedDict()
    outdict = {}

    for ext_id in ext_id_list:
        text_dict = get_text(ext_id)
        fulltext = reconstruct_fulltext(text_dict, tokenise=False)

        nlp = spacy.load('en')
        fulldoc = nlp(fulltext)
        fulltext_tokens = [t for t in fulldoc]

        # fulltext_tokens = reconstruct_fulltext(text_dict, tokenise=True)
        unique_residues = identify_residues(fulltext, return_mentions=True)
        location_dict = locate_residues(fulltext_tokens, unique_residues, fulldoc=fulldoc, offset=True)
        if verbose:
            print(location_dict)
        outdict[ext_id] = get_rawcontext(location_dict, fulltext)

    outpath = os.path.join(os.path.abspath(outdir), "output.json")
    print(outdict)

    with open(outpath, 'w') as outfile:
        json.dump(outdict, outfile, cls=MyEncoder)
    pass

if __name__ == "__main__":
    pass
else:
    pass
