class Student:
  number_of_sutdents = 0
  def __init__(self, first_name, last_name, major):
    self.first_name = first_name
    self.last_name = last_name 
    self.major = major 
    Student.number_of_sutdents += 1
  
  def fullname_with_major(self):
    return f'{self.first_name} {self.last_name} is a ' \
           f'{self.major} major!'
           
student = Student('John', 'Miller', 'Math')      

print(f'Number of Student {Student.number_of_sutdents}')    
student.number_of_sutdents +=1
print(f'Number of Student {student.number_of_sutdents}')    
print(f'Number of Student {Student.number_of_sutdents}')   
