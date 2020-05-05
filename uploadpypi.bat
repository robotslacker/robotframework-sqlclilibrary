del /s/q dist\*
del /s/q build\*
python setup.py sdist
python setup.py bdist_wheel --universal
pip uninstall --yes robotframework-sqlclilibrary
python setup.py install
python -m robot.libdoc .\SQLCliLibrary doc\SQLCliLibrary.html
REM twine upload dist/*