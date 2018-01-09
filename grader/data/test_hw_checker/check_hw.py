import os,sys,tarfile,shutil
TMP = "__tmp__"

def check_program():
  # check input parameters
  if len(sys.argv) != 4:
    print ("It seems like the .sh file is incorrect. The shell file should execute this program with these arguments:\ncheck_hw.py <code_dependencies> <expected_files> <tar_name>")
    return
  #check for inputted file list
  filelist = sys.argv[2]
  if not os.path.isfile(filelist):
    print ("It seems like the .sh file is incorect. The expected file list at path " + filelist + " does not exist")
    return
  # check tar file
  tar_name = sys.argv[3]
  if not os.path.isfile(tar_name):
    print_red("ERROR: Expected to find a file '" + tar_name + "' in the current directory " + os.getcwd())
    return
  try:
    tar = tarfile.open(tar_name)
    tar.extractall(TMP)
  except:
    print_red("ERROR: There was an issue opening your tar file. Is it corrupted?")
    return
  # list all files in the extracted folder
  allfiles = []
  for root,dirs,files in os.walk(TMP):
    for f in files:
      allfiles.append(root + '/' + f)
  # expected files are all present
  expected_structure = read_expected_files(filelist)
  check_for_expected_files(expected_structure, TMP)
  check_for_shebang(allfiles)
  # compiled code exists and has associated source code
  code_dependencies = get_code_dependencies(sys.argv[1])
  if not contains_code(allfiles, code_dependencies.keys()):
    print_purple("WARNING: Did not find any compiled or interpreted code from a recommended \n         language. (Ignore this if you are using another coding language.)")
  check_code_dependencies(allfiles, code_dependencies)
  print ("Check complete")

def cleanup():
  if os.path.isdir(TMP):
    shutil.rmtree(TMP)

# returns a dict view of the dir structure of expected files:
# files are modeled as name -> None
# directories are modeled as name -> dict()
def read_expected_files(fileloc):
  expected_contents = [line.strip() for line in open(fileloc).readlines()]
  expected_contents = [x for x in expected_contents if x != ''] # robust against empty lines
  filelist = dict()
  for content in expected_contents:
    by_directory = content.split('/')
    curr_directory = filelist
    while len(by_directory) > 1:
      next_directory = by_directory[0]
      if next_directory not in curr_directory:
        curr_directory[next_directory] = dict()
      curr_directory = curr_directory[next_directory]
      by_directory = by_directory[1:]
    curr_directory[by_directory[0]] = None
  return filelist

# Recursively checks actual_dir for expected files
def check_for_expected_files(expected_structure, actual_dir):
  pwd_name = actual_dir[len(TMP)+1:]
  if len(pwd_name) > 0: #add trailing /
    pwd_name += '/'
  for file_or_dir in expected_structure.keys():
    if expected_structure[file_or_dir] == None: #file
      if file_or_dir not in os.listdir(actual_dir):
        print_red("ERROR: Expected file '" + pwd_name + file_or_dir + "' not found in submission.")
    else: #folder
      if file_or_dir not in os.listdir(actual_dir): #folder doesn't exist
        print_red("ERROR: Expected folder '" + pwd_name + file_or_dir + "' not found in submission")
      else: #folder exists
        check_for_expected_files(expected_structure[file_or_dir], actual_dir + "/" + file_or_dir)
  return

def check_for_shebang(allfiles):
  for f in allfiles:
    if ".sh" == f[-3:]:
      shell_file = open(f,"r")
      first_line = shell_file.readline().strip()
      shell_file.close()
      if first_line != '#!/bin/sh':
        print_red("ERROR: Expected shell file '" + f[f.index(TMP)+len(TMP)+1:] + "' to begin with '#!/bin/sh'")

