import time

#模拟企业数据库里的合同数据
MOCK_CONTRACTS = {
    "张三":"甲方(张三)同意将名下房产抵押给乙方.本合同一经签订,乙方拥有绝对免责权,无论发生任何意外.甲方均不得追究乙方责任.",
    "李四":"甲方(李四)与乙方合作开发软件.合同期限一年,双方违约需赔付违约金."
}

def get_contract_by_name(name:str) -> str:
    """工具1:根据客户姓名1,查询合同文本"""
    time.sleep(0.5) #模拟数据库查询耗时
    if name in MOCK_CONTRACTS:
        return f"合同查询成功,内容如下:{MOCK_CONTRACTS[name]}"
    return f"未找到名为{name}的合同."


def check_risks_keywords(text:str) -> str:
    """工具2:检查文本中是否包含高风险词汇"""
    time.sleep(0.5)
    #模拟企业里的高危词库
    risk_words = ["绝对免责","不追究责任","违约金过高","无限连带责任"]
    found_risks = [word for word in risk_words if word in text]

    if found_risks:
        return f"⚠️ 发现高风险条款!包含违规词汇:{','.join(found_risks)}"
    return f"✅ 未发现明显风险词汇."
