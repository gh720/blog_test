import rules

@rules.predicate
def is_post_author(user, post):
    return post.author == user

# can_change_entry = rules.has_perm('blog.change_entry')
is_editor = rules.is_group_member('Editors')
is_superuser = rules.is_superuser

rules.add_perm('post.change', is_post_author|is_editor|is_superuser)
rules.add_perm('post.view',      rules.is_authenticated) # check if deleted
rules.add_perm('post.add',       rules.is_authenticated)
rules.add_perm('post.delete',    is_post_author|is_superuser)
