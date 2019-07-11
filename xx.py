

import os
if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NBcrm1.settings")
    import django
    django.setup()
    from nbapp1 import models
    import random
    l1=[]
    for i in range(1,101):
        obj=models.Customer(
                qq=''.join([str(i) for i in random.choices(range(1,10),k=11)]),
                name='liuyu'+str(i),
                sex=random.choice(['male','female']),
                source=random.choice(['qq','referral','website']),
                course=random.choice(['LinuxL','PythonFullStack'])
            )
        l1.append(obj)
    models.Customer.objects.bulk_create(l1)


























