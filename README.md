# PixivSurfer

This is a simple non-async GUI desktop application I made with TKinter and upbit's PixivPy

Link to upbit's pixivpy: https://github.com/upbit/pixivpy

Current feature:
  main.py: an application for viewing and downloading illustrations with IDs
  app.py: browse works of saved users, you can edit in the listed_user.json
  non-async => very SLOW (sorry..)

Requirements:
  1. Python 3
  2. PixivPy
  3. A pixiv account
  
Use pip to install PixivPy: 
  ~~~
  pip install pixivpy --upgrade
  ~~~

How to use:
  1. Firstly, type your username and password in the user.json (Required)
  2. Type in your desired download path if you wish to download
  3. Run main.py or app.py with python
