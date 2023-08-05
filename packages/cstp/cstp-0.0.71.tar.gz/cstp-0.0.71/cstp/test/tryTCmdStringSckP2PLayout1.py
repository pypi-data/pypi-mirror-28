# -*- coding:utf-8 -*-
"""
Created on 2016-7-5
@author: WeiYanfeng

测试 TCmdStringSckP2PLayout 类。

"""
import _addpath
from weberFuncs import PrintTimeMsg, GetCurrentTime, PrintAndSleep

from peer.TCmdStringSckP2PLayout import TCmdStringSckP2PLayout


def TryTCmdStringSckP2PLayout():
    sHubId = 'fba008448317ea7f5c31f8e19c68fcf7'
    cssa = TCmdStringSckP2PLayout(sHubId, "127.0.0.1:8888", 'one', 'C', 'onePairC', 'sClientDevInfo')
    cssa.StartMainThreadLoop()

# -------------------------------------
if __name__ == '__main__':
    TryTCmdStringSckP2PLayout()
