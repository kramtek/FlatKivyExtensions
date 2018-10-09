
import platform, shutil, os, zipfile, fnmatch, sys

packageLabel = 'SswClient'
packageLabel = 'Services'
packageLabel = 'LauncherUtils'

packageLabels = ['FlatKivyExtensions']
#if len(sys.argv) > 1:
#    if (sys.argv[1] != '1'):
#        packageLabel = sys.argv[1].replace('/','')
#        print 'packageLabel: "%s"' % packageLabel
#        packageLabels = [packageLabel]

os.chdir('../')

tmpLocation = '/tmp/'
if platform.system() == 'Windows':
    tmpLocation = 'c:\\tmp\\'
sitePackagePath = '%s/external-site-packages' % tmpLocation


def getVersion(packagePath):
    f = open('%s/__init__.py' % packagePath)
    lines = f.readlines()
    f.close()
    for line in lines:
        if line.find('__version__') >= 0:
            version = line.replace('__version__', '').replace('=', '').strip().replace("'", '').replace('"', '')
            return version

def getPackageName(packageLabel):
    f = open('%s/setup.py' % packageLabel)
    lines = f.readlines()
    f.close()
    for line in lines:
        if line.find('import')>=0 and line.find('__version__')>=0:
            packageName = line.replace('from', '').replace('import', '').replace('__version__', '').strip()
            return packageName.strip()

def copytree(packagePath, tmpPath):
    print '  * Copying directory:  %s  --> %s' % (packagePath, tmpPath)
    try:
        shutil.copytree(packagePath, tmpPath, ignore=shutil.ignore_patterns('*.pyc', '*.log'))
    except Exception as e:
        print 'exception: %s' % str(e)

def clean(path):
    current = os.getcwd()
    os.chdir(path)
    print '  * Cleaning files from %s' % path
    matches = []
    removeList = ["1", "hey", "*.pyc", "*.log", "*.DS_Store", ".gitignore", "*.mp_*"]
    for root, dirnames, filenames in os.walk('.'):
        for removeItem in removeList:
            for filename in fnmatch.filter(filenames, removeItem):
                matches.append(os.path.join(root, filename))

    for filename in matches:
        os.remove( filename )

    directoryRemoveList = ['.git', '.kivy', '.idea']
    for directory in directoryRemoveList:
        try:
            shutil.rmtree(directory)
        except Exception as e:
            if str(e).find('No such file') == -1:
                print 'Exception removing %s: %s' % (directory, str(e))
                print str(e)
    os.chdir(current)


def zipDir(path, dst):
    print '  * Zipping contents of: %s --> %s' % (path, dst)
    zipf = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for filename in files:
            # print '  adding: %s to zip' % filename
            zipf.write(os.path.join(root, filename))
    zipf.close()

def copypackage(path, fullName, sitePackageLocation):
    archivedPackageLocation = '%s/%s' % (tmpLocation, fullName)
    if os.path.isdir(sitePackageLocation):
        shutil.rmtree(sitePackageLocation)
    if os.path.isdir(archivedPackageLocation):
        shutil.rmtree(archivedPackageLocation)

    copytree(path, sitePackageLocation)


def archivePackage(tmpLocation, sitePackagePath, label, onlyToSitePackages=False):

    current = os.getcwd()

    packageName = getPackageName(label)

    packagePath = '%s/%s' % (label, packageName)
    version = getVersion(packagePath)
    fullPackageName = '%s_%s' % (label, version)
    sitePackageLocation = '%s/%s'% (sitePackagePath, packageName)

    print '-- "Installing" package %s into external site-packages...' % str(packageName)
    copypackage(packagePath, fullPackageName, sitePackageLocation)

    if onlyToSitePackages:
        return

    archivedPackageLocation = '%s/%s' % (tmpLocation, fullPackageName)
    print '-- Archive package to: %s' % str(archivedPackageLocation)
    copytree(packagePath, '%s/%s' % (archivedPackageLocation, packageName))
    shutil.copyfile('%s/setup.py' % label, '%s/setup.py' % archivedPackageLocation)

    print '  * Generating html documentation...'
    os.chdir(label)
    cmd = 'scripts/build_docs.sh %s %s' % (packageName, version)
    os.system(cmd)

    copytree('doc', '%s/doc' % (archivedPackageLocation))

    cmd = 'rm -rf doc'
    os.system(cmd)

    os.chdir('../')

    os.chdir(tmpLocation)
    clean(fullPackageName)

    zipDir(fullPackageName, '%s.zip' % fullPackageName)

    os.chdir(current)


onlyToSitePackages = (len(sys.argv) >= 2)

for packageLabel in packageLabels:
    archivePackage(tmpLocation, sitePackagePath, packageLabel, onlyToSitePackages)


