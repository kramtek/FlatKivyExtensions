
import os, string, shutil, subprocess, glob, fnmatch, zipfile, platform

from subprocess import call

def copyApp():
    # Copy over this application
    src = '/Users/kramer/%s' % projectName
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

    directoryRemoveList = ['.git', '.kivy', '.idea']
    for directory in directoryRemoveList:
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print 'Exception removing %s: %s' % (directory, str(e))

##def zipDir(path, ziph):
#def zipDir(path, dst):
#    print 'zipping contents of: %s --> %s' % (path, dst)
#    zipf = zipfile.ZipFile(outFile, 'w', zipfile.ZIP_DEFLATED)
#    for root, dirs, files in os.walk(path):
#        for filename in files:
#            # print '  adding: %s to zip' % filename
#            zipf.write(os.path.join(root, filename))
#    zipf.close()


tmpLocation = '/tmp/'
if platform.system() == 'Windows':
    tmpLocation = 'c:\\tmp\\'
print 'tmp location: %s' % tmpLocation
projectName = 'FlatKivyExtensions'
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

os.chdir(current)

