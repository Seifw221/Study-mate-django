# schedules/models.py

from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField

class Schedule(models.Model):
    STAGE_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]

    TYPE_CHOICES = [
        ('lecture', 'Lecture Schedule'),
        ('exam', 'Exam Schedule'),
    ]

    # ** إضافة هذا الجزء لحقل القسم الجديد **
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('IS', 'Information Systems'),
        ('General', 'General (For 1st and 2nd year)') # ممكن نضيف قسم عام للسنين اللي مفيهاش تخصصات
    ]

    title = models.CharField(max_length=255, default='Unnamed Schedule')

    stage = models.IntegerField(choices=STAGE_CHOICES)
    schedule_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # ** إضافة حقل القسم هنا **
    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES,
        default='General', # قيمة افتراضية للسنين اللي مفيهاش أقسام
        blank=True, # ممكن يكون فاضي لو مفيش قسم معين
        null=True,
    )
    image = models.ImageField(
        upload_to='damanhour/Section/images/',
        storage=MediaCloudinaryStorage(),
        blank=True, null=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ** إضافة UniqueConstraint لضمان عدم تكرار جدول بنفس السنة والنوع والقسم **
        # ده مهم عشان ميقدرش حد يرفع جدولين (محاضرات / سنة تالتة / CS) مثلاً
        unique_together = ('stage', 'schedule_type', 'department')


    def __str__(self):
        # تعديل ليتضمن القسم في اسم العرض
        return f"{self.title} - {self.get_schedule_type_display()} - {self.get_stage_display()} - {self.get_department_display()}"