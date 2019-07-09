	# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import MySQLdb as mdb 
import sys
from django.http import HttpResponse,HttpResponseRedirect
import cgi
from django.shortcuts import render	
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.contrib import messages
import copy 
from collections import Counter
from collections import OrderedDict
import operator
import calendar
from time import strptime
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import JsonResponse

def make_connection():
	try:
		con = mdb.connect('localhost','demo','demo123','lucumr')
		return con
	
	except (mdb.Error, e):
		print ("Error %d: %s" % (e.args[0],e.args[1]))
		sys.exit(1)

def view_blogs(request):
	
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)	
	cur.execute("""select * from blogs""")
	rows=cur.fetchall()
	con.close()
	paginator = Paginator(rows, 10) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		rows = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		rows = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		rows = paginator.page(paginator.num_pages)
	data={'blogs':rows}
	return render(request,'content.html',data)

def depth_first_search(request,comment_id,comment_rows,child_data,i):
	child_inner_dict={}
	id_items=[]
	for comment in comment_rows:
		if comment_id==comment['parent_id']:				
			child_inner_dict['depth']=i
			child_inner_dict['child_comment']=comment['comment']
			child_inner_dict['Id']=comment['Id']
			child_inner_dict['parent_id']=comment['parent_id']
			child_inner_dict['likes']=comment['likes']
			child_data.append(child_inner_dict)
			# print (child_data)
			child_inner_dict={}
			comment_id=comment['Id']
			i=i+1	
	# child_data=parallelNode_traversing(request,comment_rows,child_data)
		
	for data in child_data:
		id_items.append(data['Id'])
		
	
	return child_data,id_items	

def parallelNode_traversing(request,comment_rows,child_data,id_items):
	child_inner_dict={}
	temp=0
	count=0
	copy_child_data=copy.deepcopy(child_data)
	restart=True
	
	while restart:
		temp=0
		count=0
		for child in reversed(copy_child_data):
			# print (' i m in outer for',child)
			count=count+1
			child_inner_dict={}
			for comment in comment_rows:
				# print (' i m in inner for',len(child_data))
				if comment['Id']!=child['Id'] and comment['parent_id']== child['parent_id']: 
					
					if comment['Id'] not in id_items:
						
						Id=comment['Id']
						temp=1
						child_inner_dict['depth']=child['depth']
						child_inner_dict['child_comment']=comment['comment']
						child_inner_dict['Id']=comment['Id']
						child_inner_dict['parent_id']=comment['parent_id']
						child_inner_dict['likes']=comment['likes']
						child_data.append(child_inner_dict)
						i=child['depth']+1
						# print (child_data,'--------------',copy_child_data)
						child_data,id_items=depth_first_search(request,Id,comment_rows,child_data,i)
						copy_child_data=copy.deepcopy(child_data)
						# print ('after dfs-',copy_child_data)
						break
			
			if temp==1:
				break 
			elif temp==0 and count == len(copy_child_data):
				return child_data		
			# else:
			# 	restart=False
			# 	continue

			  				
		
	return child_data			
def view_description(request):
	
	Id=request.GET.get('id')
	comment_data=[]
	inner_dict={}
	child_data=[]
	child_inner_dict={}
	
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)
	# fetching blog_description	
	cur.execute("""select * from blogs where Id=%s""",(Id))
	desc_row=cur.fetchone()
	# fetching fresh_comments with no parent_id	
	cur.execute("""select Id,comment,parent_id,likes from comment where blog_id=%s order by parent_id""",(Id))
	comment_rows=cur.fetchall()
	# fetching total_comments				
	cur.execute("""select Count(Id) as total_comments from comment where blog_id=%s""",(Id))
	count_rows=cur.fetchone()
	con.close()
	# creating hierarchial structure of comments
	for cmnt in comment_rows:
		if cmnt['parent_id']==0:
			Id=cmnt['Id']
			inner_dict['depth']=cmnt['parent_id']
			inner_dict['root_comment']=cmnt['comment']
			inner_dict['Id']=Id
			inner_dict['likes']=cmnt['likes']

			child_data,id_items=depth_first_search(request,Id,comment_rows,child_data,i=1)
			if len(child_data)>0:
				child_data=parallelNode_traversing(request,comment_rows,child_data,id_items)  
			else:
				print ('no child exist')	 

			inner_dict['children']=child_data
			# print ('hello',child_data)
			comment_data.append(inner_dict)	
			child_data=[]	
			inner_dict={} 
	# print (comment_data)									
	data={'blog_desc':desc_row,'comments':comment_data,'total_comments':count_rows}
	return render(request,'content.html',data)	

