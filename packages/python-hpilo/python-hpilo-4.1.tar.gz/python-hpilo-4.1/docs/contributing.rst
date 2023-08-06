Contributing guide
==================

python-hpilo is maintained by Dennis Kaarsemaker on GitHub_. If you have a
problem with the software, that's the place to file an issue. And if you want
to contribute to the project, that's the place to go to as well.

Patches can be submitted as pull requests on github or mailed to
dennis@kaarsemaker.net.

If you are looking for a really simple way of contributing, please contribute
test data from a server model that's not included in the tests yet, see
`tests/README` for more details.

Coding guidelines
-----------------
* python-hpilo currently supports python 2.6, 2.7 and 3.5 or newer. Any new
  code in `hpilo.py` and `hpilo_cli` needs to be compatible with all these
  versions.
* No non-stdlib dependencies in `hpilo.py` and `hpilo_cli`. Examples may have
  additional dependencies.
* All methods call into :func:`_info_tag` or :func:`_control_tag`. Any
  new method must do so too, to be able to use it in :meth:`call_delayed`.
* All new methods must be documented. A docstring is mandatory and will appear
  in the docs. For methods that return data, sample output must be added to the
  documentation too.
* All new methods must be tested. You should add data for the xml
  parser/generator tests and, if applicable, a test that manipulates the iLO.
  See the `tests/README` file in the git repository for more details on tests.

.. _GitHub: https://github.com/seveas/python-hpilo
