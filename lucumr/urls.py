from django.conf.urls import url
from lucumr import views

urlpatterns = [
url(r'^home/',views.view_blogs),
url(r'^blogs/',views.view_blogs),
url(r'^blog_description/',views.view_description,name='view_description'),
url(r'^archive/',views.blog_archive),
url(r'^archive_year/',views.blog_archive_year),
url(r'^archive_month/',views.blog_archive_month),
url(r'^about/',views.about_page),
url(r'^tags/',views.blog_tags),
url(r'^tags_link/',views.blog_tags_link),
url(r'^count_likes/',views.count_likes, name='count_likes'),
url(r'^comment_save/',views.comment_save, name='comment-save'),
url(r'^comment_count_likes/',views.count_commentlikes, name='comment_count_likes'),
]