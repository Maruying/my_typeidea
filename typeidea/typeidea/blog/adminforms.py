
# 用作后台管理的Form
from django import forms

class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)   # desc字段名字要与model中的一致，Textarea为多行多列属性


