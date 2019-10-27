# -*- encoding=utf8 -*-
__author__ = "liulongbiao"

from airtest.core.api import *


auto_setup(__file__)

# touch(Template(r"tpl1572061082925.png", record_pos=(0.223, -0.099), resolution=(1280, 720)))

TPL_BTL_SSJ_ZS_5 = Template(r"tpl1572137976418.png", threshold=0.95, record_pos=(0.223, 0.084), resolution=(1280, 720))
TPL_AVATAR_KM = Template(r"tpl1572174866378.png", threshold=0.9, record_pos=(-0.237, -0.009), resolution=(1280, 720))
TPL_AVATAR_CBA = Template(r"tpl1572174911553.png", threshold=0.9, record_pos=(0.077, -0.009), resolution=(1280, 720))
TPL_SVT_CBA = Template(r"tpl1572146578835.png", threshold=0.9, record_pos=(-0.398, 0.08), resolution=(1280, 720))
TPL_SUIT_SSJ_AUO = Template(r"tpl1572146602174.png", threshold=0.8, record_pos=(-0.398, 0.148), resolution=(1280, 720))
TPL_SCROLL = Template(r"tpl1572164030830.png", threshold=0.75, record_pos=(0.469, 0.235), resolution=(1280, 720))
TPL_REFRESH = Template(r"tpl1572165942863.png", threshold=0.9, record_pos=(0.154, -0.177), resolution=(1280, 720))

TPL_ATTACK = Template(r"tpl1572168649410.png", threshold=0.75, record_pos=(0.395, 0.211), resolution=(1280, 720))
TPL_SELECT = Template(r"tpl1572169762864.png", record_pos=(0.001, -0.131), resolution=(1280, 720))


TPL_LASLOT_SELECT = Template(r"tpl1572169659166.png", record_pos=(-0.241, 0.056), resolution=(1280, 720))

TPL_LASLOT_NOBLE = Template(r"tpl1572170000768.png", threshold=0.8, record_pos=(-0.173, -0.115), resolution=(1280, 720))
TPL_LASLOT_QUICK = Template(r"tpl1572175497123.png", threshold=0.9, record_pos=(0.403, 0.118), resolution=(1280, 720))
TPL_LASLOT_BUSTER = Template(r"tpl1572175545958.png", record_pos=(0.005, 0.113), resolution=(1280, 720))

TPL_LASLOT_ARTS = Template(r"tpl1572175640507.png", threshold=0.9, record_pos=(-0.195, 0.12), resolution=(1280, 720))

TPL_MASTER_SKILL = Template(r"tpl1572174247693.png", threshold=0.75, record_pos=(0.433, -0.038), resolution=(1280, 720))
TPL_MS_SWITCH = Template(r"tpl1572174427789.png", record_pos=(0.347, -0.038), resolution=(1280, 720))
TPL_DO_SWITCH = Template(r"tpl1572175070597.png", threshold=0.9, record_pos=(-0.001, 0.207), resolution=(1280, 720))

TPL_BTN_NEXT = Template(r"tpl1572176753926.png", threshold=0.9, record_pos=(0.366, 0.247), resolution=(1280, 720))

TPL_BTN_DECIDE = Template(r"tpl1572188532409.png", threshold=0.9, record_pos=(0.154, 0.159), resolution=(1280, 720))

TPL_LABEL_SUPPORT = Template(r"tpl1572161166185.png", threshold=0.8, record_pos=(0.362, -0.244), resolution=(1280, 720))

TPL_LABEL_AP = Template(r"tpl1572188292195.png", threshold=0.9, record_pos=(0.0, -0.227), resolution=(1280, 720))

TPL_APPLE_GOLD = Template(r"tpl1572188367373.png", threshold=0.9, record_pos=(-0.12, -0.12), resolution=(1280, 720))

TPL_APPLE_SILVER = Template(r"tpl1572188409421.png", threshold=0.9, record_pos=(-0.122, -0.006), resolution=(1280, 720))

TPL_APPLE_COPPER = Template(r"tpl1572188453221.png", threshold=0.9, record_pos=(-0.118, 0.109), resolution=(1280, 720))

