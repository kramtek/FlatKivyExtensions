
import os, string, shutil, subprocess, glob, fnmatch, zipfile, platform, datetime

from subprocess import call

projectName = 'FlatKivyExtensions'
projectDir = '/Users/kramer/'

def copyApp():
    # Copy over this application
    src = '/Users/kramer/%s' % projectName
    src = '%s%s' % (projectDir, projectName)
    dst = '/tmp/%s' % projectName
    print 'Copying app: %s  --> %s' % (src, dst)
    shutil.copytree(src, dst)

def clean():
    print 'cleaning...'
    matches = []
    removeList = ["1", "hey", "*.pyc", "*.log", "*.DS_Store", ".gitignore", ]
    for root, dirnames, filenames in os.walk('.'):
        for removeItem in removeList:
            for filename in fnmatch.filter(filenames, removeItem):
                matches.append(os.path.join(root, filename))

    # print '  removing: %s' % matches
    for filename in matches:
        os.remove( filename )

    directoryRemoveList = ['.git', '.kivy', '.idea', 'flat_kivy_extensions']
    for directory in directoryRemoveList:
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print 'Exception removing %s: %s' % (directory, str(e))

def zipDir(path, dst):
    print 'Zipping contents of: %s --> %s' % (path, dst)
    zipf = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for filename in files:
            # print '  adding: %s to zip' % filename
            zipf.write(os.path.join(root, filename))
    zipf.close()


tmpLocation = '/tmp/'
if platform.system() == 'Windows':
    tmpLocation = 'c:\\tmp\\'
print 'tmp location: %s' % tmpLocation
projectPath = os.getcwd()
if platform.system() == 'Windows':
    archiveRoot = '%s\\%s' % (tmpLocation, projectName)
else:
    archiveRoot = '%s/%s' % (tmpLocation, projectName)

print 'archiveRoot: %s' % str(archiveRoot)

if os.path.isdir(archiveRoot):
    print 'clearing out old archive'
    shutil.rmtree(archiveRoot)

copyApp()

current = os.getcwd()
os.chdir(archiveRoot)

clean()

os.chdir(tmpLocation)

# tag = 'huh'
# outFile = '%s%s_%s.zip' % (tmpLocation, projectName, tag)
# inDir = '%s' % projectName
# zipDir(inDir, outFile)
#

today = datetime.datetime.now().strftime('%Y.%m.%d')
variant = 'flat_kivy_extensions_demo'
tag = ''
dirName = '%s_archived_app_%s%s' % (variant, today, tag)
os.mkdir(dirName)

# Copy the app and launcher_config
shutil.copytree(archiveRoot, '%s/%s' % (dirName, projectName))
shutil.copyfile('%s/launcher_config.txt' % archiveRoot, '%s/launcher_config.txt' % dirName)

# Copy kivy garden files
os.mkdir('%s/%s/.kivy/' % (dirName, projectName))
shutil.copytree('/Users/kramer/.kivy/garden', '%s/%s/.kivy/garden' % (dirName, projectName))

# Copy external site packages
shutil.copytree('external-site-packages', '%s/external-site-packages' % dirName)

zipDir(dirName, '%s.zip' % dirName)

os.chdir(current)