# returns a dictionary of list of lists
# the value is all possible required file extensions
# compiled_code -> [ [file_ext1, file_ext2], [file_ext3] ... ]
# e.g.
# exe -> [ [.c, .h], [.cs], [.fs], [.fsscript] ]
# this means an executable should have either [.c, .h] OR [.cs] OR ...
# in the degenerate case for compiled code this will look like:
# jar -> [ [.java] ]
# in the degenerate case for interpreted code this will look like:
# py -> [ [] ]
def get_code_dependencies(filepath):
  code_dependencies = dict()
  expected_languages = [line.strip() for line in open(filepath).readlines()]
  expected_languages = [x for x in expected_languages if x != ''] #robust against empty lines
  for line in expected_languages:
    ls = line.split()
    ext = '.' + ls[0]
    if ext not in code_dependencies:
      code_dependencies[ext] = []
    code_dependencies[ext].append(['.' + src for src in ls[1:]])
  return code_dependencies

# allfiles: a list of all the files in the tar
# code_extensions: a list of code extensions
def contains_code(allfiles, code_extensions):
  for f in allfiles:
    for ext in code_extensions:
      if f[-len(ext):] == ext:
        return True
  return False

# allfiles: a list of all the files in the tar
# code_dependencies is a dict, str -> [ [code1 code2] [code3 code4] ... ]
def check_code_dependencies(allfiles, code_dependencies):
  for compiled in code_dependencies.keys():
    binaries = []
    for f in allfiles:
      if f[-len(compiled):] == compiled:
        binaries.append(get_short_name(f))
    if len(binaries) > 0 and code_dependencies[compiled] != [[]]: # we found a compiled binary that expects separate code files
      found_some_code = False
      partial_source_code = []
      partial_source_code_src_list = []
      for src_list in code_dependencies[compiled]:
        has_src_files = [False] * len(src_list)
        src_files = []
        for i in range(len(src_list)):
          ext = src_list[i]
          for f in allfiles:
            if f[-len(ext):] == ext:
              has_src_files[i] = True
              src_files.append(get_short_name(f))
        if reduce(lambda x, y: x * y, has_src_files) == True:
          found_some_code = True
          print ("Found source file(s) '" + ', '.join(src_files) + "' for binary files(s) '" + ', '.join(binaries) + "'")
        elif len(has_src_files) > 1 and True in has_src_files: #found some src files but not all
          partial_source_code = src_files
          partial_source_code_src_list = src_list
      if not found_some_code and partial_source_code == []: #found no possible source code
        print_purple("WARNING: Did not find any source code for file(s) '" + ', '.join(binaries) + "'")
      elif not found_some_code and partial_source_code != []: #found only some source code
        print_purple("WARNING: Did not find all expected source code for file '" + ', '.join(binaries) +"'")
        print_purple("         Expected files of types " + ', '.join(partial_source_code_src_list) +", but only found " + ', '.join(partial_source_code))

def print_red(s):
  print ("\033[91m{}\033[00m" .format(s))

def print_purple(s):
  print ("\033[95m{}\033[00m" .format(s))

def get_short_name(s):
  short_name = s
  if '/' in short_name:
    short_name = short_name[len(short_name) - short_name[::-1].index('/'):]
  return short_name


# Parameters: check_hw.py code_dependencies expected_files tar_name 
# <code_dependencies> is a newline-separated list in space-separated format:
# compiled_extension code_extension1 code_extension2 [...]
# Each line begins with the extension (no ".") for the compiled/scripted code that is run
# Each following space-separated extension is the extension for the code
# If the program is scripted, then you just give the extension. 4 example lines:
# class java
# exe cs
# exe c
# py
# <expected_files> is a newline-separated list of all files (in relative path form) expected to be in the student submission
# <tar_name> is the expected name of the tar file
if __name__ == "__main__":
  try:
    check_program()
  except Exception as e:
    print_red("EXCEPTION: " + str(e) + "\nThis script is still a work in progress. Please contact davinman@uw.edu with the details of how this exception occurred and the tar file used.")
  finally:
    cleanup()
