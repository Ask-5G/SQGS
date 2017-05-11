from PIL import Image
import os
from django.db import connection, transaction

model = 'Parts'
path = "/home/linuxuser/Desktop/decals/"
valid_images = [".jpg",".gif",".png",".jpeg"]
for file in os.listdir(path):
    extension = os.path.splitext(file)[1]
    if extension.lower() in self.valid_images:
        image = os.path.splitext(file)[2]
        query = "UPDATE %s SET='/images/parts/'+ %s WHERE description = %s",[model,file,image]
        cursor=connection.cursor()
        cursor.execute(sql)
        transaction.commit_unless_managed()

sql="select * from %s",,[model]
db.commit()
cursor.execute(sql)
data=cursor.fetchone()
print data