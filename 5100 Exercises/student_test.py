import student
import unittest

class StudentTests(unittest.TestCase):
    
    def test_01(self):
        stud = student.Student("Ben Pelczynski", ["DS 5100"])
        stud.enroll_in_course("DS 6001")
        stud.enroll_in_course("AR 1001")
        act = stud.num_courses
        exp = 3
        self.assertEqual(act, exp)
        
    def test_02(self):
        stud = student.Student("Ben Pelczynski", ["DS 5100"])
        stud.enroll_in_course("DS 6001")
        stud.unenroll_in_course("DS 6001")
        self.assertFalse("DS 6001" in stud.courses)

    def test_03(self):
        stud = student.Student("Ben Pelczynski", ["DS 5100"])
        exp = stud.num_courses
        stud.unenroll_in_course("DS 6001")
        act = stud.num_courses
        self.assertEqual(act, exp)

if __name__ == "__main__":
    unittest.main(verbosity=2)