# MajsoulAI-fix
 

 雀魂麻将ai,雀魂麻将助手,雀魂麻将机器学习
 
 基于大佬的项目, https://github.com/747929791/MajsoulAI

 大量修改了一些bug

 现在可以正常启动了

 推荐全部以本地模式启动服务,因为远程服务器有延迟,会诱发一些不可预料的bug.

 启动方式:
 1. 先启动爬虫脚本:

     mitmdump -s  .\majsoul_wrapper\addons.py
 2. 再启动主程序:
    
    main.py --level 0   （根据自己的要求来使用参数）
    
    
 一些建议：（不定期更新）
 
 1.首先pytoch版本 要看你是什么卡，如果不懂装啥版本，推荐装纯cpu版本的，可以兼容n卡和a卡，如果是n卡的话要看你的是不是最新的30系列的，这个要自己去选对应支持的cuda版本
 
 2.如果不是python大佬，推荐直接裸装各种包，不要用那个虚拟环境安装各种包。
 
 3.关于liqi三件套的编译都在那个文件夹里面“ MajsoulAI-fix/majsoul_wrapper/proto/ ”，游戏更新的速度还是蛮快的。。最好自己去编译一下最新的版本。
 
 4.要格外注意一下，webdriver.Chrome 的驱动，要和proto这些一一对应，版本相同的重要性大于 全部拉到最新的版本。
    
