# MajsoulAI-fix
 

 雀魂麻将ai,雀魂麻将助手,雀魂麻将机器学习
 
 基于大佬的项目, https://github.com/747929791/MajsoulAI

 大量修改了一些bug,因为大佬的代码很久都没更新了,无法正常启动

 现在可以正常启动了

 推荐全部以本地模式启动服务,因为远程服务器有延迟,会诱发一些不可预料的bug.

 启动方式:
 1. 先启动爬虫脚本:

     mitmdump -s  .\majsoul_wrapper\addons.py
 2. 再启动主程序:
    
    main.py --level 0
    
