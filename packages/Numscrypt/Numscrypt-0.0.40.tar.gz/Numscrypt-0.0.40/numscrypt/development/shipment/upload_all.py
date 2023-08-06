import os

shipDir = os.path.dirname (os.path.abspath (__file__)) .replace ('\\', '/')
appRootDir = '/'.join  (shipDir.split ('/')[ : -2])
distributionDir = '/'.join  (appRootDir.split ('/')[ : -1])
dynWebRootDir, statWebRootDir = eval (open ('upload_all.nogit') .read ())
sphinxDir = '/'.join ([appRootDir, 'docs/sphinx'])

def getAbsPath (rootDir, relPath):
	return '{}/{}'.format (rootDir, relPath)

def copyWebsite (projRelPath, webRelPath, static = False, subdirs = False):
	 os.system ('xcopy /Y {} {} {}'.format ('/E' if subdirs else '', getAbsPath (appRootDir, projRelPath) .replace ('/', '\\'), getAbsPath (statWebRootDir if static else dynWebRootDir, webRelPath) .replace ('/', '\\')))

os.chdir (sphinxDir)
os.system ('make html')
copyWebsite ('docs/sphinx/_build/html', 'numscrypt/docs/html/', True, True)

os.chdir (distributionDir)

os.system ('uploadPython')

os.system ('git add .')
os.system ('git commit -m"{}"'.format (input ('Description of commit: ')))
os.system ('git push origin master')

os.chdir (shipDir)
