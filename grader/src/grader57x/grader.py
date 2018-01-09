import os,sys,tarfile,zipfile,struct,stat,difflib,shutil
from GradeReport import GradeReport as GR

def main():
  if len(sys.argv) < 2:
    invalid_arguments()
    return
  config = read_config_file(sys.argv[1])
  if sys.argv[2] == 'open':
    open_submissions(config['zipfile'], config['destination'], config['file_structure'], config['total_grade'], config['gold_grade'], config['report'])
  elif sys.argv[2] == 'open_student':
    open_student(sys.argv[3], sys.argv[4], config['destination'], config['file_structure'], config['total_grade'], config['gold_grade'], config['report'])
  elif sys.argv[2] == 'eval_all':
    eval_all(config['destination'], config['repro_comparison'], config['gold_comparison'], config['report'], config['gold_grade'])
  elif sys.argv[2] == 'eval_student':
    eval_single_student(config['destination'], sys.argv[3], config['repro_comparison'], config['gold_comparison'], config['report'], config['gold_grade'])
  else: #invalid
    invalid_arguments()

def invalid_arguments():
  print('Invalid argument passed in. This program expects 2-3 arguments: (1) the config file; (2) the opration')
  print('Possible operations: open')
  print('\teval_all')
  print('\teval_student <studentname>')

def open_submissions(zipname, foldername, file_structure, total_grade, gold_grade, reportname):
  #check input paramaters
  expected_files = read_expected_files(file_structure)
  if os.path.exists(foldername):
    print('It looks like the folder ' + foldername + ' already exists. Aborting.')
    return
  grade_report = unzip(zipname, foldername, total_grade, gold_grade)
  #check folder structure
  students = get_students('.')
  for student in students:
    os.chdir(student)
    points_off = check_for_nesting(grade_report, student)
    check_for_expected_files(grade_report, student, expected_files, '.', points_off)
    os.chdir('..')
  #write errors to file
  os.chdir('..')
  write_evaluation(grade_report, foldername, reportname)
  #prepare for running
  sh_files = find_sh_files(expected_files)
  for student in students:
    for sh_file in sh_files:
      if os.path.isfile(student + '/' + sh_file):
        os.chmod(student + '/' + sh_file, stat.S_IXUSR)

def open_student(student_name, student_tar, foldername, file_structure, total_grade, gold_grade, reportname):
  #check input parameters
  expected_files = read_expected_files(file_structure)
  if not os.path.exists(foldername):
    print('It looks like the folder ' + foldername + ' doesn\'t exist. Aborting.')
    return
  grade_report = GR.from_file(reportname)
  #move tar file to student directory and untar
  #if the student directory exists, delete it
  if os.path.exists(foldername + '/' + student_name):
    shutil.rmtree(foldername + '/' + student_name)
  os.mkdir(foldername + '/' + student_name)
  shutil.copyfile(student_tar, foldername + '/' + student_name + '/' + student_tar)
  os.chdir(foldername + '/' + student_name)
  #if student grade exists, remove it
  grade_report.remove_student(student_name)
  grade_report.add_student(student_name, total_grade, gold_grade)
  untar(student_name, grade_report)
  #write to file
  os.chdir('../..')
  write_evaluation(grade_report, foldername, reportname)
  #prepare for running
  for sh_file in find_sh_files(expected_files):
    if os.path.isfile(student_name + '/' + sh_file):
      os.chmod(student + '/' + sh_file, stat.S_IXUSR)
  print ('I cannot tell if the student submitted a readme separately. Please verify the student\'s readme score.')

#ends up in the unzipped file
def unzip(zipname, foldername, grade_total, gold_grade):
  #unzip canvas file
  zipped = zipfile.ZipFile(zipname, 'r')
  zipped.extractall(foldername)
  zipped.close()
  #reorganize student submissions
  os.chdir(foldername)
  students = set()
  allfiles = os.listdir('.')
  for file in allfiles:
    students.add(file[:file.index('_')])
  for student in students:
    os.mkdir(student)
  for file in allfiles:
    os.rename(file, get_student_name(file) + '/' + get_turnin_name(file))
  #initialize student grades
  grade_report = GR.new(students, grade_total, gold_grade)
  #for student in students:
  #  TAR_README_GRADE_STRS[student] = 4
  #  FILE_STRUCT_GRADE_STRS[student] = 6
  #untar student submissions
  for student in students:
    os.chdir(student)
    untar(student, grade_report)
    os.chdir('..')
  return grade_report

