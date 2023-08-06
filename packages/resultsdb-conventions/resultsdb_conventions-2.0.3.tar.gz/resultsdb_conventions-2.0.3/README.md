# resultsdb_conventions

resultsdb_conventions is a Python library that represents various conventions for reporting test results to [ResultsDB][1]. It allows you to report results easily and without a lot of boilerplate, and be relatively confident their ResultsDB metadata will be consistent with other results of the same basic nature.

## Installation

resultsdb_conventions packages are available in the Fedora and [EPEL][2] 7 repositories. The core package is `python2-resultsdb_conventions`, and the `fedora` module is in the package `python2-resultsdb_conventions-fedora`. For other distributions, or if you want to use the git code, you can simply make the library available in the Python path for your consumer in some way, or to install the library systemwide, just run `sudo python setup.py install`. You will need the `cached-property` library as well, and the `fedfind` library if you wish to use the Fedora conventions (these are both packaged for Fedora and EPEL). For actually submitting results, you will need the `ResultsDBapi` class from the `resultsdb_api` module.

resultsdb_conventions is intended to be compatible with Python 2.6+ and current Python 3. Please report bugs if you find compatibility problems.

## Use

The simplest way to use resultsdb_conventions is to pick the `Result` subclass that most closely represents the kind of result you wish to submit, instantiate it with appropriate arguments, get an instance of `ResultsDBapi`, and run the `report()` method. This will apply the 'default' metadata for the result (based on the kind of result and the args used for instantiation), and submit it to whichever ResultsDB you got an API instance for. The `Result` subclasses should all document their required and optional arguments.

For simple modifications of the submitted result, you can simply adjust the `extradata` property (which is just a dict of arbitrary string key:value pairs that are passed to ResultsDB and stored as-is) after getting the instance but before running `report()`. You can also cause the result to be added to more groups by including an iterable of group dicts or UUID strings as the `groups` arg when instantiating the result class, or by adjusting the instance's `groups` property directly.

For more complex changes to the behaviour, you can of course start from the most relevant class and create a subclass, then adjust things as appropriate. The important conventions for how subclasses should be implemented are documented in the `Result` class. If your subclass is likely to have utility outside your project, you may want to submit a pull request for it, so other projects can conveniently report results according to the same conventions.

A simple validation mechanism has been included, but currently none of the included classes implements any significant validation. The validation is intended to enforce the convention being encoded, not to do fundamental checks on the validity of the result in ResultsDB terms; ResultsDB will reject any outright invalid submission. Please consider implementing validation for any pull requests you submit.

## Bugs, pull requests etc.

You can file issues and pull requests on the [resultsdb_conventions project][3] in Pagure.

## Credits

Jan Sedlak and Josef Skladanka contributed valuable inspiration, ideas and reviews.

## Licensing

resultsdb_conventions is available under the GPL, version 3 or any later version. A copy is included as COPYING.

[1]: https://fedoraproject.org/wiki/ResultsDB
[2]: https://fedoraproject.org/wiki/EPEL
[3]: https://pagure.io/taskotron/resultsdb_conventions
