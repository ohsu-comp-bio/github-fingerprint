import logging
import sys
import github
import jinja2

# Get this from your personal account settings page (not the organization settings)
# Settings > Personal access tokens > Generate new token
TOKEN = ''
ORG = 'ohsu-comp-bio'

class Row:
    name = ''
    description = ''
    contributors = ''
    langauges = ''
    url = ''

class Contrib:
    def __init__(self, author, total_commits=0):
        self.author = author
        self.total = total_commits


def get_language_percentages(repo):
    langs = repo.get_languages()
    lang_byte_sum = sum(langs.values())
    langs_percentage = {}
    for l, s in langs.items():
        langs_percentage[l] = s / lang_byte_sum
    return sorted(langs_percentage.items(), key=lambda r: r[1])


def format_language_percentages(lang_percents):
    return '\n'.join('{0}: {1:.2f}'.format(l, s) for l, s in lang_percents)


def get_contributors(repo):
    contribs = []
    c = repo.get_stats_contributors()
    if c is not None:
        for i in c:
            contribs.append(Contrib(i.author, i.total))
    else:
        c = repo.get_contributors()
        for i in c:
            contribs.append(Contrib(i))
    return contribs

def format_contributor(c):
    u = c.author
    return '{} : {} : {} total commits'.format(
        u.name,
        u.login,
        c.total
    )


def format_contributors(contribs):
    return '\n'.join(format_contributor(c) for c in contribs)


def format_row(r):
    return '\n'.join(str(i) for i in [
        r.name,
        r.description,
        r.contributors,
        r.languages,
        r.url,
    ])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if not TOKEN:
        logging.error("No API TOKEN set. Edit main.py")
        sys.exit(1)

    g = github.Github("35de2a11d970f9025495d53ecc1d89928d933a09")
    tpl = jinja2.Template(open('template.html').read())
    rows = []

    repos = g.get_organization(ORG).get_repos()
    for repo in repos[:3]:
        r = Row()
        rows.append(r)
        r.name = repo.name
        r.description = repo.description
        r.url = repo.html_url

        c = get_contributors(repo)
        r.contributors = format_contributors(c)

        lp = get_language_percentages(repo)
        r.languages = format_language_percentages(lp)

        try:
            x = repo.get_file_contents(".travis.yml")
            print("Has TravisCI", x)
        except github.UnknownObjectException:
            pass

        rs = format_row(r)
        logging.info("Pulled " + r.name)

    print(tpl.render(rows=rows))