def blog_archive(request):
	year=[]
	date=[]
	months=[]
	data_dict={}
	entries=[]
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)	
	cur.execute("""select created_at from blogs order by created_at desc""")
	rows=cur.fetchall()
	con.close()
	print (rows)

	
	for row in rows:
		date.append(row['created_at'])
		year.append(row['created_at'].year)
	print ('dates',date)	
	print ('year_list',year)	

	# retieving unique years
	myset = set(year)
	unique_year=sorted(myset, reverse=True)

	print(unique_year)

	# retrieving months
	for y in unique_year:
		for d in date:
			if y == d.year:
				print ('required date',calendar.month_abbr[d.month]+' '+str(d.year))
				months.append(calendar.month_name[d.month])
			else:
				continue
	# retrieving count of months
		data_dict[y]=dict(Counter(months))
		entries.append(data_dict)
		data_dict={}
		months=[]
	print ('entries',entries)

	return render (request,'content.html',{'archive_data':entries})                             
	

def blog_archive_year(request):
	date=[]
	months=[]
	data_dict={}
	entries=[]
	yr=int(request.GET.get('year'))
	print (yr)
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)	
	cur.execute("""select created_at from blogs order by created_at desc""")
	rows=cur.fetchall()
	con.close()
	print (rows)

	
	for row in rows:
		date.append(row['created_at'])
	print ('dates',date)	
	
	# retrieving months	
	for d in date:
		print (type(d.year),type(yr))
		print (d.year==yr)
		if d.year==yr:
			print ('required date',calendar.month_abbr[d.month]+' '+str(d.year))
			months.append(calendar.month_name[d.month])
			print ('months',months)
		else:
			continue
		
		# retrieving count of months
		data_dict[yr]=dict(Counter(months))
	entries.append(data_dict)
		
			
	print ('entries',entries)	
	return render (request,'content.html',{'archive_year':entries})     

def blog_archive_month(request):
	year=int(request.GET.get('year'))

	month=(request.GET.get('month'))
	print (type(year),type(month))
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)	
	cur.execute("""SELECT Id, title, created_at FROM blogs where MONTH(created_at) = %s AND YEAR(created_at) = %s order by created_at desc""",(strptime(calendar.month_abbr [list(calendar.month_name).index(month)],'%b').tm_mon,year))
	rows=cur.fetchall()
	con.close()
	print ('data',rows)
	return render (request,'content.html',{'archive_month':rows,'month':month,'year':year})    

def about_page(request):
	title='About Me'
	return render (request,'content.html',{'about_title':title})   	

def blog_tags(request):
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)	
	cur.execute("""SELECT Distinct tag,counter FROM tags""")
	rows=cur.fetchall()
	con.close()
	print ('data',rows)
	return render (request,'content.html',{'tags':rows})    

def blog_tags_link(request):
	tagname=request.GET.get('tagname')
	# incrmenting tag counter
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)
	cur.execute("""UPDATE tags SET counter = counter + 1 where tag=%s""",(tagname))
	con.commit()
	#opening tag_link	
	cur.execute("""SELECT blog.Id,blog.title, blog.created_at from tags tag inner join blogs blog on tag.blog_id=blog.Id where tag.tag=%s""",(tagname))
	rows=cur.fetchall()
	print ('data',rows)
	return render (request,'content.html',{'tags_info':rows,'tagname':tagname})    

def count_likes(request):
	blog_id = request.GET.get('Id', None)
	# print('dssd',blog_id)
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)
	cur.execute("""UPDATE blogs SET likes = likes + 1 where Id=%s""",(blog_id))
	con.commit()
	con.close()
	return render (request,'content.html')

def comment_save(request):
	parent_id=request.POST.get('parent_id')
	blog_id=request.POST.get('blog_idd')
	comment=request.POST.get('comment')
	# print ('ids',blog_id,comment)
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)
	if parent_id:
		cur.execute('INSERT INTO comment(blog_id,comment,parent_id) VALUES(%s,%s,%s)',(blog_id,comment,parent_id))
		con.commit()
		
	else:
		cur.execute('INSERT INTO comment(blog_id,comment,parent_id) VALUES(%s,%s,%s)',(blog_id,comment,0))
		con.commit()
		
	con.close()
	return redirect(reverse('view_description') + '?id='+blog_id)

def count_commentlikes(request):
	comment_id = request.GET.get('Id', None)
	print('dssd',comment_id)
	con=make_connection()
	cur=con.cursor(mdb.cursors.DictCursor)
	cur.execute("""UPDATE comment SET likes = likes + 1 where Id=%s""",(comment_id))
	con.commit()
	return HttpResponse(request)

