from django.db import models


class UserInfo(models.Model):
    id = models.AutoField(verbose_name='id', db_column='id', primary_key=True)
    username = models.CharField(unique=True, max_length=32, verbose_name='用户名', db_column='username')
    realName = models.CharField(max_length=32, verbose_name='真实姓名', db_column='realName')
    email = models.EmailField(max_length=256, verbose_name='邮箱', db_column='email')
    createTime = models.DateTimeField(verbose_name='创建时间', db_column='createTime')
    createUserId = models.IntegerField(verbose_name='创建人id', db_column='createUserId')
    updateTime = models.DateTimeField(verbose_name='修改时间', db_column='updateTime')
    updateUserId = models.IntegerField(verbose_name='修改人id', db_column='updateUserId')
    password = models.CharField(max_length=256, verbose_name='密码', db_column='password')
    isDelete = models.BooleanField(verbose_name='是否删除', db_column='isDelete', default=False)
    roles = models.ManyToManyField('Role')
    permissions = models.ManyToManyField('Permissions')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        db_table = "usersystem_userinfo"

    def __str__(self):
        return self.username


class Role(models.Model):
    id = models.AutoField(verbose_name='id', db_column='id', primary_key=True)
    name = models.CharField(max_length=16, verbose_name='角色名', db_column='name')
    remarks = models.CharField(max_length=256, verbose_name='备注', db_column='remarks')
    createTime = models.DateTimeField(verbose_name='创建时间', db_column='createTime')
    createUserId = models.IntegerField(verbose_name='创建人id', db_column='createUserId')
    updateTime = models.DateTimeField(verbose_name='修改时间', db_column='updateTime')
    updateUserId = models.IntegerField(verbose_name='修改人id', db_column='updateUserId')
    isDelete = models.BooleanField(verbose_name='是否删除', db_column='isDelete', default=False)
    permissions = models.ManyToManyField('Permissions')

    class Meta:
        verbose_name = '角色信息'
        verbose_name_plural = verbose_name
        db_table = "usersystem_role"

    def __str__(self):
        return self.name


class Permissions(models.Model):
    id = models.AutoField(verbose_name='id', db_column='id', primary_key=True)
    title = models.CharField(max_length=32, verbose_name='权限名', db_column='title')
    explain = models.CharField(max_length=128, verbose_name='权限说明', db_column='explain')
    remarks = models.CharField(max_length=256, verbose_name='备注', db_column='remarks')
    createTime = models.DateTimeField(verbose_name='创建时间', db_column='createTime')
    createUserId = models.IntegerField(verbose_name='创建人id', db_column='createUserId')
    updateTime = models.DateTimeField(verbose_name='修改时间', db_column='updateTime')
    updateUserId = models.IntegerField(verbose_name='修改人id', db_column='updateUserId')
    isDelete = models.BooleanField(verbose_name='是否删除', db_column='isDelete', default=False)

    class Meta:
        verbose_name = '权限信息'
        verbose_name_plural = verbose_name
        db_table = "usersystem_permissions"

    def __str__(self):
        return self.title
