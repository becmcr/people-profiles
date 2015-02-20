import os
import yaml
import staticjinja


# We define constants for the deployment.
cwd = os.getcwd()
searchpath = os.path.join(cwd, "templates")
outputpath = os.path.join(cwd, "site")


# We load the data we want to use in the templates.
people = yaml.load(open('data/people.yaml'))


def loadAcademyData():
    return {'people': people, 'resources': None}


site = staticjinja.make_site(
    searchpath=searchpath,
    outpath=outputpath,
    staticpaths=['static', '../data'],
    contexts=[(r'.*.html', loadAcademyData), ]
)


site.render(use_reloader=True)
