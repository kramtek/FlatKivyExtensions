
import platform, shutil, os

packageName = 'flat_kivy_extensions'
packagePath = '/Users/kramer/FlatKivyExtensions/%s' % packageName


def copyPackage(packageName, packagePath, tmpPath):
    print 'Copying package :   %s (%s  --> %s' % (packageName, packagePath, tmpPath)
    try:
        shutil.copytree(packagePath, tmpPath, ignore=shutil.ignore_patterns('*.pyc', '*.log'))
    except Exception as e:
        print 'exception: %s' % str(e)


tmpLocation = '/tmp/'
if platform.system() == 'Windows':
    tmpLocation = 'c:\\tmp\\'

sitePackageLocation = '%sexternal-site-packages/%s' % (tmpLocation, packageName)

if os.path.isdir(sitePackageLocation):
    shutil.rmtree(sitePackageLocation)

copyPackage(packageName, packagePath, sitePackageLocation)