def untar(student, grade_report):
  #check for readme
  readme = None
  for file in os.listdir('.'):
    if 'readme' in file.lower():
      readme = file
      if 'readme' not in file: #there was some case issue
        grade_report.add_error(student, GR.FILES_MODULE_STR, 1, 'Readme file name should be lowercase: ' + readme)
  if readme == None: #no readme
    grade_report.add_error(student, GR.FILES_MODULE_STR, 2, 'No readme found.')
  elif readme[-3:] != 'pdf' and readme[-3:] != 'txt':
    grade_report.add_error(student, GR.FILES_MODULE_STR, 1, 'Readme extension is incorrect: ' + readme)
  #check for tar
  tarname = None
  for file in os.listdir('.'):
    if '.tar' in file:
      tarname = file
      break
  if tarname == None: #no tar file
    grade_report.add_error(student, GR.FILES_MODULE_STR, 2, 'No tar or gzip file found.')
    return
  if tarname[:6] == 'hw.tar' and tarname[-3:] == '.gz':
    #note: If the readme is also within the tar file, the tar readme will overwrite the original!
    try:
      tar = tarfile.open(tarname)
      tar.extractall('.')
    except (tarfile.TarError, struct.error) as e:
      grade_report.add_error(student, GR.FILES_MODULE_STR, 2, 'Tar file was corrupted: ' + tarname)
  elif tarname[-3:] == '.gz' or tarname[-4:] == '.tar': #this is a tar or gz file
    grade_report.add_error(student, GR.FILES_MODULE_STR, 1, 'Misnamed tar file: ' + tarname)
    try:
      tar = tarfile.open(tarname)
      tar.extractall('.')
    except (tarfile.TarError, struct.error) as e:
      grade_report.add_error(student, GR.FILES_MODULE_STR, 1, 'Tar file was corrupted: ' + tarname) # 1 pt already docked
  else: #no extractable tar file
    grade_report.add_error(student, GR.FILES_MODULE_STR,  2, 'Tar file not found.')

#returns the # of points taken off
def check_for_nesting(grade_report, student):
  empty_dir = False
  top_directory = '.'
  contents = os.listdir(top_directory)
  #first time is different: there may be a readme file and will definitely be a tar file
  if len(contents) == 2 or len(contents) == 3:
    for file_or_dir in os.listdir(top_directory):
      if os.path.isdir(file_or_dir):
        top_directory = file_or_dir
        empty_dir = True
  while(empty_dir):
    contents = os.listdir(top_directory)
    if len(contents) == 1 and os.path.isdir(top_directory + '/' + contents[0]):
      top_directory = top_directory + '/' + contents[0]
      empty_dir = True
    else:
      empty_dir = False
  #only if we ever recursed
  if top_directory != '.':
    grade_report.add_error(student, GR.FILES_MODULE_STR, 2, 'Incorrectly nested structure inside ' + top_directory)
    for content in contents:
      os.rename(top_directory + '/' + content, content)
    return 2
  return 0

def check_for_expected_files(grade_report, student, expected_structure, actual_dir, points_off):
  errors_list = check_for_expected_files_helper([], expected_structure, actual_dir)
  penalty = float(6) * 1 / count_daughter_files(expected_structure)
  error_sum = points_off
  for error in errors_list:
    if error_sum + penalty > 6: # max points off for files is 6 
      penalty = 6 - error_sum
      error += ' (max points off for file structure reached)'
    error_sum += penalty
    grade_report.add_error(student, GR.FILES_MODULE_STR, penalty, error)
  return

