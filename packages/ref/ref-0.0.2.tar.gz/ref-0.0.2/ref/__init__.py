#!/usr/bin/python
#package: ref
#name: ref
#title: Getting Started 
access = lambda m,k: {dict:lambda : m[k], 
                      list: lambda :m[k]
                          
                          
                    }
path_f = lambda m,keys : access(m,keys[0])[type(m)]() if len(keys) == 1 else path_f(access(m,keys[0])[type(m)](),keys[1:])  
#path_f(noise,[lambda m : m["noiseprofiles"] ])
#Index 
#index = lambda items,k : dict([ (i[k],i) for i in items ])
indexff = lambda items,k,fn0,fn1 : dict([ (fn0(i,k),fn1(i)) for i in items ]) 
indexf = lambda items,k,fn : dict([ (fn(i,k),i) for i in items ])
index = lambda items,k:  indexf(items,k, lambda i,k: i[k])
view = lambda m,keys:  dict([(k,v) for  k,v in m.items() if k in keys])
#indexpath 
#indexpath = <----
path = lambda m,keys :  m[keys[0]]
keys = lambda m,keys : m[keys[0]].keys()
typef = lambda m,keys :  type(path(m,keys))