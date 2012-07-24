# HMA has a unique method of presenting IP addresses
# This processors applies a method to extract HMA IP addresses

from scrapy import log
import re


class GetIPAddresses(object):
    '''Parse HTML and extract IP addresses    '''
    def __init__(self):
        self.re_IP = re.compile(r'\d+\.\d+\.\d+\.\d+|\d+\.\d+\.\d+|\d+\.\d+|\d+(?=<)|\.\d+|\d+\.|\d+$|\.')

    def __call__(self, Xpaths):
        self.IPs = []
        nodeList = self.removeDisNone(Xpaths)
        nodeList, toToss = self.keepNone(nodeList)
        nodeList = self.removeStyNone(nodeList, toToss)
        return self.getIPs(nodeList)

    # remove the 'display:none' from the nodeList
    def removeDisNone(self, Xpaths):
        nodeList, disNone = Xpaths
        for i, nono in enumerate(disNone):
            for j in nono:
                if j in nodeList[i]:
                    nodeList[i].remove(j)
        return nodeList

    # parse node[0] <style> and keep the 'none' types
    def keepNone(self, nodeList):
        toToss = [[] for _ in range(len(nodeList))]
        for i, node in enumerate(nodeList):
            reg = re.findall(r'\.(.+){display:(\w+)', str(node[0]))
            for j, k in reg:
                if k == 'none':
                    toToss[i].append(j)
        return nodeList, toToss

    # cycle through both nodes and classes to remove the <style>'display:none' node
    def removeStyNone(self, nodeList, toToss):
        torm = [[] for _ in range(len(nodeList))]
        for i, pnode in enumerate(nodeList):
            for cnode in pnode:
                for toss in toToss:
                    for k in toss:
                        if 'class="%s"' % k in str(cnode):
                            torm[i].append(cnode)

        for i, rm in enumerate(torm):
            for j in rm:
                nodeList[i].remove(j)

        return nodeList

    # remove the <style> tag and join the IPs
    def getIPs(self, nodeList):
        for node in nodeList:
            node.remove(node[0])
            joinIP = ''.join(node)
            self.IPs.append(''.join(self.re_IP.findall(joinIP)))
            # log.msg("IPs: %s" % self.IPs, level=log.DEBUG)
        return self.IPs
