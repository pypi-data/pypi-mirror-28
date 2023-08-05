""" 从Python发布工具导入"setup"函数 """
from distutils.core import setup

setup(
        name = 'python_recursion',
        version = '1.1.0',
        py_modules = ['python_recursion'],#将模块的元数据与setup函数的参数关联
        author = 'dmlpython',
        author_email = '1252366224@qq.com',
        url = 'https://gitee.com/Violaine/events',
        description = '用额外的参数控制缩进',
    )
