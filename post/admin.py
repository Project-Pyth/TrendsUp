from django.contrib import admin
from django.utils.html import format_html

# Importing Post App Models
from post.models import Post, Category, PostComment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'date_posted', 'action_btn')

    search_fields = ('title', 'category')
    actions = None
    list_display_links = ('category', 'author')

    # list_filter = ('category',)
    change_list_template = 'admin/posts/list.html'
    add_form_template = 'admin/posts/add.html'
    change_form_template = 'admin/posts/edit.html'

    def action_btn(self, obj):
        html = "<a class='btn btn-default' href='/admin/post/post/" + str(obj.id) + "/change/'>Edit</a>&nbsp&nbsp&nbsp"
        html += "<a class='btn btn-default' href='/admin/post/post/" + str(obj.id) + "/delete/'>Delete</a>"

        return format_html(html)

    action_btn.short_description = 'Action'


# Post App Registration
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostComment)
