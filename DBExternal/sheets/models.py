from __future__ import unicode_literals

from django.db import models
import json

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

    def __unicode__(self):
        return self.username    

class Documents(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_name = models.CharField(max_length=20)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True)

    class Meta:
        db_table = 'documents'

    def __unicode__(self):
        return str(self.doc_id) 

class Ownership(models.Model):
    username = models.ForeignKey('Users', db_column='username')
    doc = models.ForeignKey('Documents',db_column='doc_id')
    rights = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'ownership'

    def __unicode__(self):
        return str(self.username)

class Sheets(models.Model):
    sheet_id = models.AutoField(primary_key=True)
    sheet_name = models.CharField(max_length=20)
    total_columns = models.IntegerField(blank=True, null=True)
    total_rows = models.IntegerField(blank=True, null=True)
    sheet_last_modified = models.DateTimeField(blank=True, null=True)
    sheet_created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'sheets'

    def __unicode__(self):
        return str(self.sheet_id)
    
    def as_json(self):
        return json.dumps(
            dict(
            sheet_id=self.sheet_id,
            sheet_name=self.sheet_name,
            total_columns=self.total_columns,
            total_rows=self.total_rows,
            )
            )

class ContainedIn(models.Model):
    doc = models.ForeignKey('Documents')
    sheet = models.ForeignKey('Sheets')

    class Meta:
        db_table = 'contained_in'
    def __unicode__(self):
        return str(self.doc)

class Cell(models.Model):
    cell_id = models.AutoField(primary_key=True)
    cell_x = models.IntegerField()
    cell_y = models.IntegerField()
    cell_color = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'cell'

    def __unicode__(self):
        return str(self.cell_id)

class IsIn(models.Model):
    sheet = models.ForeignKey('Sheets')
    cell = models.ForeignKey('Cell')

    class Meta:
        db_table = 'is_in'
    def __unicode__(self):
        return str(self.sheet)

class DataObject(models.Model):
    data_id = models.AutoField(primary_key=True)
    data_size = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'data_object'

class Has(models.Model):
    data = models.ForeignKey(DataObject)
    cell = models.ForeignKey(Cell)

    class Meta:
        db_table = 'has'


class Image(models.Model):
    data = models.ForeignKey(DataObject, primary_key=True)
    image_data = models.TextField(blank=True)  # This field type is a guess.
    image_title = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'image'

class Text(models.Model):
    data = models.ForeignKey(DataObject, primary_key=True)
    text_data = models.CharField(max_length=1000, blank=True)
    text_font = models.CharField(max_length=20, blank=True)
    font_size = models.IntegerField(blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'text'


class Video(models.Model):
    data = models.ForeignKey(DataObject, primary_key=True)
    video_data = models.TextField(blank=True)  # This field type is a guess.
    video_title = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'video'
