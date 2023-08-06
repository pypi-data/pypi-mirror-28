# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
from typing import Optional
from pyqrllib.pyqrllib import bin2hstr
from pyqryptonight.pyqryptonight import StringToUInt256, UInt256ToString, PoWHelper

from qrl.core.GenesisBlock import GenesisBlock
from qrl.core.BlockMetadata import BlockMetadata
from qrl.core.misc import logger, ntp
from qrl.core import config
from qrl.core.Block import Block
from qrl.core.Transaction import Transaction
from qrl.core.TransactionPool import TransactionPool
from qrl.generated import qrl_pb2


class ChainManager:
    def __init__(self, state):
        self.state = state
        self.tx_pool = TransactionPool()  # TODO: Move to some pool manager
        self.last_block = GenesisBlock()
        self.current_difficulty = StringToUInt256(str(config.dev.genesis_difficulty))
        self.current_target = None  # TODO: Not needed, replace all reference to local variable

        self.trigger_miner = False

    @property
    def height(self):
        return self.last_block.block_number

    def get_last_block(self) -> Block:
        return self.last_block

    def get_cumulative_difficulty(self):
        last_block_metadata = self.state.get_block_metadata(self.last_block.headerhash)
        return last_block_metadata.cumulative_difficulty

    @staticmethod
    def calc_difficulty(timestamp, parent_timestamp, parent_difficulty):
        ph = PoWHelper()
        ph.addTimestamp(parent_timestamp)
        current_difficulty = ph.getDifficulty(timestamp=timestamp,
                                              parent_difficulty=parent_difficulty)
        current_target = ph.getBoundary(current_difficulty)
        return current_difficulty, current_target

    def load(self, genesis_block):
        height = self.state.get_mainchain_height()

        if height == -1:
            self.state.put_block(genesis_block, None)
            block_number_mapping = qrl_pb2.BlockNumberMapping(headerhash=genesis_block.headerhash,
                                                              prev_headerhash=genesis_block.prev_headerhash)
            self.state.put_block_number_mapping(genesis_block.block_number, block_number_mapping, None)
            parent_difficulty = StringToUInt256(str(config.dev.genesis_difficulty))

            self.current_difficulty, self.current_target = self.calc_difficulty(genesis_block.timestamp,
                                                                                genesis_block.timestamp - 60,
                                                                                parent_difficulty)
            block_metadata = BlockMetadata.create()

            block_metadata.set_orphan(False)
            block_metadata.set_block_difficulty(self.current_difficulty)
            block_metadata.set_cumulative_difficulty(self.current_difficulty)

            self.state.put_block_metadata(genesis_block.headerhash, block_metadata, None)
        else:
            self.last_block = self.get_block_by_number(height)
            self.current_difficulty = self.state.get_block_metadata(self.last_block.headerhash).block_difficulty

    def validate_mining_nonce(self, block, enable_logging=False):
        parent_metadata = self.state.get_block_metadata(block.prev_headerhash)
        parent_block = self.state.get_block(block.prev_headerhash)
        input_bytes = StringToUInt256(str(block.mining_nonce))[-4:] + tuple(block.mining_hash)

        diff, target = self.calc_difficulty(block.timestamp,
                                            parent_block.timestamp,
                                            parent_metadata.block_difficulty)
        if enable_logging:
            logger.debug('-----------------START--------------------')
            logger.debug('Validate #%s', block.block_number)
            logger.debug('block.timestamp %s', block.timestamp)
            logger.debug('parent_block.timestamp %s', parent_block.timestamp)
            logger.debug('parent_block.difficulty %s', UInt256ToString(parent_metadata.block_difficulty))
            logger.debug('input_bytes %s', UInt256ToString(input_bytes))
            logger.debug('diff : %s | target : %s', UInt256ToString(diff), target)
            logger.debug('-------------------END--------------------')

        if not PoWHelper.verifyInput(input_bytes, target):
            if enable_logging:
                logger.warning("PoW verification failed")
                logger.warning("{}".format(self.miner.calc_hash(input_bytes)))
                logger.debug('%s', block.to_json())
            return False

        return True

    def validate_block(self, block, address_txn) -> bool:
        len_transactions = len(block.transactions)

        if len_transactions < 1:
            return False

        coinbase_tx = Transaction.from_pbdata(block.transactions[0])
        coinbase_tx.validate()

        if not self.validate_mining_nonce(block):
            return False

        if coinbase_tx.subtype != qrl_pb2.Transaction.COINBASE:
            return False

        if not coinbase_tx.validate():
            return False

        coinbase_tx.apply_on_state(address_txn)

        if not coinbase_tx.validate_extended(address_txn[coinbase_tx.txfrom], block.blockheader):
            return False

        # TODO: check block reward must be equal to coinbase amount

        for tx_idx in range(1, len_transactions):
            tx = Transaction.from_pbdata(block.transactions[tx_idx])

            if tx.subtype == qrl_pb2.Transaction.COINBASE:
                return False

            if not tx.validate():  # TODO: Move this validation, before adding txn to pool
                return False

            if not tx.validate_extended(address_txn[tx.txfrom], self.tx_pool.transaction_pool):
                return False

            expected_nonce = address_txn[tx.txfrom].nonce + 1

            if tx.nonce != expected_nonce:
                logger.warning('nonce incorrect, invalid tx')
                logger.warning('subtype: %s', tx.subtype)
                logger.warning('%s actual: %s expected: %s', tx.txfrom, tx.nonce, expected_nonce)
                return False

            if tx.ots_key_reuse(address_txn[tx.txfrom], tx.ots_key):
                logger.warning('pubkey reuse detected: invalid tx %s', tx.txhash)
                logger.warning('subtype: %s', tx.subtype)
                return False

            tx.apply_on_state(address_txn)

        return True

    def _pre_check(self, block, ignore_duplicate):
        if block.block_number < 1:
            return False

        if not block.validate():
            return False

        if (not ignore_duplicate) and self.state.get_block(block.headerhash):  # Duplicate block check
            logger.info('Duplicate block %s %s', block.block_number, bin2hstr(block.headerhash))
            return False

        return True

    def _try_orphan_add_block(self, block, batch):
        prev_block_metadata = self.state.get_block_metadata(block.prev_headerhash)

        if prev_block_metadata is None or prev_block_metadata.is_orphan:
            self.state.put_block(block, batch)
            self.add_block_metadata(block.headerhash, block.timestamp, block.prev_headerhash, batch)
            return True

        self.trigger_miner = False

        return False

    def _try_branch_add_block(self, block, batch=None) -> bool:
        parent_block = self.state.get_block(block.prev_headerhash)
        if not block.validate_parent_child_relation(parent_block):
            logger.warning('Failed to validate blocks parent child relation')
            return False

        address_set = self.state.prepare_address_list(block)  # Prepare list for current block
        address_txn = self.state.get_state(block.prev_headerhash, address_set)

        if self.validate_block(block, address_txn):
            self.state.put_block(block, None)
            self.add_block_metadata(block.headerhash, block.timestamp, block.prev_headerhash, None)

            last_block_metadata = self.state.get_block_metadata(self.last_block.headerhash)
            new_block_metadata = self.state.get_block_metadata(block.headerhash)
            last_block_difficulty = int(UInt256ToString(last_block_metadata.cumulative_difficulty))
            new_block_difficulty = int(UInt256ToString(new_block_metadata.cumulative_difficulty))

            self.trigger_miner = False
            if new_block_difficulty > last_block_difficulty:
                self.state.update_mainchain_state(address_txn, block.block_number, block.headerhash)
                self.last_block = block
                self.update_mainchain(block, batch)
                self.tx_pool.remove_tx_in_block_from_pool(block)
                self.state.update_mainchain_height(block.block_number, batch)
                self.state.update_tx_metadata(block, batch)

                self.trigger_miner = True

            return True

        return False

    def _add_block(self, block, ignore_duplicate=False, batch=None):
        block_size_limit = self.state.get_block_size_limit(block)
        if block_size_limit and block.size > block_size_limit:
            logger.info('Block Size greater than threshold limit %s > %s', block.size, block_size_limit)
            return False

        if not self._pre_check(block, ignore_duplicate):
            logger.debug('Failed pre_check')
            return False

        if self._try_orphan_add_block(block, batch):
            return True

        if self._try_branch_add_block(block, batch):
            return True

        return False

    def add_block(self, block: Block) -> bool:
        batch = self.state.get_batch()
        if self._add_block(block, batch=batch):
            self.state.write_batch(batch)

            batch = self.state.get_batch()
            self.update_child_metadata(block.headerhash, batch)
            self.state.write_batch(batch)
            return True

        return False

    def update_child_metadata(self, headerhash, batch):
        block_metadata = self.state.get_block_metadata(headerhash)

        childs = list(block_metadata.child_headerhashes)

        while childs:
            child_headerhash = childs.pop(0)
            block = self.state.get_block(child_headerhash)
            if not block:
                continue
            if not self._add_block(block, True, batch):
                self._prune([block.headerhash], batch=batch)
                continue
            block_metadata = self.state.get_block_metadata(child_headerhash)
            childs += block_metadata.child_headerhashes

    def _prune(self, childs, batch):
        while childs:
            child_headerhash = childs.pop(0)

            block_metadata = self.state.get_block_metadata(child_headerhash)
            childs += block_metadata.child_headerhashes

            batch.Delete(bin2hstr(child_headerhash).encode())
            batch.Delete(b'metadata_' + bin2hstr(child_headerhash).encode())

    def add_block_metadata(self, headerhash, block_timestamp, parent_headerhash, batch):
        parent_metadata = self.state.get_block_metadata(parent_headerhash)
        block_difficulty = (0,) * 32  # 32 bytes to represent 256 bit of 0
        block_cumulative_difficulty = (0,) * 32  # 32 bytes to represent 256 bit of 0
        if not parent_metadata:
            parent_metadata = BlockMetadata.create()
        else:
            parent_block = self.state.get_block(parent_headerhash)
            if parent_block:
                parent_block_difficulty = parent_metadata.block_difficulty
                parent_cumulative_difficulty = parent_metadata.cumulative_difficulty

                block_difficulty, _ = self.calc_difficulty(block_timestamp,
                                                           parent_block.timestamp,
                                                           parent_block_difficulty)

                block_cumulative_difficulty = StringToUInt256(str(
                    int(UInt256ToString(block_difficulty)) +
                    int(UInt256ToString(parent_cumulative_difficulty))))

        block_metadata = self.state.get_block_metadata(headerhash)
        if not block_metadata:
            block_metadata = BlockMetadata.create()

        block_metadata.set_orphan(parent_metadata.is_orphan)
        block_metadata.set_block_difficulty(block_difficulty)
        block_metadata.set_cumulative_difficulty(block_cumulative_difficulty)
        parent_metadata.add_child_headerhash(headerhash)
        self.state.put_block_metadata(parent_headerhash, parent_metadata, batch)
        self.state.put_block_metadata(headerhash, block_metadata, batch)

    def update_mainchain(self, block, batch):
        current_time = int(ntp.getTime())
        self.current_difficulty, self.current_target = self.calc_difficulty(current_time,
                                                                            block.timestamp,
                                                                            self.current_difficulty)
        block_number_mapping = None
        while block_number_mapping is None or block.headerhash != block_number_mapping.headerhash:
            block_number_mapping = qrl_pb2.BlockNumberMapping(headerhash=block.headerhash,
                                                              prev_headerhash=block.prev_headerhash)
            self.state.put_block_number_mapping(block.block_number, block_number_mapping, batch)
            block = self.state.get_block(block.prev_headerhash)
            block_number_mapping = self.state.get_block_number_mapping(block.block_number)

    def get_block_by_number(self, block_number) -> Optional[Block]:
        return self.state.get_block_by_number(block_number)

    def get_state(self, headerhash):
        return self.state.get_state(headerhash, set())

    def get_address(self, address):
        return self.state.get_address(address)

    def get_transaction(self, transaction_hash) -> list:
        for tx in self.tx_pool.transaction_pool:
            if tx.txhash == transaction_hash:
                return [tx, None]

        return self.state.get_tx_metadata(transaction_hash)

    def get_headerhashes(self):
        start_blocknumber = max(0, self.last_block.block_number - 10000)
        node_header_hash = qrl_pb2.NodeHeaderHash()
        node_header_hash.block_number = start_blocknumber
        for i in range(start_blocknumber, self.last_block.block_number + 1):
            block = self.state.get_block_by_number(i)
            node_header_hash.headerhashes.append(block.headerhash)

        return node_header_hash
