#DIST:distutils,setup.py 

#!/usr/bin/env python

#modules = map(__import__, moduleNames)



from distutils.core import setup

import json;



settings = json.loads(open("config.json").read()) 




package_name = str(settings["package"])

setup(

    name=package_name,

    version="0.0.2.2",

    author="thinkersilver",

    author_email="myonlineprofile2012@gmail.com",

    packages=[package_name],

    scripts=['bin/%s' % package_name],

    package_data={'':["./config.json"]},

    description="References library"

) 
