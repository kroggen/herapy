# -*- coding: utf-8 -*-

"""Communication(grpc) module."""

import grpc

from .grpc import account_pb2, blockchain_pb2, rpc_pb2, rpc_pb2_grpc
from .utils.converter import convert_tx_to_grpc_tx


class Comm:
    def __init__(self, target=None):
        self.__target = target
        self.__channel = None
        self.__rpc_stub = None

    def connect(self):
        self.disconnect()

        self.__channel = grpc.insecure_channel(self.__target)
        self.__rpc_stub = rpc_pb2_grpc.AergoRPCServiceStub(self.__channel)

    def disconnect(self):
        if self.__channel is not None:
            self.__channel.close()

    def create_account(self, address, passphrase):
        account = account_pb2.Account(address=address)
        return self.__rpc_stub.CreateAccount(request=rpc_pb2.Personal(account=account, passphrase=passphrase))

    def get_account_state(self, address):
        if self.__rpc_stub is None:
            return None

        rpc_account = account_pb2.Account()
        rpc_account.address = address
        return self.__rpc_stub.GetState(rpc_account)

    def get_blockchain_status(self):
        if self.__rpc_stub is None:
            return None

        return self.__rpc_stub.Blockchain(rpc_pb2.Empty())

    def get_accounts(self):
        if self.__rpc_stub is None:
            return None
        return self.__rpc_stub.GetAccounts(rpc_pb2.Empty())

    def get_block(self, block_hash):
        if self.__rpc_stub is None:
            return None
        v = rpc_pb2.SingleBytes()
        v.value = block_hash
        return self.__rpc_stub.GetBlock(v)

    def get_peers(self):
        return self.__rpc_stub.GetPeers(rpc_pb2.Empty())

    def get_node_state(self, timeout):
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = timeout.to_bytes(8, byteorder='little')
        return self.__rpc_stub.NodeState(single_bytes)

    def get_tx(self, tx_hash):
        single_bytes = rpc_pb2.SingleBytes()
        single_bytes.value = tx_hash
        return self.__rpc_stub.GetTX(single_bytes)

    def unlock_account(self, address, passphrase):
        account = account_pb2.Account(address=address)
        personal = rpc_pb2.Personal(passphrase=passphrase, account=account)
        return self.__rpc_stub.UnlockAccount(request=personal)

    def lock_account(self, address, passphrase):
        account = account_pb2.Account(address=address)
        personal = rpc_pb2.Personal(passphrase=passphrase, account=account)
        return self.__rpc_stub.LockAccount(request=personal)

    def get_peers(self):
        return self.__rpc_stub.GetPeers(rpc_pb2.Empty())

    # This RPC is for making and sending Tx inside a node.
    # Don't use it for sending TX which is made by a client.
    def send_tx(self, unsigned_tx):
        return self.__rpc_stub.SendTX(convert_tx_to_grpc_tx(unsigned_tx))

    # This RPC is for sending signed Txs made by a client.
    def commit_txs(self, signed_txs):
        rpc_txs = []
        for signed_tx in signed_txs:
            rpc_txs.append(convert_tx_to_grpc_tx(signed_tx))
        rpc_tx_list = blockchain_pb2.TxList()
        rpc_tx_list.txs.extend(rpc_txs)
        return self.__rpc_stub.CommitTX(rpc_tx_list)

    def query_contract(self, query):
        return self.__rpc_stub.GetQuery(convert_tx_to_grpc_tx(signed_tx))
