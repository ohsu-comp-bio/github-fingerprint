#!/usr/bin/env python

import os
import logging
import argparse
import jinja2
import github
import subprocess


REPO_TEMPLATE = """
---
title: {{repo.name}}
description: {{repo.description}}
draft: false
topics:
---

## {{repo.name}}
{{repo.description}}

"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token")
    parser.add_argument("-o", "--org")
    parser.add_argument("-b", "--base", default="site")
    parser.add_argument("--theme")
        
    args = parser.parse_args()
    
    if not os.path.exists(args.base):
        subprocess.check_call("hugo new site %s -f yaml" % (args.base), shell=True)
        
    g = github.Github(args.token)
    
    repos = []
    for i in g.get_organization(args.org).get_repos():
        repos.append( { 
            "name" : i.name, 
            "description" : i.description, 
            "page" : i.html_url,
            "fork" : i.fork,
        } )
    
    repo_template = jinja2.Template(REPO_TEMPLATE)
    repo_dir = os.path.join(args.base, "content", "repos")
    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    for r in repos:
        if not r['fork']:
            if r['description'] is not None:
                with open(os.path.join(repo_dir, "%s.md" % (r['name']) ), "w") as handle:
                    txt = repo_template.render(repo=r)
                    handle.write(txt)
