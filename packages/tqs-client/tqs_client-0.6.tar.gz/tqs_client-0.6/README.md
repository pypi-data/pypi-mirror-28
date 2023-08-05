# Tiny Queue Service Client (Python)

*Stefan Arentz, January 2018*

[![Build Status](https://travis-ci.org/st3fan/tqs-client.svg?branch=master)](https://travis-ci.org/st3fan/tqs-client) [![codecov](https://codecov.io/gh/st3fan/tqs-client/branch/master/graph/badge.svg)](https://codecov.io/gh/st3fan/tqs-client) [![Lintly](https://lintly.com/gh/st3fan/tqs-client/badge.svg)](https://lintly.com/gh/st3fan/tqs-client/)

TODO LOTS TO DO

Notes on building and pushing a Python package:

```
git add Pipfile.lock setup.cfg setup.py
git commit
git tag 0.4 -m "0.4"
git push --tags
python setup.py sdist bdist_wheel
twine upload --repository pypi dist/tqs_client-0.4*
```

