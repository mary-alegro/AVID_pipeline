
from Node import Node
from Tree import Tree


class XMLUtils(object):

    def parse_dict(self,dics,parent=None):
        # dics is always and array with 1 or more dictionaries. There head must always have 1 single dict.

        node = None

        nD = len(dics)
        for d in range(nD):
            dic = dics[d] #get obj from array
            node = Node(dic['name'])

            print(dic['name'])

            if not parent is None:  # add curr node to parents children list
                parent.add_child(node)

            node.set_parent(parent)
            node_dic = {}

            att = dic['attrib'] #another dict
            for key in att.keys():
                if key == 'children':
                    arr_dic = att[key]
                    self.parse_dict(arr_dic,node)
                else:
                    node_dic[key] = att[key] #it's a leave node
                    node.add_data(node_dic)

        return node



    def dict2xml(self,dic):
        if type(dic) != list:
            dic = [dic]
        head = self.parse_dict(dic)
        tree = Tree(head)
        return tree.export_xml_string()


    def dict2xmlfile(self,dic,xml_file):
        if type(dic) != list:
            dic = [dic]
        head = self.parse_dict(dic)
        tree = Tree(head)
        with open(xml_file, 'w+') as out:
            out.write(tree.export_xml_string())



def main():

    e = dict()
    e['name'] = 'e'
    e['attrib'] = {}

    f = dict()
    f['name'] = 'f'
    f['attrib'] = {'etc':'f'}

    c = dict()
    c['name'] = 'c'
    c['attrib'] = {'children':[e,f], 'att':'123', 'att2':'123'}

    d = dict()
    d['name'] = 'd'
    d['attrib'] = {}

    b = dict()
    b['name'] = 'b'
    b['attrib'] = {'children':[c,d]}

    a = dict()
    a['name'] = 'a'
    a['attrib'] = {'children':[b]}

    dics = [a]

    xmlUtils = XMLUtils()
    str_xml = xmlUtils.dict2xml(dics)
    print(str_xml)



if __name__ == '__main__':
    main()