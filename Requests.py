import time
import json
import time
from steem import Steem
from steem.blockchain import Blockchain
from api import Api
import string
import hashlib
from secrets import choice
import hashlib
from binascii import hexlify
from steembase.transactions import SignedTransaction
from steem.account import Account


nodes = ['https://steemd.minnowsupportproject.org']
nodes = ['https://anyx.io']
#nodes = ['https://techcoderx.com']
#nodes = ['https://steem.61bts.com']

nodes = ['https://rpc.esteem.app']



class Requests:

    def __init__(self,private_posting_key):
        self.s = Steem(nodes,keys=private_posting_key)
        #self.b = Blockchain(steemd_instance=self.s)
        self.api = Api()
        #self.settings = self.api.settings()

    def get_current_block_num(self):
        b = Blockchain(steemd_instance=self.s)
        return b.get_current_block_num()

    def find_match(self,name,type,tournament_id=None,round=0):
        if type == "Ranked:":
            json_data = {"match_type": type}
        elif type == "Tournament":
            json_data = {"match_type": type,"settings":{"tournament_id":tournament_id,"round":round}}
        else:
            json_data = {"match_type": type}

        tx=self.s.commit.custom_json('sm_find_match', json_data, required_posting_auths=[name])
        return tx

    def find_match_transaction(self,player,old_trx):
            #TODO add break condition, e.g. 5 minutes or validity block
            oo=0
            b = Blockchain(steemd_instance=self.s)
            while True:
                try:
                    block_num = b.get_current_block_num()
                    for r in self.api.get_from_block(block_num):
                        if r["type"] == "find_match":
                            if r["id"] != old_trx:
                                if r["player"] == player:
                                    print(r["id"])
                                    return r["id"]
                except:
                    print("Error while trying to get current block")
                    oo+=1
                    if oo>=8:
                        break

    def find_match_tt(self):
        b = Blockchain(steemd_instance=self.s)
        block_num = b.get_current_block_num()
        return block_num


    def enter_tournament(self, id, name):
        json_data = {"tournament_id": id,"signed_pw":""}

        self.s.custom_json('sm_enter_tournament', json_data, required_posting_auths=[name])

    def tournament_checkin(self, id, name):
        json_data = {"tournament_id": id,"signed_pw":""}

        self.s.custom_json('sm_tournament_checkin', json_data, required_posting_auths=[name])

    def submit_team(self, trx_id, team, name):
        """
        Submits a Steem Monsters team for the given match search transaction
        :param trx_id: search transaction id
        :param team: list of UID's corresponding to Monsters (Summoner at index 0, Remaining team 1-n
        :param name: player name
        """
        secret = self.generate_key()
        hash = self.generate_team_hash(team[0],team[1:],secret)

        json_data = {"trx_id": trx_id,"team_hash":hash, "summoner": team[0], "monsters": team[1:], "secret": secret}

        self.s.custom_json('sm_submit_team', json_data, required_posting_auths=[name])

    def generate_key(self,length=10):
        return ''.join(choice(string.ascii_letters + string.digits) for i in range(length))


    def generate_team_hash(self,summoner, monsters, secret):
        m = hashlib.md5()
        m.update((summoner + ',' + ','.join(monsters) + ',' + secret).encode("utf-8"))
        team_hash = m.hexdigest()
        return team_hash

    def open_card_pack(self,player, edition):
        """
        Opens a card pack and prints the transaction details

        Parameters:
        player (String): Name of the player
        edition (int): open pack of edition n, e.g. 1 for beta
        """

        self.s.custom_json("sm_open_pack",{ "edition": edition},required_posting_auths=[player])
        b = Blockchain(steemd_instance=self.s)
        while True:
            for r in self.api.get_from_block(b.get_current_block_num()):

                if r["type"] == "open_pack":

                    if r["player"] == player:
                        print(r)
                        return r["id"]

    def claim_reward(self,name,quest_id,type):

        json_data = {"type": type ,"quest_id":quest_id}

        self.s.custom_json('sm_claim_reward', json_data, required_posting_auths=[name])

     #获取赛季奖励
    def claim_season(self,name,season):

        json_data = {"type":"league_season","season":season,"app":"steemmonsters/0.7.6"}

        self.s.custom_json('sm_claim_reward', json_data, required_posting_auths=[name])

    def start_quest(self,name,type):

        json_data = {"type": type}

        self.s.custom_json('sm_start_quest', json_data, required_posting_auths=[name])

    #换新任务
    def refresh_quest(self, name):

        json_data = {"type":"daily","app":"steemmonsters/0.7.7"}

        self.s.commit.custom_json('sm_refresh_quest',json_data, required_posting_auths=[name])

    #发送一张卡片
    def send_card(self,name,toplayer,card_id):

        json_data = {"to": toplayer,"cards":[card_id]}

        self.s.custom_json('sm_gift_cards', json_data, required_posting_auths=[name])

    #发送一组卡片
    def send_allcard(self,name,toplayer,send):

        json_data = {"to": toplayer,"cards":send}

        self.s.custom_json('sm_gift_cards', json_data, required_posting_auths=[name])

    #游戏里提现DEC到steem-engines
    def transfer_withdraw(self,name,money_number):

        json_data = {"to":"steemmonsters","qty":money_number,"token":"DEC","type":"withdraw","app":"steemmonsters/0.7.7"}

        self.s.custom_json('sm_token_transfer', json_data, required_posting_auths=[name])

    # 游戏里提现DEC到tron
    def transfer_withdraw_tron(self, name, money_number):
        json_data ={"to":"sm-dec-tron","qty":money_number,"token":"DEC","type":"withdraw","app":"steemmonsters/0.7.11"}

        self.s.custom_json('sm_token_transfer', json_data, required_posting_auths=[name])

    # 游戏里提现DEC转账到别人
    def transfer_toplayer(self, name, money_number,toplayer):
        json_data = {"to": toplayer, "qty": money_number, "token": "DEC", "type": "withdraw",
                     "app": "steemmonsters/0.7.7"}

        self.s.custom_json('sm_token_transfer', json_data, required_posting_auths=[name])

    #steem-engines转账DEC
    def transfer_se_trans(self,name,toplayer,money):
        contract_payload = {'symbol': 'DEC', 'to': toplayer, 'quantity': str(money), 'memo': ''}
        json_data = {'contractName': 'tokens', 'contractAction': 'transfer', 'contractPayload': contract_payload}
        tx=self.s.commit.custom_json('ssc-mainnet1', json_data, required_auths=[name])
        return tx

    # steem-engines转账token
    def transfer_se_trans(self,token, name, toplayer, money):
        contract_payload = {'symbol': token, 'to': toplayer, 'quantity': str(money), 'memo': ''}
        json_data = {'contractName': 'tokens', 'contractAction': 'transfer', 'contractPayload': contract_payload}
        tx = self.s.commit.custom_json('ssc-mainnet1', json_data, required_auths=[name])
        return tx

    # 打开宝箱
    def open_ORB(self, name):
        json_data = {"edition":2,"app":"steemmonsters/0.7.10"}
        tx = self.s.commit.custom_json('sm_open_pack', json_data, required_posting_auths=[name])
        return tx



    # steem-engines转账steemp
    def transfer_steemp(self, name, toplayer, money):
        contract_payload = {'symbol': 'STEEMP', 'to': toplayer, 'quantity': str(money), 'memo': ''}
        json_data = {'contractName': 'tokens', 'contractAction': 'transfer', 'contractPayload': contract_payload}
        tx = self.s.commit.custom_json('ssc-mainnet1', json_data, required_auths=[name])
        return tx



    #提现steemp
    def transfer_withdraw_steemp(self,name,money):
        json_data = {"contractName":"steempegged","contractAction":"withdraw","contractPayload":{"quantity":str(money)}}
        tx=self.s.commit.custom_json('ssc-mainnet1', json_data, required_auths=[name])
        return tx

    # 卖掉DEC
    def transfer_market_sellbyse_DEC(self, name, money,price):
        json_data = {"contractName":"market","contractAction":"sell","contractPayload":{"symbol":"DEC","quantity":str(money),"price":str(price)}}
        tx = self.s.commit.custom_json('ssc-mainnet1', json_data, required_auths=[name])
        return tx

    # 卖卡
    def transfer_sell_card(self, name, sell_groud):
        json_data = sell_groud
        #sell_groud=[{"cards":["G4-171-A6T2NQ5IY8"],"currency":"USD","price":0.65,"fee_pct":500}]
        tx = self.s.commit.custom_json('sm_sell_cards', json_data, required_posting_auths=[name])
        return tx

    def helloworld(self, name):
        json_data = {"hello":"hello"}
        tx = self.s.commit.custom_json('helloworld', json_data, required_posting_auths=[name])
        return tx

    def huobi(self,mymoney,player):
        print("余额:", mymoney)
        num = mymoney
        if num > 1.1:
            # 转账
            kk = self.s.commit.transfer(
                "huobi-pro",
                num,
                "STEEM",
                memo="101634",
                account=player
            )

            tx = SignedTransaction(kk)
            tx.data.pop("signatures", None)
            print(tx)
            h = hashlib.sha256(bytes(tx)).digest()
            transaction_id = hexlify(h[:20]).decode("ascii")
            print(transaction_id)
            url = "https://steemd.com/tx/%s" % transaction_id
            print(url)

            print("转账完成")
        else:
            print("余额不足")
    #查询余额
    def maiyude(self,name="maiyude"):
        account = Account(name)
        balance = account['balance']
        balance = float(balance.replace(" STEEM", ""))
        return balance
    def cancel_sell(self,name,market_id):
        json_data = {"trx_ids":market_id}
        tx = self.s.commit.custom_json('sm_cancel_sell', json_data, required_posting_auths=[name])
        return tx
    def point(self,player):
        if "." in player:
            player = player.replace(".", "_")
        return player
    def gang(self,player):
        if "_" in player:
            player = player.replace("_", ".")
        return player