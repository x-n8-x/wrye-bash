#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quickly generate some files for sphinx to process source code of a project.

"""

from collections import OrderedDict
from os.path import join, dirname, abspath, isfile, basename, exists
from os import sep, listdir

# :seealso: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
# Most of the autodoc options can be set up in the conf.py `autodoc_default_flags` variable
   # :members:
   # :undoc-members:
   # :private-members:
   # :special-members:
   # :show-inheritance:

# Some other options
   # :deprecated:
   # :platform:
   # :synopsis:
template = """\
.. include:: headings.inc

{headerline}
|module_summary| {filenamenoext}
{headerline}

.. automodule:: {dotdir}.{filenamenoext}
   :member-order:
   :exclude-members: __module__, __dict__, __weakref__, staticMetaObject

"""

toctree_template = """
.. toctree::
   :maxdepth: 20
"""

if __name__ == '__main__':
    import os
    # Ensure the cwd is right, so we don't churn out the files somewhere else.
    gFileDir = abspath(dirname(__file__))
    os.chdir(gFileDir)
    gMopyDir = abspath(abspath(dirname(dirname(dirname(dirname(__file__))))) + sep + 'Mopy')
    print('gMopyDir = %s' % gMopyDir)
    assert exists(gMopyDir)  # Sanity Check.
    assert basename(gMopyDir) == 'Mopy'  # Sanity Check.

    WryeBashPythonSourceDirs = OrderedDict([
        # dotdir, dirpath
        ('bash'                          , join(gMopyDir, 'bash')),
        ('bash.basher'                   , join(gMopyDir, 'bash', 'basher')),
        ('bash.bosh'                     , join(gMopyDir, 'bash', 'bosh')),
        ('bash.chardet'                  , join(gMopyDir, 'bash', 'chardet')),
        ## ('bash.compiled'                 , join(gMopyDir, 'bash', 'compiled')),
        ## ('bash.db'                       , join(gMopyDir, 'bash', 'db')),
        ('bash.game'                     , join(gMopyDir, 'bash', 'game')),
        ('bash.game.fallout4'            , join(gMopyDir, 'bash', 'game', 'fallout4')),
        ('bash.game.fallout4.patcher'    , join(gMopyDir, 'bash', 'game', 'fallout4', 'patcher')),
        ('bash.game.oblivion'            , join(gMopyDir, 'bash', 'game', 'oblivion')),
        ('bash.game.oblivion.patcher'    , join(gMopyDir, 'bash', 'game', 'oblivion', 'patcher')),
        ('bash.game.skyrim'              , join(gMopyDir, 'bash', 'game', 'skyrim')),
        ('bash.game.skyrim.patcher'      , join(gMopyDir, 'bash', 'game', 'skyrim', 'patcher')),
        ## ('bash.images'                   , join(gMopyDir, 'bash', 'images')),
        ## ('bash.l10n'                     , join(gMopyDir, 'bash', 'l10n')),
        ('bash.patcher'                  , join(gMopyDir, 'bash', 'patcher')),
        ('bash.patcher.patchers'         , join(gMopyDir, 'bash', 'patcher', 'patchers')),
        ])


    def generateToCTree():
        toctree = toctree_template
        for dotDir, dirPath in list(WryeBashPythonSourceDirs.items()):
            for item in listdir(dirPath):
                theitempath = dirPath + sep + item
                if isfile(theitempath) and item.endswith('.py') and not item == '__init__.py':
                    filenameNoExt = item[:-3]
                    toctree += '\n   %s.%s' % (dotDir, filenameNoExt)
        return toctree

    def generateSphinxFiles():
        for dotDir, dirPath in list(WryeBashPythonSourceDirs.items()):
            for item in listdir(dirPath):
                theitempath = dirPath + sep + item
                if isfile(theitempath) and item.endswith('.py') and not item == '__init__.py':
                    filenameNoExt = item[:-3]
                    headerLine = '=' * len('|module_summary| ' + filenameNoExt)
                    with open(gFileDir + sep + '%s.%s.rst' % (dotDir, filenameNoExt), 'w') as f:
                        f.write(template.format(headerline=headerLine,
                                                filenamenoext=filenameNoExt,
                                                dotdir=dotDir))

    # Uncomment to make the rst/txt files.
    ## generateSphinxFiles()
    ## print(generateToCTree())
    print('DONE')