def check_for_expected_files_helper(errors_list, expected_structure, actual_dir):
  pwd_name = actual_dir
  if pwd_name == '.':
    pwd_name = ''
  elif pwd_name[0:2] == './':
    pwd_name = pwd_name[2:] + '/'
  for file_or_dir in expected_structure.keys():
    if expected_structure[file_or_dir] == None: #file
      if file_or_dir not in os.listdir(actual_dir):
        errors_list.append("File missing or in wrong location: '" + pwd_name + file_or_dir + "'")
    else: #folder
      if file_or_dir not in os.listdir(actual_dir): #folder doesn't exist
        num_files_missing = count_daughter_files(expected_structure[file_or_dir])
        errors_list.append("Folder missing or in wrong location: '" + pwd_name + file_or_dir + "' not found.")
      else: #folder exists
        check_for_expected_files_helper(errors_list, expected_structure[file_or_dir], actual_dir + "/" + file_or_dir)
  return errors_list

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

def count_daughter_files(expected_file_structure):
  count = 0
  for file_or_dir in expected_file_structure.keys():
    if expected_file_structure[file_or_dir] == None:
      count += 1
    else:
      count += count_daughter_files(expected_file_structure[file_or_dir])
  return count

def get_student_name(filename):
  return filename[:filename.index('_')]

def get_turnin_name(filename):
  return filename[len(filename) - filename[::-1].index('_'):]

def find_sh_files(expected_file_structure):
  sh_files = []
  for file_or_dir in expected_file_structure.keys():
    if expected_file_structure[file_or_dir] == None: #file
      if file_or_dir[-3:] == '.sh': #is an sh file
        sh_files.append(file_or_dir)
    else: #folder
      sh_files += find_sh_files(expected_file_structure[file_or_dir])
  return sh_files

def compare_files(file1, file2):
  diff_lines = []
  diff = difflib.unified_diff(file1, file2, fromfile='file1',tofile='file2',n=0)
  for line in diff:
    to_add = True
    for prefix in ('---','+++','@@'):
      if line.startswith(prefix):
        to_add = False
    if to_add:
      diff_lines.append(line)
  return diff_lines

def write_evaluation(grade_report,foldername, reportname):
  outfile = open(reportname, 'w')
  outfile.write(grade_report.pprint())
  outfile.close()

#expected_files a list of tuples [(filename sorted|unsorted) ..]
#test_files a list of tuples [(gold_file test_file sorted|unsorted) ..]
def eval_all(foldername, expected_files, test_files, reportname, gold_grade):
  grade_report = GR.from_file(reportname)
  for student in grade_report.get_students():
    eval_student(grade_report, foldername, student, expected_files, test_files, gold_grade)
  write_evaluation(grade_report, foldername, reportname)

def eval_single_student(foldername, student, expected_files, test_files, reportname, gold_grade):
  grade_report = GR.from_file(reportname)
  eval_student(grade_report, foldername, student, expected_files, test_files, gold_grade)
  write_evaluation(grade_report, foldername, reportname)

def eval_student(grade_report, foldername, student, expected_files, test_files, gold_grade):
  grade_report.clear_student_modules_except_files(student, gold_grade)
  check_expected_files_ran(grade_report, foldername, student, expected_files)
  check_test_files(grade_report, foldername, student, test_files)

def get_students(folder_name):
  return set(os.listdir(folder_name))

def read_config_file(filename):
  config_file = open(filename).readlines()
  config = dict()
  #initialize with defaults
  config['cmd'] = 'hw.cmd'
  config['gold_comparison'] = []
  config['repro_comparison'] = []
  gold_comparison_points = 0
  for line in config_file:
    if line == '':
      continue
    elif '=' not in line:
      print("The following line is formatted incorrectly:\n" + line)
      return False
    line_split = [a.strip() for a in line.split('=')]
    attribute = line_split[0]
    value = line_split[1].split()
    if attribute == 'zipfile':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['zipfile'] = value[0]
    elif attribute == 'destination':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['destination'] = value[0]
    elif attribute == 'report':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['report'] = value[0]
    elif attribute == 'cmd':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['cmd'] = value[0]
    elif attribute == 'run_script':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['run_script'] = value[0]
    elif attribute == 'gold_comparison':
      if not len(value) == 4:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['gold_comparison'].append((value[0], value[1], value[2], int(value[3])))
      gold_comparison_points += int(value[3])
    elif attribute == 'repro_comparison':
      if not len(value) == 2:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['repro_comparison'].append((value[0], value[1]))
