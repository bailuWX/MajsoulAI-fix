# majsoul_wrapper
在[JianYangAI](https://github.com/erreurt/MahjongAI)的基础上进行了一些修改以支持本地的fake server，并添加了一些日志用于分析tanhou协议与AI流程(FuncTrace.log,AnaMsg.log)。通信逻辑在client/tenhou_client.py中。

JianYangAI是一个使用特征工程与LSTM预测模型的日本麻将AI，实力约为天凤2段。