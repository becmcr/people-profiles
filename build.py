from os import getcwd, path
from csv import reader
from yaml import load
from slugify import slugify
from collections import defaultdict
import staticjinja


_MAP = {
    'Entry Id': 'entry_id',
    'Name': 'name',
    'Last': 'last',
    'Profile Header Sentence': 'profile',
    'Bio': 'bio',
    'Educational Experience': 'experience',
    'Affiliation': 'affiliation',
    'Year': 'year',
    'Current Role and Organization/Employer': 'role',
    'City': 'city',
    'State / Province': 'state',
    'Country': 'country',
    'Email': 'email',
    'Facebook': 'facebook',
    'LinkedIn': 'linkedin',
    'Twitter': 'twitter',
    'Instagram': 'instagram',
    'Personal / Venture Website': 'website',
    'Date Created': 'created',
    'N-AK-data': 'impact_areas',
    'AL-BT-data': 'expertise',
    'BU-CE-data': 'geographic_interest'
}


# We define constants for the deployment.
cwd = getcwd()
searchpath = path.join(cwd, "templates")


def slugy(x):
    return slugify(x.decode('utf-8')).encode('ascii')


def loadAcademyData():
    ctx = {'people': [], 'resources': None, 'filters': defaultdict(set)}
    lists = ['impact_areas', 'expertise', 'geographic_interest']

    for person in load(open('data/people.yaml')):
        img_url = lambda x, y: slugy(x + '-' + y).title() + '.jpg'
        dic = {'filters': set()}

        if str(person['Entry Id']).strip():
            for k in [x for x in person.keys() if x in _MAP]:
                val = person[k] or ''
                key = _MAP[k]

                if isinstance(val, str):
                    val = '' if val == '@' else val.strip()

                if key == 'year':
                    dic[key] = str(val)

                    dic['filters'].add(str(val))
                    ctx['filters']['year'].add(str(val))

                elif key == 'affiliation':
                    dic[key] = val

                    dic['filters'].add(slugy(val))
                    ctx['filters']['affiliation'].add(val)

                elif key in lists:
                    lst = []

                    for split in reader([val]):
                        lst.extend([x.strip() for x in split if x.strip()])

                    dic[key] = lst

                    dic['filters'].update([slugy(x) for x in lst])
                    ctx['filters'][key].update(lst)

                else:
                    dic[key] = val

            dic['image'] = img_url(dic['name'], dic['last'])
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
