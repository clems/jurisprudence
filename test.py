# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:51:25 2017

@author: cleme
"""

# import jurinet data
import tarfile
tar = tarfile.open("data/jurinet_sans_dila.tar.gz")
print(tar.getmembers())
tar.extractall("data")
tar.close()


tar = tarfile.open("data/pseudonymisation-master-13db1ddfdf9843339c1c5971b8e73fa98fc9f460.tar.gz")
tar.extractall("data")
tar.close()



xml_file = 'data/EXPDP_JURINET_2015.DMP'
from xml.etree import ElementTree as et
e = et.parse(xml_file).getroott()

from xml.dom import minidom
e = minidom.parse(xml_file)        