#DIST:distutils,setup.py 

#!/usr/bin/env python

#modules = map(__import__, moduleNames)



from distutils.core import setup

import json;



settings = json.loads(open("config.json").read()) 



print settings 

package_name = str(settings["package"])

setup(

    name=package_name,

    version="0.0.1",

    author="thinkersilver",

    author_email="thinkersilver@replacewithgooglesemail.com",

    packages=[package_name],

    scripts=['bin/%s' % package_name],

    description="References library"

) 
