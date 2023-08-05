# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:55:42 2018

@author: root
"""

class  Person( object ):
    def  __init__( self ,name,age):
        self .name =  name
        self .age =  age
    def  __repr__( self ):
        return  'Person Object name : %s , age : %d'  %  ( self .name, self .age)
if  __name__   ==  '__main__' :
    p =  Person( 'Peter' , 22 )
    print  (p)