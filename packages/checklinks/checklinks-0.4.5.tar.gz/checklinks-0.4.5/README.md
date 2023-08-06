# check-links


If you are seeing this on GitHub, it is a mirror from Gitlab: https://gitlab.com/alexbenfica/check-links/

# What does it do?

Allows you to check for broken links in all internal pages of a website and more:
- export results to HTML
- export results to comma separated values
- export results to tab separated values
- can be used as library and return values

It is used for some specific tasks:
- find broken urls on pages
- as a desired side effect, load pages and forces caching creation
- created to run in a daily basis reporting broken links of multi site network

# How to use it?

```python3 check_links.py --help```

It is simple and really fast as it reuses http socket connections!

Enjoy it!
