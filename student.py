class Student:
    
    # constructor
    def __init__(self, name, courses=None):
        self.name = name # string type
        self.courses = [] if courses is None else courses # list of strings
        self.num_courses = len(self.courses)
        
    # enroll in a course
    def enroll_in_course(self, course_name): 
        self.courses.append(course_name)
        self.num_courses += 1 # increment the number of courses

    def unenroll_in_course(self, course_name):
        try:
            self.courses.remove(course_name)
            self.num_courses -= 1
        except:
            print("I'm not in that course!")