#    Removing this: It is calculated as 25 + gold_comparison scores.
#    elif attribute == 'total_grade':
#      if not len(value) == 1:
#        print("The following line is formatted incorrectly:\n" + line)
#        return False
#      config['total_grade'] = int(value[0])
    elif attribute == 'file_structure':
      if not len(value) == 1:
        print("The following line is formatted incorrectly:\n" + line)
        return False
      config['file_structure'] = value[0]
    else:
      print("I don't understand the following line in from " + filename + ".\n" + line + "Skipping.")
  #set defaults
  if 'report' not in config:
    config['report'] = config['destination'] + '_report.txt' #default is foldername_report.txt
  config['total_grade'] = 25 + gold_comparison_points
  config['gold_grade'] = gold_comparison_points
  return config

def check_expected_files_ran(grade_report, folder_name, student, expected_files):
  number_files = len(expected_files)
  for file_tuple in expected_files:
    file = folder_name + '/' + student + '/' + file_tuple[0]
    if not os.path.isfile(file):
      program_matches_penalty = float(5)/number_files
      grade_report.add_error(student, GR.RUN_MODULE_STR, program_matches_penalty, 'No file to match against for file: ' + file_tuple[0])
    if not os.path.isfile(file + '.out'):
      program_runs_penalty = float(10)/number_files
      grade_report.add_error(student, GR.RUN_MODULE_STR, program_runs_penalty, 'Program did not run when trying to generate file: ' + file_tuple[0])
    if os.path.isfile(file) and os.path.isfile(file + '.out'):
      turned_in_file = open(file).readlines()
      run_file = open(file + '.out').readlines()
      if file_tuple[1] == 'sorted':
        sorted(turned_in_file)
        sorted(run_file)
      if turned_in_file != run_file:
        #diff them to a file in student directory
        diff_lines = compare_files(turned_in_file, run_file)
        diff_file = open(file + '.diff', 'w')
        diff_file.writelines(diff_lines)
        diff_file.close()
        #take off points and report # of lines different
        program_matches_penalty = float(5)/number_files
        grade_report.add_error(student, GR.RUN_MODULE_STR, program_matches_penalty, 'There are ' + str(len(diff_lines)) + ' lines different between the turned in and locally run versions of ' + file_tuple[0] + '. See ' + student + '/' + file_tuple[0] + '.diff')

def check_test_files(grade_report, folder_name, student, tested_files):
  for file_tuple in tested_files:
    test_file_path = folder_name + '/' + student + '/' + file_tuple[1]
    if not os.path.isfile(file_tuple[0]):
      print "ERROR, gold file " + file_tuple[0] + " does not exist!"
      break
    if not os.path.isfile(test_file_path):
      grade_report.add_error(student, 'Gold Standard Grading', file_tuple[3], 'Did not find output ' + file_tuple[1])
      continue
    # we can assume both files exist now
    gold_file = open(file_tuple[0]).readlines()
    test_file = open(test_file_path).readlines()
    if file_tuple[2] == 'sorted':
      sorted(gold_file)
      sorted(test_file)
    diff_lines = compare_files(gold_file, test_file)
    if len(diff_lines) == 0:
      grade_report.add_error(student, 'Gold Standard Grading', 0, file_tuple[1] + ' looks good')
    else:
      grade_report.add_error(student, 'Gold Standard Grading', file_tuple[3], str(len(diff_lines)) + ' lines different from the gold file for ' + file_tuple[1] + ': see ' + test_file_path + '.diff')
      diff_file = open(test_file_path + '.diff', 'w')
      diff_file.writelines(diff_lines)
      diff_file.close()

def compare_files(file1, file2):
  diff_lines = []
  diff = difflib.unified_diff(file1, file2, fromfile='file1',tofile='file2',n=0)
  for line in diff:
    do_add = True
    for prefix in ('---','+++','@@'):
      if line.startswith(prefix):
        do_add = False
    if do_add:
      diff_lines.append(line)
  return diff_lines

if __name__ == "__main__":
    main()
