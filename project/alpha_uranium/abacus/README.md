为了还原邱老师说的TDOS：
![|500x400](https://obsidian-1319448707.cos.ap-chengdu.myqcloud.com/alphaU-W25-%E6%80%BB%E7%BB%93_image_3.png)
采用原INCAR参数，进行计算。我们进行一下的猜测：
1. 原胞不同。一次采用原胞project/alpha_uranium/abacus/primitive_cell，另一次采用单胞project/alpha_uranium/abacus/unit_cell。（认证失败了，abacus.band会自动转换成原胞结构。
2. 结构不同。经过认证，其采用的晶格常数是`"Alpha-U-test": (63, ["4c"], ["U"], [2.8420000076, 5.8656997681, 4.9340000153, 0.105])`，对比50K附近的晶格常数是：`"Alpha-U": (63, ["4c"], ["U"], [2.8364, 5.8666, 4.9363, 0.10187])`
