config = {'template_file': 'number.jinja2',
          'kind': ['header', 'figure', 'table'],
          'tag_file': '.pheasant-number.json',
          'tag_pattern': r'\{#(\S+)#\}',
          'class': 'pheasant-{kind}',
          'id': 'pheasant-{tag}',
          'relpath_function': None,
          'level': 2  # numbering level. 0 for multiple pages, 2 for h2 etc.
          }
