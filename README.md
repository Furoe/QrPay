# 基于二维码的电子现金支付协议
## QRcodePay
#### server.py
> 实现确定商家信息
> 解密交易金额
> 认证用户钱包
  

#### user.py
> 生成用户电子钱包，装载到二维码中，生成付款码
  
  
#### shop.py
> 对商家ID散列，加密交易金额
> 解析扫描二维码的有效性