TPL_AP_APPLES = [
    TPL_APPLE_COPPER,
    TPL_APPLE_SILVER,
    TPL_APPLE_GOLD
]

TPL_ATTACK_BRANCHS = [
    ('attack', TPL_ATTACK),
    ('next', TPL_BTN_NEXT)
]
TPL_START_BRANCHES = [
    ('ap', TPL_LABEL_AP),
    ('support', TPL_LABEL_SUPPORT)
]

class BattleBot:
    def __init__(self, tplBattle, tplSptSvt = TPL_SVT_CBA, tplSptSuit = TPL_SUIT_SSJ_AUO, times = 1):
        self.tplBattle = tplBattle
        self.tplSptSvt = tplSptSvt
        self.tplSptSuit = tplSptSuit
        self.times = times
        self.round = 0;
    def run(self, times = 1):
        round = 0
        while round < times:
            self.runOnce()
            round = round + 1
    def runOnce(self):
        touch(self.tplBattle)
        sleep(2)
        name, pos = self._awaitMulti(TPL_START_BRANCHES, interval = 1)
        if name == 'ap':
            refueled = self.refuel();
            if not refueled:
                return False
            self._await(v = TPL_LABEL_SUPPORT)
        selected = self.selectSupport()
        if not selected:
            return False;
        self.battle()
        return True;
    def refuel(self):
        swipe((600, 420), (600, 260))
        sleep(0.5)
        screen = G.DEVICE.snapshot()
        for v in TPL_AP_APPLES:
            pos = v.match_in(screen)
            if pos:
                touch(pos)
                touch(TPL_BTN_DECIDE)
                return True
        return False
    def selectSupport(self):
        touch(Template(r"tpl1572167235337.png", threshold=0.75, record_pos=(-0.163, -0.18), resolution=(1280, 720)))

        svt = self._findSupport()
        if not svt:
            touch(Template(r"tpl1572167586320.png", threshold=0.9, record_pos=(-0.427, -0.245), resolution=(1280, 720)))
            return False
        else:
            touch(svt['result'])
            touch(Template(r"tpl1572168155446.png", threshold=0.9, record_pos=(0.428, 0.245), resolution=(1280, 720)))
            return True
    def _findSupport(self):
        times = 3
        svt = self._findSupportInPage()
        while (not svt) and times > 0:
            touch(TPL_REFRESH)
            sleep(0.5)
            svt = self._findSupportInPage()
            times = times - 1
        return svt
    def _findSupportInPage(self):
        svt, end = self._findSupportInScreen()
        while (not svt) and (not end):
            swipe((600, 630), (600, 230))
            svt, end = self._findSupportInScreen()
        return svt
    def _findSupportInScreen(self):
        screen = G.DEVICE.snapshot()
        scroll = TPL_SCROLL.match_in(screen)
        end = scroll[1] > 600
        svts = self.tplSptSvt.match_all_in(screen)
        suits = self.tplSptSuit.match_all_in(screen)
        if (not suits) or (not svts):
            return (None, end)
        for suit in suits:
            for svt in svts:
                (x1, y1) = svt['result']
                (x2, y2) = suit['result']
                diffx = x2 - x1
                diffy = y2 - y1
                if (-5 < diffx) and (diffx < 5) and (0 < diffy) and (diffy < 100):
                    return (svt, end)
        return (None, end)
    def battle(self):
        self._battle_1()
        self._battle_2()
        self._battle_3()
    def _battle_1(self):
        # BATTLE 1/3
        self._await()
        touch((40, 40)) # 点第一个怪
        touch((160, 572)) # 狂兰 2
        sleep(2)
        self._await()
        touch((480, 572)) # 孔明 2
        sleep(2)
        self._await()
        touch((570, 572)) # 孔明 3
        sleep(2)
        self._await()
        touch((700, 572)) # CBA 1
        wait(TPL_SELECT)
        touch(TPL_LASLOT_SELECT)
        
        ## 选卡攻击
        self._doAttack()
    def _battle_2(self):
        # BATTLE 2/3
        self._await(accelerate = True)
        touch((40, 40)) # 点第一个怪
        touch((256, 572)) # 狂兰 3
        sleep(2)
        self._await()
        touch((386, 572)) # 孔明 1
        wait(TPL_SELECT)
        touch(TPL_LASLOT_SELECT)
        
        ## 换人 2 <-> 4
        sleep(2)
        self._await()
        touch(TPL_MASTER_SKILL)
        sleep(1)
        touch(TPL_MS_SWITCH)
        touch(TPL_AVATAR_KM)
        touch(TPL_AVATAR_CBA)
        touch(TPL_DO_SWITCH)
        
        sleep(2)
        self._await(accelerate = True)
        touch((386, 572)) # CBA(S) 1
        wait(TPL_SELECT)
        touch(TPL_LASLOT_SELECT)
        
        sleep(2)
        self._await()
        touch((570, 572)) # CBA(S) 3
        wait(TPL_SELECT)
        touch(TPL_LASLOT_SELECT)

        ## 选卡攻击
        self._doAttack()
    def _battle_3(self):
        # BATTLE 3/3
        self._await(accelerate = True)
        touch((285, 40)) # 点第二个怪
        touch((480, 572)) # CBA(S) 2
        sleep(2)
        self._await()
        touch((800, 572)) # CBA 2
        sleep(2)
        self._await()
        touch((888, 572)) # CBA 3
        wait(TPL_SELECT)
        touch(TPL_LASLOT_SELECT)
        
        ## 主技能 1
        self._await()
        touch(TPL_MASTER_SKILL)
        sleep(2)
        touch((900, 310))
        
        ## 选卡攻击
        self._attackUtilNext()
    def _doAttack(self):
        """
           选卡攻击
        """
        self._await()
        touch(TPL_ATTACK)
        sleep(2)
        cards = CardSelector().select()
        for card in cards:
            touch(card)
        sleep(5)
    def _attackUtilNext(self):
        self._doAttack()
        name, pos = self._awaitMulti(TPL_ATTACK_BRANCHS, accelerate = True, interval = 2)
        
        while name != 'next':
            self._doAttack()
            name, pos = self._awaitMulti(TPL_ATTACK_BRANCHS, accelerate = True, interval = 2)
            
        touch(TPL_BTN_NEXT)
        sleep(3)
    def _await(self, v = TPL_ATTACK, accelerate = False, interval = 1):
        found = exists(v)
        while not found:
            if accelerate:
                touch((1250, 690))
            sleep(interval)
            found = exists(v)
        return found
    def _awaitMulti(self, vs, accelerate = False, interval = 1):
        found = self._find(vs)
        while not found:
            if accelerate:
                touch((1250, 690))
            sleep(interval)
            found = self._find(vs)
        return found
    def _find(self, vs):
        screen = G.DEVICE.snapshot()
        for (name, v) in vs:
            match_pos = v.match_in(screen)
            if match_pos:
                return (name, match_pos)
        return None
        

