import rules

@rules.predicate
def is_post_author(user, post):
    return post.created_by == user

@rules.predicate
def is_logged_in(user):
    return user.is_authenticated

# can_change_entry = rules.has_perm('blog.change_entry')
is_editor = rules.is_group_member('Editors')
is_superuser = rules.is_superuser

rules.add_perm('post.change', is_post_author)
rules.add_perm('post.view_post', rules.is_authenticated)
rules.add_perm('post.view',      rules.is_authenticated) # check if deleted
rules.add_perm('post.add',       rules.is_authenticated)
rules.add_perm('post.delete',    is_post_author|is_superuser)
