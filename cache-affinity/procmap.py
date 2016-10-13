import os, re, time, sys

class Tree: 

# The computer's central processor can be thought of as a 
# tree whose inner nodes are shared cache and whose leaves
# are the cores themselves. For example: 
#
#    [ L3 / Main memory ]
#        /            \  
#    [ L2 ]          [ L2 ]
#    /    \          /    \
#  [L1]   [L1]    [L1]    [L1]
#   |      |       |       |
# cpu0    cpu1    cpu2    cpu3
#
# In this datastructure, leaves have a tuple called 'cpu' 
# with the core number and an associated process id (-1 
# if the core is not running an application through our 
# domain.

  def __init__(self, parent=None):
    self.visited = False
    self.parent = parent
    self.children = {}
    self.cpu = None # leaf
  
  def insert(self, branch): 
    # insert a branch
    if len(branch) == 0:
      return None
    elif len(branch) == 1: 
      self.children[branch[0]] = Tree(self)
      self.children[branch[0]].cpu = (branch[0], -1) # (cpu number, associated pid) 
      return self.children[branch[0]]
    else:
      try:  
        core = self.children[branch[0]].insert(branch[1:])
        return core
      except KeyError: 
        self.children[branch[0]] = Tree(self)
        core = self.children[branch[0]].insert(branch[1:])        
        return core

class ProcMap: 

# Processor core/cache topolgoy. A 'Tree' structure is created from the 
# system's CPU information. We use /sys/devices/system/cpu infomration 
# to build this tree. ProcMap.topology is the actual tree structure 
# and ProcMap.cores is a mapping of core id to leaves. 

  def __init__(self): 
       
    self.polarity = False  
    self.topology = Tree()
    self.cores = {}

    # Get a list of online cores.
    cpu_ids = []
    online = open("/sys/devices/system/cpu/online", "r").readline().strip().split(',')
    for c in online:
      c_list = map(int, c.split('-'))
      if len(c_list) == 2: 
        cpu_ids += range(c_list[0], c_list[1]+1)
      elif len(c_list) == 1:
        cpu_ids.append(c_list[0])
      else:
        print >> sys.stderr, "uh oh!"

    # Discover each online core's branch
    for cpu_id in cpu_ids:
      core_id = int(open("/sys/devices/system/cpu/cpu%d/topology/core_id" % cpu_id).readline().strip())
      physical_id = int(open("/sys/devices/system/cpu/cpu%d/topology/physical_package_id" % cpu_id).readline().strip())
      self.cores[cpu_id] = self.topology.insert([physical_id, core_id, cpu_id])

  def _dfs(self, s, u, dist): 
    
    if u == s or u == None:
      return 
    
    u.visited = not self.polarity

    if u.cpu: # leaf
      (core, pid) = u.cpu
      if pid == -1: 
        print "%d is %d away." % (core, dist)

    else: # inner node
      for v in u.children.values() + [u.parent]: 
        if v and v.visited == self.polarity: 
          self._dfs(s, v, dist + 1)

  def search(self, s):
    s.visited = not self.polarity
    self._dfs(s, s.parent, 0)
    self.polarity = not self.polarity
    
    

pmap = ProcMap() 
pmap.search(pmap.cores[0])
pmap.search(pmap.cores[1])