class CardSelector:
    def __init__(self):
        self.screen = G.DEVICE.snapshot()
        self.indexes = [(i, 0, 0) for i in range(5)]
        self._match(TPL_LASLOT_ARTS, 2, 3)
        self._match(TPL_LASLOT_QUICK, 3, 2)
        self._match(TPL_LASLOT_BUSTER, 1, 1)
        self.indexes.sort(key = lambda a: a[1], reverse = True)
    def _match(self, v, weight, order):
        cards = v.match_all_in(self.screen)
        if not cards:
            return;
        for card in cards:
            idx = card['result'][0] // 256
            self.indexes[idx] = (idx, weight, order)
    def select(self):
        cards = []
        noble = TPL_LASLOT_NOBLE.match_in(self.screen)
        items = 3
        if noble:
            cards.append(noble)
            items = 2
        idxs = self.indexes[0:items]
        idxs.sort(key = lambda a: a[2])
        for (idx, w, order) in idxs:
            cards.append((idx * 256 + 128, 500))
        return cards
        
bot = BattleBot(TPL_BTL_SSJ_ZS_5, tplSptSuit = TPL_SUIT_SSJ_AUO)
bot.run(times = 2)
# bot.runOnce()
#bot._battle_3()

#sel = CardSelector().select()
#print(sel)