#!/usr/bin/env python
# coding: utf-8

# In[142]:


# Read Data
def read_data():
    f = open("data/validationDataset.txt", "r")
    fData = f.readlines()
    lData = []

    for sIter in fData:
        if (sIter[-1] == "\n"):
            sIter = sIter[:-1]
        if (sIter == ""):
            continue
        lData.append(sIter.split(","))
    return lData


# In[143]:


# Create HashMaps
def create_dictionary(lData):
    lDicts = [dict() for x in range(len(lData[0]))] # array/list of dictionaries (Hashmaps)
    for i in range(0, len(lData[0])):
        dFeatures = {} # Empty hashmaps
        for j in range(0, len(lData)):
            if lData[j][i] in dFeatures.keys():
                dFeatures[lData[j][i]] = dFeatures[lData[j][i]] + 1
            else:
                dFeatures[lData[j][i]] = 1
        lDicts[i] = dFeatures
    return lDicts


# In[155]:


def star_reduction(lData, lDicts, nIcebergCondn):
    lData1 = deepcopy(lData)
    for i in range(0, len(lData[0])):
        dInterest = lDicts[i]
        for j in range(0, len(lData)):
            if (dInterest[lData[j][i]] < nIcebergCondn):
                lData1[j][i] = '*';
    return lData1
print(lData1)


# In[156]:


def tuple_convert(lData2):
    for i in range(0, len(lData2)):
        lData2[i] = tuple(lData2[i])
    return lData2


# In[157]:


def generate_compressed_table(lData2):
    dFeatures = {}
    for i in range(0, len(lData2)):
        if lData2[i] in dFeatures.keys():
            dFeatures[lData2[i]] = dFeatures[lData2[i]] + 1
        else:
            dFeatures[lData2[i]] = 1
    return dFeatures


# In[158]:


def lexographical_Sort_keys(lKeys):
    lKeys = sorted(dFeatures.keys())
    return lKeys


# In[159]:


#Tree class
class Tree(object):
    def __init__(node, label = "root", children = None, count = 0):
        node.name = label
        node.children = []
        node.count = count
        node.sibling = []
        if (children != None):
            for i in (0, len(children)):
                node.add_node(children[i])
    
    def add_node(node, child):
        node.children.append(child)
    
    def find(node, label = str("")):
        for i in range(0, len(node.children)):
            if (node.children[i].name == label):
                return node.children[i]
        return None
    
    def update_count(node, count = 0):
        node.count += count
    
    def add_sibling(node, sibling):
        print(node.name)
        node.sibling.append(sibling)


# In[160]:


def create_star_tree(lKeys):
    star_tree = Tree()
    for i in range (0, len(lKeys)):
        head = star_tree
        add_children_to_tree(head, lKeys[i], 0)
    return star_tree


# In[161]:


def add_children_to_tree(head, tChars, nIndex):
    tNew = head.find(tChars[nIndex])
    if (tNew != None):
        tNew.update_count(count = dFeatures[tChars])
    else:
        tNew = Tree(label = tChars[nIndex], count = dFeatures[tChars])
        head.add_node(tNew)
        if (len(head.children) > 1):
            head.children[len(head.children) - 2].add_sibling(tNew)
    nIndex += 1
    if (nIndex < len(tChars)):
        add_children_to_tree(tNew, tChars, nIndex)

# In[163]:


def fPrintTree(tree):
    nIndex = 0
    if (len(tree.children) != 0):
        for child in tree.children:
            fPrintTree(tree.children[nIndex])
            nIndex+=1
    print(tree.name, tree.count)


# In[164]:


def starcubing(star_tree, cNode, nLevel, lCuboidValList):
    Cc = None
    if (cNode.count >= nIcebergCondn):
        if ((cNode.name != "root") or (len(cNode.children) == 0)):
            lCuboidValList[nLevel] = cNode.count
            print(lCuboidValList)
        else:
            Cc = Tree(name = "root", count = cNode.count, children = cNode.children)
    
    if (len(cNode.children) != 0):
            starcubing(star_tree, cNode.children[0], nLevel + 1, lCuboidValList)
    if (Cc != None):
            starcubing(Cc, Cc, nLevel, lCuboidValList)
    if (len(cNode.sibling) > 0):
            cNode.sibling[0].count += cNode.count
            starcubing(star_tree, cNode.sibling[0], nLevel,  lCuboidValList)
    lCuboidValList[nLevel] = "*"


# In[167]:

from copy import deepcopy
def main():
    nIcebergCondn = 2
    lData = read_data()
    lDicts = create_dictionary(lData)
    lData1 = star_reduction(lData, lDicts, nIcebergCondn)
    star_tree = create_star_tree(lKeys)
    lCuboidValList = ["*"] * (len(lData[0]) + 1)
    starcubing(star_tree, star_tree, 0, lCuboidValList)


if __name__ == "__main__":
    main()

