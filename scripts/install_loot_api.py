#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import tempfile
import urllib
import _winreg

try:
    sys.path.append('Mopy')
    import loot_api
except ImportError:
    pass

def isMSVCRedistInstalled(majorVersion, minorVersion, buildVersion):
    subKey = 'SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x86'

    try:
        keyHandle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, subKey)

        runtimeInstalled = _winreg.QueryValueEx(keyHandle, 'Installed')[0]
        installedMajorVersion = _winreg.QueryValueEx(keyHandle, 'Major')[0]
        installedMinorVersion = _winreg.QueryValueEx(keyHandle, 'Minor')[0]
        installedBuildVersion = _winreg.QueryValueEx(keyHandle, 'Bld')[0]

        if runtimeInstalled != 0:
            print 'Found MSVC 2015 redistributable version %s.%s.%s' % (installedMajorVersion, installedMinorVersion, installedBuildVersion)

        return (runtimeInstalled != 0
            and installedMajorVersion >= majorVersion
            and installedMinorVersion >= minorVersion
            and installedBuildVersion >= buildVersion)
    except:
        return False

def installMSVCRedist():
    url = 'http://download.microsoft.com/download/9/a/2/9a2a7e36-a8af-46c0-8a78-a5eb111eefe2/vc_redist.x86.exe'
    downloadedFile = os.path.join(tempfile.gettempdir(), 'vc_redist.x86.exe')

    print 'Downloading the MSVC 2015 redistributable...'
    urllib.urlretrieve(url, downloadedFile)

    print 'Installing the MSVC 2015 redistributable...'
    subprocess.call([downloadedFile, '/quiet'])

    os.remove(downloadedFile)

def isLootApiInstalled(revision):
    return ('loot_api' in sys.modules
        and loot_api.WrapperVersion.revision == revision)

def installLootApi(revision, destinationPath):
    url = 'https://bintray.com/wrinklyninja/loot/download_file?file_path=loot_api_python-' + revision + '-win32.7z'
    archivePath = os.path.join(tempfile.gettempdir(), 'archive.7z')
    sevenZipPath = os.path.join('Mopy', 'bash', 'compiled', '7z.exe')

    print 'Downloading LOOT API Python wrapper from "' + url + '"...'
    urllib.urlretrieve(url, archivePath)

    print 'Extracting LOOT API Python wrapper to ' + destinationPath
    subprocess.call([sevenZipPath, 'e', archivePath, '-y', '-o' + destinationPath, '*/loot_api.dll', '*/loot_api.pyd'])

    os.remove(archivePath)

if isMSVCRedistInstalled(14, 0, 24212):
    print 'MSVC 2015 Redistributable is already installed'
else:
    installMSVCRedist()

lootApiWrapperRevision = '1.1.1-0-g1fb6502'
if isLootApiInstalled(lootApiWrapperRevision):
    print 'LOOT API wrapper revision %s is already installed' % lootApiWrapperRevision
else:
    installLootApi(lootApiWrapperRevision, 'Mopy')
