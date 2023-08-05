import re


def get_renderables(path,tpt,datum):
    for v in Fabric.__SUBSTITIONS__.findall(tpt):
        if v not in datum:
            continue
        yield v

def get_dispatchers(path,tpt,selectors):
    for v in Fabric.__SUBSTITIONS__.findall(tpt):
        new_path  =  "%s/%s" % (path,v)
        if new_path not in selectors:
            continue
        yield v


class Fabric():
    __SUBSTITIONS__ = re.compile("#(\w+)")
    def __init__(self):
        self.__templates__ = {}
        self.__selectors__ = {}

        pass

    def add_weave(self, path, tpt, fn_data_selector=None ):
        self.__templates__[path] = tpt
        self.__selectors__[path] = fn_data_selector
        pass

    @staticmethod
    def process(path,tpts,selectors):

        template = tpts[path]
        data = selectors[path]
        rendered = []
        for datum in  data():
            t = template

            renderables =  [ r for r in get_renderables(path,template,datum)]
            for r in renderables:
                t= t.replace("#%s" % r , datum[r])

            dispatchables = [ d for d in get_dispatchers(path,template,selectors)]
            for d in dispatchables:
                t = t.replace("#%s" % d ,Fabric.process("%s/%s" % (path,d),tpts,selectors))


            rendered.append(t)
        return " ".join(rendered)

    def render1(self):
        return Fabric.process("$/root",self.__templates__,self.__selectors__)

    @staticmethod 
    def find_indent(tpt,k):
        indents = [ t.find("%s" % k ) for t in tpt.split("\n") if t.find("%s" % k ) > -1 ]
        if len(indents) > 0:
            return indents[0] 
        return 0 

    def render(self,path,data=None,trace=False):
        if trace:
            print (path,data)
        tpt = self.__templates__[path] 

        if data is None:
            data = self.__selectors__[path]() 
        for k in data.keys():
            v = data[k] 
            if type(v) == list:
                outputs = [] 
                tab_count = Fabric.find_indent(tpt,"%s" % k ) 
                for el in enumerate(v): 
                    #outputs.append(None)
                    if el[0] > 0:
                        outputs.append("%s%s" % (tab_count*" ", self.render("%s/%s" % (path,k),el[1])))

                    if el[0] == 0:
                        outputs.append("%s" % ( self.render("%s/%s" % (path,k),el[1])))
     
                tpt = tpt.replace("#%s" % k , " ".join(outputs))  

            if type(v) != list:
                tpt = tpt.replace("#%s" % k, str(v) )  
        return tpt 


if __name__ == "__main__":
    
    f = Fabric()
    f.add_weave("$/root","""
        digraph #name {
            #label
            #edges
            #more
        }


    """,lambda : {"name":"graph_eins","edges":[{"a":1,"b":2},{"a":10,"b":20}], "more":[{"a":0},{"a":3}]})

    f.add_weave("$/root/edges","#a->#b;") 
    f.add_weave("$/root/more","#a;") 
    print f.render("$/root")
