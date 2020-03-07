import time
import requests
import json


class Api(object):
    """ Access the steemmonsters API
        https://github.com/holgern/steemmonsters
    """
    __url__ = 'https://steemmonsters.com/'

    def get_card_details(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            try:
                response = requests.get(self.__url__ + "cards/get_details")
                if str(response) != '<Response [200]>':
                    time.sleep(2)
                cnt2 += 1
            except:
                pass
        return response.json()
    #任务信息
    def get_quests(self,name):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            try:
                response = requests.get(self.__url__ + "players/quests?username="+name,timeout=20)
                if str(response) != '<Response [200]>':
                    time.sleep(2)
                cnt2 += 1
            except:
                pass
        return response.json()

    def get_purchases_stats(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "purchases/stats")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def settings(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "settings")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def players_leaderboard(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "players/leaderboard")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def find_cards(self, card_ids):
        if isinstance(card_ids, list):
            card_ids_str = ','.join(card_ids)
        else:
            card_ids_str = card_ids
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "/cards/find?ids=%s" % card_ids_str)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()



    def get_upcoming_tournaments(self, player=None, token=None):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            if player is None and token is None:
                response = requests.get(self.__url__ + "tournaments/upcoming")
            elif token is None:
                response = requests.get(self.__url__ + "tournaments/upcoming?username=%s" % player)
            else:
                response = requests.get(self.__url__ + "tournaments/upcoming?token=%s&username=%s" % (token, player))
            cnt2 += 1
        return response.json()

    def get_inprogress_tournaments(self, player=None, token=None):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            if player is None and token is None:
                response = requests.get(self.__url__ + "tournaments/in_progress")
            elif token is None:
                response = requests.get(self.__url__ + "tournaments/in_progress?username=%s" % (player))
            else:
                response = requests.get(self.__url__ + "tournaments/in_progress?token=%s&username=%s" % (token, player))
            cnt2 += 1
        return response.json()

    def get_completed_tournaments(self, player=None, token=None):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            if player is None and token is None:
                response = requests.get(self.__url__ + "tournaments/completed")
            elif token is None:
                response = requests.get(self.__url__ + "tournaments/completed?username=%s" % (player))
            else:
                response = requests.get(self.__url__ + "tournaments/completed?token=%s&username=%s" % (token, player))
            cnt2 += 1
        return response.json()

    def get_tournament(self, player, uid, token):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "tournaments/find?id=%s&token=%s&username=%s" % (uid, token, player))
            cnt2 += 1
        return response.json()
    def get_tournament_details(self,id):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "tournaments/find?id="+id)

            cnt2 += 1
        return response.json()

    def get_tournament_round_lineup(self,id,rnd):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "tournaments/battles?id="+id+"&round="+str(rnd))

            cnt2 += 1
        return response.json()

    def get_open_all_packs(self, player, edition, token):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "cards/open_all_packs/%s?player=%s&edition=%d&token=%s&username=%s" % (player, player, edition, token, player))
            cnt2 += 1
        return response.json()

    def get_open_packs(self, uuid, player, edition, token):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "cards/open_pack/%s?player=%s&edition=%d&token=%s&username=%s" % (uuid, player, edition, token, player))
            cnt2 += 1
        return response.json()

    def get_cards_packs(self, player, token):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            try:
                response = requests.get(self.__url__ + "cards/packs/%s?token=%s" % (player, token))
            except:
                pass
            cnt2 += 1
        return response.json()


    #获取玩家所有卡片
    def get_collection(self, player):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            try:
                response = requests.get(self.__url__ + "cards/collection/%s" % player)
            except:
                pass
            cnt2 += 1
        return response.json()



    #获取玩家信息，极为详细
    def get_player_login(self, player):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "players/login?name=%s" % player)
            cnt2 += 1
        return response.json()

    # 获取玩家信息，赛季分数等等
    def get_player_details(self, player):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            try:
                response = requests.get(self.__url__ + "players/details?name=%s" % player,timeout=20)
            except:
                pass
            cnt2 += 1
        return response.json()

    # 获取玩家任务信息
    def get_player_quests(self, player):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "players/quests?username=%s" % player,timeout=20)
            cnt2 += 1
        return response.json()

    #RC检测
    def get_player_vp(self, player):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            #response = requests.get("https://anyx.io/v1/rc_api/find_rc_accounts?accounts=%s" % player,timeout=20)
            #rjson=response.json()
            #rc=rjson["rc_accounts"]
            #max_rc=float(rc[0]["max_rc"])
            #rc_manabar=float(rc[0]["rc_manabar"]["current_mana"])
            #rate = (rc_manabar/max_rc) * 100
            url = "https://techcoderx.com"
            data = {"jsonrpc": "2.0", "method": "rc_api.find_rc_accounts", "params": {"accounts": [player]}, "id": 1}
            response = requests.post(url, data=json.dumps(data))
            rjson = response.json()
            rc = rjson["result"]["rc_accounts"]
            max_rc = float(rc[0]["max_rc"])
            rc_manabar = float(rc[0]["rc_manabar"]["current_mana"])
            rate = (rc_manabar / max_rc) * 100
            cnt2 += 1
        return rate

    def get_for_sale(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "market/for_sale")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_purchases_settings(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "purchases/settings")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()
    
    def get_purchases_status(self, uuid):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "purchases/status?id=%s" % uuid)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_from_block(self, block_num):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "transactions/history?from_block=%d" % block_num,timeout=25)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_transaction(self, trx):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "transactions/lookup?trx_id=%s" % trx)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_cards_stats(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "cards/stats")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    #获取卡片市场价格，card_detail_id：卡片编号， gold：是否金卡, edition：卡片等级
    def get_market_for_sale_by_card(self, card_detail_id, gold, edition):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "market/for_sale_by_card?card_detail_id=%d&gold=%s&edition=%d" % (card_detail_id, gold, edition))
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_market_for_sale_grouped(self):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "market/for_sale_grouped")
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def get_market_status(self, market_id):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "market/status?id=%s" % market_id)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    #玩家对战历史
    def get_battle_history(self, player="%24top"):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 20:
            try:
                response = requests.get(self.__url__ + "battle/history?player=%s" % player,timeout=20)
                if str(response) != '<Response [200]>':
                    time.sleep(1)
                cnt2 += 1
            except:
                pass
        return response.json()

    #比赛结果
    def get_battle_result(self, ids):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 20:
            try:
                response = requests.get(self.__url__ + "battle/result?id=%s" % ids,timeout=20)
                if str(response) != '<Response [200]>':
                    time.sleep(1)
                cnt2 += 1
            except:
                pass
        return response.json()

    def get_battle_status(self, ids):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 20:
            try:
                response = requests.get(self.__url__ + "battle/status?id=%s" % ids,timeout=20)
                if str(response) != '<Response [200]>':
                    time.sleep(1)
                cnt2 += 1
            except:
                pass
        return response.json()

    #玩家资金信息，捕抓率也在其内
    def get_player_balances(self,player):
        response = ""
        cnt = 0
        while str(response) != '<Response [200]>' and cnt < 20:
            try:
                response = requests.get(self.__url__ + "players/balances?username=%s" % player,timeout=10)
                if str(response) != '<Response [200]>':
                    time.sleep(1)
                cnt += 1
            except:
                pass
        return response.json()

    # 玩家steem资金信息
    def get_steem_balances(self, player):
        response = ""
        cnt = 0
        while str(response) != '<Response [200]>' and cnt < 20:
            try:
                response = requests.get("https://uploadbeta.com/api/steemit/account/?cached&id=%s" % player, timeout=20)
                rjson=response.json()
                banner = rjson[0]["balance"]
                banner = float(banner.replace(" STEEM", ""))
                if str(response) != '<Response [200]>':
                    time.sleep(1)
                cnt += 1
            except:
                pass
        return banner

    def get_enemy(self, player2):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get("https://api.steemmonsters.io/players/history?username=%s&limit=1" % player2)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        return response.json()

    def find_enemy_card(self, player2,enemy):
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.__url__ + "cards/collection/%s" % player2)
            if str(response) != '<Response [200]>':
                time.sleep(2)
            cnt2 += 1
        r_json = response.json()
        cards = r_json["cards"]
        monsters_linshi = []
        monsters2 = []
        key_num = 0
        enemy_sum = enemy[0]
        enemy_mon = enemy[1]
        for i in cards:
            if i["uid"] == enemy_sum:
                summoner2 = {'id': i['card_detail_id'], 'level': i['level'], 'uid': i['uid']}
            for w in enemy_mon:
                if i["uid"] == w:
                    w = {'key': key_num, 'id': i['card_detail_id'], 'level': i['level'], 'uid': i['uid']}
                    monsters_linshi.append(w)
                    key_num += 1
        # 重新排序
        key_num = 0
        for w in enemy_mon:
            for i in monsters_linshi:
                if i["uid"] == w:
                    i = {'key': key_num, 'id': i['id'], 'level': i['level'], 'uid': i['uid']}
                    monsters2.append(i)
            key_num += 1
        enemy_team = [summoner2, monsters2]


        return enemy_team

    #等级判定
    def rating(self,rating):
        ras=[0,0]
        if rating < 99:
            ras = ["新手",0]
        if 100 <= rating <= 399:
            ras = ["青铜3",5]
        if 400 <= rating <= 699:
            ras = ["青铜2",7]
        if 700 <= rating <= 999:
            ras = ["青铜1",9]
        if 1000 <= rating <= 1299:
            ras = ["白银3",12]
        if 1300 <= rating <= 1599:
            ras = ["白银2",15]
        if 1600 <= rating <= 1899:
            ras = ["白银1",18]
        if 1900 <= rating <= 2199:
            ras = ["黄金3",22]
        if 2200 <= rating <= 2499:
            ras = ["黄金2",26]
        if 2500 <= rating <= 2799:
            ras = ["黄金1",30]
        if 2800 <= rating <= 3099:
            ras = ["钻石3", 40]
        if 3100 <= rating <= 3399:
            ras = ["钻石2", 50]
        if 3400 <= rating <= 3699:
            ras = ["钻石1", 60]
        if 3700 <= rating <= 4199:
            ras = ["总冠军3", 80]
        if 4200 <= rating <= 4699:
            ras = ["总冠军2", 120]
        if rating >= 4700:
            ras = ["总冠军1", 150]

        return ras

    #获取捕抓率
    def get_dec_rec_rate(self,player, block_num):
        """
        :param player: name of player
        :param block_num: current block number
        :return: dark energy recovery rate in range [0-1]
        """
        balances = self.get_player_balances(player)
        ecr_balance = dict()
        for balance in balances:
            if balance["token"] == "ECR":
                ecr_balance = balance
                break
        settings = self.settings()
        return (((block_num - ecr_balance["last_reward_block"])*settings["dec"]["ecr_regen_rate"])+ecr_balance["balance"])/10000
