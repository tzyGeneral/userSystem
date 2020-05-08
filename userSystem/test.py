import datetime


def save():

    # permissions1 = {'title': '新增用户', 'explain':'','remarks':'','createTime':datetime.datetime.now(), 'createUserId':0,'updateTime':datetime.datetime.now(),'updateUserId':0}
    # permissions2 = {'title': '修改用户', 'explain':'','remarks':'','createTime':datetime.datetime.now(), 'createUserId':0,'updateTime':datetime.datetime.now(),'updateUserId':0}
    permissions3 = {'title': '删除用户', 'explain': '', 'remarks': '', 'createTime': datetime.datetime.now(),
                    'createUserId': 0, 'updateTime': datetime.datetime.now(), 'updateUserId': 0}
    #
    permissions = Permissions.objects.create(**permissions3)
    #
    # role = Role(name='管理员',remarks='', createTime=datetime.datetime.now(),createUserId=0,updateTime=datetime.datetime.now(),updateUserId=0)
    # role.save()
    # role.permissions.add(permissions)

    # role = Role.objects.get(name='管理员')
    #
    # user = UserInfo(username='3', realName='王五',email='asdfg@qq.com',createTime=datetime.datetime.now(), createUserId=0,password='123',updateTime=datetime.datetime.now(),updateUserId=0)
    # user.save()
    # user.roles.add(role)
    # user.save()





if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userSystem.settings')
    django.setup()
    from userSystem.models import *
    save()