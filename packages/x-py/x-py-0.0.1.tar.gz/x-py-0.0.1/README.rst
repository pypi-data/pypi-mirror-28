基于 Tornado 的示例程序

设置配置文件

```
cp app.example.yaml cp app.yaml
```

安装第三方库命令

```
pip install pyyaml sqlalchemy mysql-connector
```

启动程序命令

```
python app.py
````

启动成功后，访问地址 http://localhost:8000

执行测试命令

python tests/test_all.py

coverage run tests/test.py
