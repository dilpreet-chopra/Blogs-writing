# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField


class Blog(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
	title = models.CharField(max_length=500, null=False)
	subtitle = models.CharField(max_length=500, null=False)
	description = RichTextField(null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.title

	class Meta:
		managed = True
		db_table = 'blogs'


class Tag(models.Model):
	id = models.AutoField(db_column='Id', primary_key=True) 
	blog_id = models.ForeignKey(Blog, db_column='blog_id',on_delete=models.CASCADE)  # Field name made lowercase.
	tag = models.CharField(max_length=500, blank=True)

	def __str__(self):
		return self.tag

	class Meta:
		managed = True
		db_table = 'tags'


