## Changelog

### 2.0.3 - 2018-01-19

*   [resultsdb_conventions-2.0.3.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-2.0.3.tar.gz)

1.  Catch `FedfindError` as well as `ValueError` from fedfind `get_release`

### 2.0.2 - 2017-02-24

*   [resultsdb_conventions-2.0.2.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-2.0.2.tar.gz)

1.  Add `FedoraBodhiResult` convention for Fedora Bodhi update results

### 2.0.1 - 2017-02-15

*   [resultsdb_conventions-2.0.1.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-2.0.1.tar.gz)

1.  Update README and release script
2.  Require `productmd` in `setup.py`
3.  Add copy of license

### 2.0.0 - 2017-02-07

*   [resultsdb_conventions-2.0.0.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-2.0.0.tar.gz)

1.  **API**: Don't unnecessarily explicitly take parent class args in child classes
2.  **API**: Introduce generic productmd image class, make compose class a productmd class
3.  **API**: Split into a multiple module library for independence and scalability
4.  **API**: Require metadata instead of using fragile compose ID parsing in productmd classes
5.  **NEW**: Add `meta.conventions` extradata item indicating conventions result complies with
6.  Require setuptools_git in the setup script and use sdist again
7.  Make fedfind dependency optional

### 1.0.1 - 2017-02-02

*   [resultsdb_conventions-1.0.1.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-1.0.1.tar.gz)

1.  Pass through what the API result submission function returns

### 1.0.0 - 2017-02-02

*   [resultsdb_conventions-1.0.0.tar.gz](https://files.pythonhosted.org/packages/source/r/resultsdb-conventions/resultsdb_conventions-1.0.0.tar.gz)

1.  Initial release of resultsdb_conventions
