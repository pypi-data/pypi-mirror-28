C:\Users\SPrabhu>python -m pip install crcmod
Collecting crcmod
  Using cached crcmod-1.7.tar.gz
Installing collected packages: crcmod
  Running setup.py install for crcmod ... done
Successfully installed crcmod-1.7



C:\Users\SPrabhu>python -m pip install openpyxl
Collecting openpyxl
  Downloading openpyxl-2.5.0.tar.gz (169kB)
    100% |████████████████████████████████| 174kB 273kB/s
Collecting jdcal (from openpyxl)
  Downloading jdcal-1.3.tar.gz
Collecting et_xmlfile (from openpyxl)
  Downloading et_xmlfile-1.0.1.tar.gz
Installing collected packages: jdcal, et-xmlfile, openpyxl
  Running setup.py install for jdcal ... done
  Running setup.py install for et-xmlfile ... done
  Running setup.py install for openpyxl ... done
Successfully installed et-xmlfile-1.0.1 jdcal-1.3 openpyxl-2.5.0




PS D:\PythonWorkspace\A350_BITEmemoryProcessor> python setup.py register sdist upload -r https://www.python.org/pypi
running register
running egg_info
writing process_bm.egg-info\PKG-INFO
writing dependency_links to process_bm.egg-info\dependency_links.txt
writing top-level names to process_bm.egg-info\top_level.txt
reading manifest file 'process_bm.egg-info\SOURCES.txt'
writing manifest file 'process_bm.egg-info\SOURCES.txt'
running check
We need to know who you are, so please choose either:
 1. use your existing login,
 2. register as a new user,
 3. have the server generate a new password for you (and email it to you), or
 4. quit
Your selection [default 1]:
1
Username: sandeep-prabhu-pypi
Password:
Registering process_bm to https://upload.pypi.org/legacy/
Server response (410): Project pre-registration is no longer required or supported, so continue directly to uploading files.
running sdist
creating process_bm-0.7
creating process_bm-0.7\Test
creating process_bm-0.7\process_bm.egg-info
copying files to process_bm-0.7...
copying README.txt -> process_bm-0.7
copying setup.py -> process_bm-0.7
copying Test\__init__.py -> process_bm-0.7\Test
copying Test\binarySectorFile.py -> process_bm-0.7\Test
copying Test\csvWriter.py -> process_bm-0.7\Test
copying Test\fsid_data.py -> process_bm-0.7\Test
copying Test\process_bm.py -> process_bm-0.7\Test
copying Test\rawInputLogFile.py -> process_bm-0.7\Test
copying process_bm.egg-info\PKG-INFO -> process_bm-0.7\process_bm.egg-info
copying process_bm.egg-info\SOURCES.txt -> process_bm-0.7\process_bm.egg-info
copying process_bm.egg-info\dependency_links.txt -> process_bm-0.7\process_bm.egg-info
copying process_bm.egg-info\not-zip-safe -> process_bm-0.7\process_bm.egg-info
copying process_bm.egg-info\top_level.txt -> process_bm-0.7\process_bm.egg-info
Writing process_bm-0.7\setup.cfg
Creating tar archive
removing 'process_bm-0.7' (and everything under it)
running upload
Password:
Submitting dist\process_bm-0.7.tar.gz to https://www.python.org/pypi
Server response (200): OK
PS D:\PythonWorkspace\A350_BITEmemoryProcessor>