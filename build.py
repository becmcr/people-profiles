from os import getcwd, path
from yaml import load
from slugify import slugify
from collections import defaultdict
import staticjinja


# We define constants for the deployment.
cwd = getcwd()
searchpath = path.join(cwd, "templates")


def slugy(x):
    return str(slugify(unicode(x)))


def loadAcademyData():
    ctx = {'people': [], 'resources': None, 'filters': defaultdict(set)}
    lists = ['impact_areas', 'expertise', 'geographic_interest']

    for person in load(open('data/people.yaml')):
        dic = {'filters': set()}

        for key in person.keys():
            key = key.lower()
            val = person[key] or '&nbsp;'

            if key.lower() == 'year':
                dic[key] = str(val)

                dic['filters'].add(str(val))
                ctx['filters']['year'].add(str(val))

            elif key == 'affiliation':
                dic[key] = val

                dic['filters'].add(slugy(val))
                ctx['filters']['affiliation'].add(val)

            elif key in lists:
                lst = []

                if isinstance(val, list):
                    lst = val

                else:
                    lst = [val]

                dic[key] = lst

                dic['filters'].update([slugy(x) for x in lst])
                ctx['filters'][key].update(lst)

            else:
                dic[key] = val

        dic['filters'] = ' '.join(dic['filters'])

        ctx['people'].append(dic)

    for key in ctx['filters'].keys():
        ctx['filters'][key] = sorted(list(ctx['filters'][key]))

    return ctx


site = staticjinja.make_site(
    searchpath=searchpath,
    filters={'slugy': lambda x: slugy(x)},
    staticpaths=['static', '../data'],
    contexts=[(r'.*.html', loadAcademyData)]
)


site.render(use_reloader=True)
