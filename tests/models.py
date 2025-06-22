# tests/models.py (معدل)
from django.db import models
from academy.models import Course # بما أنك بتربط بالكورسات اللي في academy app

class Test(models.Model):
    # استخدام اسم "Test" في Django model للدلالة على Assignment عامةً
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    
    title = models.CharField(max_length=255) # عنوان الواجب/الاختبار
    description = models.TextField(blank=True, null=True) # وصف الواجب/الاختبار
    
    due_date = models.DateTimeField() # تاريخ الاستحقاق
    deadline = models.DateTimeField(null=True, blank=True) # تاريخ المهلة النهائية (deadLine في Flutter)
    
    # نوع الواجب/الاختبار (مثلاً: Quiz, Project, Homework, Lab, Report)
    # ممكن نستخدم Choices هنا عشان نحدد الأنواع المتاحة
    ASSIGNMENT_TYPES = [
        ('Quiz', 'Quiz'),
        ('Project', 'Project'),
        ('Homework', 'Homework'),
        ('Lab', 'Lab'),
        ('Report', 'Report'),
        ('Other', 'Other'),
    ]
    type = models.CharField(max_length=50, choices=ASSIGNMENT_TYPES, default='Homework')

    link = models.URLField(blank=True, null=True) # رابط للواجب (لو فيه ملف أو منصة خارجية)

    def __str__(self):
        return f"{self.title} for {self.course.name} ({self.type})"