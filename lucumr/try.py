totaltags = document.getElementById('totaltags').value;
		console.log(totaltags)	
		for (i = 1; i <= totaltags.length; i++) { 
    		var counter= document.getElementById('count_' + i).value;
    		console.log(counter)
    		var tagname= document.getElementById('tag_' + i);
    		console.log(tagname)
    		if (counter == 1){
    			tagname.style.fontSize=27+"px";
			}




# old comment section
{% for cmnt in comments %} 
                    <div class="comments-list">
                        <div class="media">
                              <!--  <p class="pull-right"><small>5 days ago</small></p> -->
                             
                            <div class="media-body"> 
                                <!-- displaying fresh comments -->
                                <h4 class="media-heading user_name">User</h4>   
                                <span> {{ cmnt.comment }} </span><br> 
                                  <p><small><a href="">Like</a> - <a href="javascript:void(0)" name="div_{{forloop.counter}}" onclick="appendRow(name)">Reply</a></small></p>
                                    <!-- input-for reply comment with parent id -->
                                <form action="{% url 'comment-save'%}" method="POST" id="div_{{forloop.counter}}">
                                    {% csrf_token %}
                                    <input type="hidden" name="blog_idd" value="{{blog_desc.Id}}"/>
                                    <input type="hidden" name="parent_id" value="{{cmnt.Id}}"/>
                                </form> 
                                {% if reply_comments %}
                                <!-- displaying reply comments -->
                                    {% for rcmnt in reply_comments %}
                                        {% if rcmnt.parent_id == cmnt.Id %}
                                <div class="reply-body">        
                                    <span> {{ rcmnt.comment }} </span><br> 
                                    <p><small><a href="">Like</a> - <a href="javascript:void(0)" name="div-{{forloop.counter}}" onclick="appendRow(name)">Reply</a></small></p>
                                    <form action="{% url 'comment-save'%}" method="POST" id="div-{{forloop.counter}}">
                                    {% csrf_token %}
                                    <input type="hidden" name="blog_idd" value="{{blog_desc.Id}}"/>
                                    <input type="hidden" name="parent_id" value="{{rcmnt.Id}}"/>
                                </form> 
                                </div>
                                        {% endif %}
                                        {% for rrcmnt in reply_comments %}
                                            {% if rrcmnt.parent_id == rcmnt.Id %}
                                <div class="reply-reply-body">      
                                    <span> {{ rcmnt.comment }} </span><br> 
                                    <p><small><a href="">Like</a> - <a href="javascript:void(0)" name="div-{{forloop.counter}}" onclick="appendRow(name)">Reply</a></small></p>
                                    <form action="{% url 'comment-save'%}" method="POST" id="div-{{forloop.counter}}">
                                    {% csrf_token %}
                                    <input type="hidden" name="blog_idd" value="{{blog_desc.Id}}"/>
                                    <input type="hidden" name="parent_id" value="{{rcmnt.Id}}"/>
                                </form> 
                                </div>
                                            {% endif %}
                                        {% endfor %}                

                                    {% endfor %}
                                {% endif %}     

                            </div>
                          
                        </div>
                    </div>
                    {% endfor %}



# handling comment_data in levels
    # for comment in comment_rows:
    #   if comment['parent_id']==0:
    #       data.append(comment)
    # dict_data['level'+str(i)]=data
    # data=[]   
    # dict_copy = copy.deepcopy(dict_data)  
    
    # for level in range(5):
    #   print ('level',level)
    #   for parent in dict_data['level'+str(i)]:
    #       print ('abac',parent)
    #       for child in comment_rows:
    #           if parent['Id']==child['parent_id']:
    #               data.append(child)
    #   if len(data)==0:
    #       break;  
    #   i=i+1   
    #   dict_data['level'+str(i)]=data
    #   data=[]
    #   print (dict_data)
    # fetching total comments

for cmnt in comment_rows:
        if cmnt['parent_id']==0:
            Id=cmnt['Id']
            inner_dict['depth']=cmnt['parent_id']
            inner_dict['comment']=cmnt['comment']
            inner_dict['Id']=Id
            med_dict['root_comment']=inner_dict
            dict_data[str(cmnt['Id'])]=med_dict
            inner_dict={}
            med_dict={}
            
            for idx1,child_nodes in enumerate(comment_rows):
                if Id==child_nodes['parent_id']:
                    i=1
                    print (Id==child_nodes['parent_id'])
                    cmnt['Id']=Id
                    for idx2,sub_cmnt in enumerate(comment_rows):
                        if cmnt['Id']==sub_cmnt['parent_id']:
                            if idx1==idx2 or idx2>idx1:
                                # print (sub_cmnt)
                                child_inner_dict['depth']=i
                                child_inner_dict['comment']=sub_cmnt['comment']
                                child_inner_dict['Id']=sub_cmnt['Id']
                                child_dict['child_comment']=child_inner_dict
                                data.append(child_dict)
                                print (data)
                                child_dict={}
                                child_inner_dict={}
                                cmnt['Id']=sub_cmnt['Id']
                                i=i+1
                                print(i)
                                
            dict_data[str(Id)+'_children']=data 
            data=[]  
   