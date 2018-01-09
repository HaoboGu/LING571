class GradeReport:
  REPORT_SEPARATOR = '---------------------------------------'
  NO_ERRORS_STR = 'No errors'
  ERRORS_STR = 'ERRORS'
  MODULE_STR = 'MODULE: '
  GRADE_STR = 'GRADE'
  TOTAL_STR = 'TOTAL'
  FILES_MODULE_STR = 'Standard: All files present'
  FILES_MODULE_TOTAL = 10
  RUN_MODULE_STR = 'Standard: Program runs'
  RUN_MODULE_TOTAL = 15
  GOLD_MODULE_STR = 'Gold Standard Grading' 
  
  def __init__(self):
    self.grade_report = dict()
  
  @classmethod
  def new(cls, students, total_grade, gold_grade):
    gr = cls()
    for student in students:
      gr.add_student(student, total_grade, gold_grade)
    return gr
  
  def add_student(self, student, total_grade, gold_grade):
    self.grade_report[student] = dict()
    self.grade_report[student][self.GRADE_STR] = total_grade
    self.grade_report[student][self.TOTAL_STR] = total_grade
    # initialize standard portions
    self.grade_report[student][self.FILES_MODULE_STR] = dict()
    self.grade_report[student][self.FILES_MODULE_STR][self.GRADE_STR] = self.FILES_MODULE_TOTAL
    self.grade_report[student][self.FILES_MODULE_STR][self.TOTAL_STR] = self.FILES_MODULE_TOTAL
    self.grade_report[student][self.FILES_MODULE_STR][self.ERRORS_STR] = []
    self.grade_report[student][self.RUN_MODULE_STR] = dict()
    self.grade_report[student][self.RUN_MODULE_STR][self.GRADE_STR] = self.RUN_MODULE_TOTAL
    self.grade_report[student][self.RUN_MODULE_STR][self.TOTAL_STR] = self.RUN_MODULE_TOTAL
    self.grade_report[student][self.RUN_MODULE_STR][self.ERRORS_STR] = []
    self.grade_report[student][self.GOLD_MODULE_STR] = dict()
    self.grade_report[student][self.GOLD_MODULE_STR][self.GRADE_STR] = gold_grade
    self.grade_report[student][self.GOLD_MODULE_STR][self.TOTAL_STR] = gold_grade
    self.grade_report[student][self.GOLD_MODULE_STR][self.ERRORS_STR] = []
  
  @classmethod
  def from_file(cls, reportname):
    grade_file = open(reportname).readlines()
    gr = cls()
    # studentname -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.MODULE_STR1_NAME -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.ERRORS_STR -> [error list]), 
    # self.MODULE_STR2_NAME -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.ERRORS_STR -> [error list])
    i = 0
    while (i < len(grade_file)):
      current_student = grade_file[i].strip()
      grade_line = grade_file[i+1].strip()
      gr.grade_report[current_student] = dict()
      gr.grade_report[current_student][cls.GRADE_STR] = float(grade_line[0:grade_line.index('/')])
      gr.grade_report[current_student][cls.TOTAL_STR] = float(grade_line[grade_line.index('/')+1:])
      i += 2
      while (i < len(grade_file) and cls.REPORT_SEPARATOR not in grade_file[i] and cls.MODULE_STR in grade_file[i]): #2nd conditional is a failsafe: should always be true
        current_module = grade_file[i].strip()[len(cls.MODULE_STR):]
        grade_line = grade_file[i+1].strip()
        gr.grade_report[current_student][current_module] = dict()
        gr.grade_report[current_student][current_module][cls.GRADE_STR] = float(grade_line[0:grade_line.index('/')])
        gr.grade_report[current_student][current_module][cls.TOTAL_STR] = float(grade_line[grade_line.index('/')+1:])
        gr.grade_report[current_student][current_module][cls.ERRORS_STR] = []
        i += 2
        while (cls.REPORT_SEPARATOR not in grade_file[i] and cls.MODULE_STR not in grade_file[i]): #reading errors
          if cls.NO_ERRORS_STR not in grade_file[i]:
            gr.grade_report[current_student][current_module][cls.ERRORS_STR].append(grade_file[i].strip())
          i += 1
      i += 1 #we've reached REPORT_SEPARATOR
    return gr

  def pprint(self):
    # studentname -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.MODULE_STR1_NAME -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.ERRORS_STR -> [error list]), 
    # self.MODULE_STR2_NAME -> dict(self.GRADE_STR -> #, self.TOTAL_STR -> #, self.ERRORS_STR -> [error list])
    print_str_list = []
    for student in self.get_students():
      print_str_list += [student, str(round(self.grade_report[student][self.GRADE_STR], 2)) + '/' + str(self.grade_report[student][self.TOTAL_STR])]
      graded_modules = self.get_modules(student)
      for module in graded_modules:
        print_str_list += [self.MODULE_STR + module, str(round(self.grade_report[student][module][self.GRADE_STR], 2)) + '/' + str(self.grade_report[student][module][self.TOTAL_STR])]
        for error in self.grade_report[student][module][self.ERRORS_STR]:
          print_str_list.append(error)
      print_str_list.append(self.REPORT_SEPARATOR)
    return '\n'.join(print_str_list)

  def remove_module_grades_from_student(self, student, modulename):
    if modulename in self.grade_report[student].keys():
      #adjust grade
      self.grade_report[student][self.GRADE_STR] -= self.grade_report[student][modulename][self.GRADE_STR]
      self.grade_report[student].pop(modulename)

  def remove_module_grades_from_all_students(self, modulename):
    for student in self.grade_report.keys():
      if modulename in self.grade_report[student].keys():
        #adjust grade
        self.grade_report[student][self.GRADE_STR] -= self.grade_report[student][modulename][self.GRADE_STR]
        self.grade_report[student].pop(modulename)

  def remove_student(self, studentname):
    if studentname in self.grade_report.keys():
      self.grade_report.pop(studentname)

  def add_module(self, student, modulename, grade_total):
    self.grade_report[student][modulename] = dict()
    self.grade_report[student][modulename][self.GRADE_STR] = grade_total
    self.grade_report[student][modulename][self.TOTAL_STR] = grade_total
    self.grade_report[student][modulename][self.ERRORS_STR] = []

  def clear_student_modules_except_files(self, student, gold_grade):
    for module in self.get_modules(student):
      if module != self.FILES_MODULE_STR:
        # add back deducted points
        self.grade_report[student][self.GRADE_STR] += self.grade_report[student][module][self.TOTAL_STR] - self.grade_report[student][module][self.GRADE_STR]
        self.grade_report[student].pop(module)
    #add back "Program runs"
    self.grade_report[student][self.RUN_MODULE_STR] = dict()
    self.grade_report[student][self.RUN_MODULE_STR][self.GRADE_STR] = self.RUN_MODULE_TOTAL
    self.grade_report[student][self.RUN_MODULE_STR][self.TOTAL_STR] = self.RUN_MODULE_TOTAL
    self.grade_report[student][self.RUN_MODULE_STR][self.ERRORS_STR] = []
    #add back gold module with expected value
    self.grade_report[student][self.GOLD_MODULE_STR] = dict()
    self.grade_report[student][self.GOLD_MODULE_STR][self.GRADE_STR] = gold_grade
    self.grade_report[student][self.GOLD_MODULE_STR][self.TOTAL_STR] = gold_grade
    self.grade_report[student][self.GOLD_MODULE_STR][self.ERRORS_STR] = []

  def get_students(self):
    retval = self.grade_report.keys()
    sorted(retval)
    return retval

  #want to display standard modules first, return them first
  def get_modules(self, student):
    modules = [ self.FILES_MODULE_STR, self.RUN_MODULE_STR ]
    modules += [ x for x in self.grade_report[student].keys() if x != self.GRADE_STR and x != self.TOTAL_STR and x != self.FILES_MODULE_STR and x != self.RUN_MODULE_STR ]
    return modules

  def add_error(self, student, module, penalty, errortext):
    p = penalty
    if module not in self.grade_report[student]:
      if module == self.FILES_MODULE_STR:
        self.add_module(student, module, FILES_MODULE_TOTAL)
      elif module == self.RUN_MODULE_STR:
        self.add_module(student, module, RUN_MODULE_TOTAL)
      else:
        self.add_module(student, module, 0) #default to no points
    if self.grade_report[student][module][self.TOTAL_STR] - penalty < 0:
      p = self.grade_report[student][module][self.TOTAL_STR]
    self.grade_report[student][self.GRADE_STR] -= p
    self.grade_report[student][module][self.GRADE_STR] -= p
    self.grade_report[student][module][self.ERRORS_STR].append('-' + str(round(penalty, 2)) + ' pts: ' + errortext)
