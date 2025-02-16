from DbServer.DbMainServer import DbMainServer

Dms = DbMainServer()


def judgeOneEqualListWord(recvWord, systemListWord):
    """
    判断接收消息前面几个字是否跟 触发关键词列表中的相匹配
    :param recvWord:
    :param systemListWord:
    :return:
    """
    for systemWord in systemListWord:
        if recvWord.startswith(systemWord):
            return True
    return False


def judgeEqualWord(recvWord, systemWord):
    """
    判断接收消息和触发关键字完全相同则返回True
    接收消息 == 触发关键字
    :param recvWord: 接收消息
    :param systemWord: 触发关键字
    :return:
    """
    if recvWord.strip() == systemWord.strip():
        return True
    return False


def judgeEqualListWord(recvWord, systemListWord):
    """
    判断接收消息在触发关键字列表中则返回True
    接收消息 in ['触发关键字列表']
    :param recvWord: 接收消息
    :param systemListWord: 触发关键字列表
    :return:
    """
    for listWord in systemListWord:
        if listWord.strip() == recvWord.strip():
            return True
    return False


def judgeInWord(recvWord, systemWord):
    """
    判断接收消息在触发关键字中则返回True
    接收消息 in 触发关键字
    :param recvWord:
    :param systemWord:
    :return:
    """
    if systemWord in recvWord:
        return True
    return False


def judgeInListWord(recvWord, systemListWord):
    """
    判断触发关键词列表中每一个关键字在接收消息中则返回True
    :param recvWord:
    :param systemListWord:
    :return:
    """
    for listWord in systemListWord:
        if listWord in recvWord:
            return True
    return False


def judgeSplitAllEqualWord(recvWord, systemListWord):
    """
    接收消息以空格切割，判断第一个元素是否在触发关键字列表中则返回True
    :param recvWord:
    :param systemListWord:
    :return:
    """
    if ' ' in recvWord:
        recvWord = recvWord.split(' ')[0]
        for listWord in systemListWord:
            if recvWord == listWord:
                return True
        return False
    return False


def judgeAtMe(selfId, content, atUserList):
    """
    判断有人@我, @所有人不算
    :param selfId:
    :param atUserList:
    :return:
    """
    if selfId in atUserList and '所有人' not in content:
        return True
    return False
