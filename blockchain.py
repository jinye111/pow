import hashlib
import json
import time
from typing import List, Dict, Any


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Dict[str, Any]] = []
        self.current_transactions: List[Dict[str, Any]] = []
        self.difficulty = difficulty  # 难度：前导 0 的个数

        # 创建创世区块
        self.new_block(proof=100, previous_hash="1")

    def new_block(self, proof: int, previous_hash: str = None) -> Dict[str, Any]:
        """
        创建一个新区块并加入链
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions.copy(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 重置当前交易列表
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        添加一笔新交易到待打包列表
        返回该交易将被打包进的区块索引
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        """
        计算区块的 SHA-256 哈希
        注意：必须对字典进行排序，保证哈希结果一致
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Dict[str, Any]:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        """
        简单的工作量证明算法：
        寻找一个数字 proof，使得 hash(last_proof + proof) 以 difficulty 个 0 开头
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof: int, proof: int) -> bool:
        """
        验证 proof 是否满足难度要求（前导 0）
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == '0' * self.difficulty

    def mine(self) -> Dict[str, Any]:
        """
        挖矿：找到合法 proof 后打包当前交易并出块
        """
        last_block = self.last_block
        last_proof = last_block['proof']

        # 进行 POW 计算
        proof = self.proof_of_work(last_proof)

        # 给矿工奖励（可选，这里简单加一笔奖励交易）
        self.new_transaction(
            sender="0",  # 系统奖励
            recipient="miner",
            amount=1.0
        )

        # 创建新区块
        previous_hash = self.hash(last_block)
        block = self.new_block(proof, previous_hash)
        return block

    def is_chain_valid(self) -> bool:
        """
        验证整条链是否合法（可选功能，但很有用）
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 检查 previous_hash 是否正确
            if current['previous_hash'] != self.hash(previous):
                return False

            # 检查 proof 是否有效
            if not self.valid_proof(previous['proof'], current['proof']):
                return False
        return True


# ==================== 演示 ====================
if __name__ == "__main__":
    bc = Blockchain(difficulty=4)

    print("创世区块已创建：")
    print(json.dumps(bc.chain[0], indent=2, ensure_ascii=False))
    print("-" * 50)

    # 添加几笔交易
    bc.new_transaction("Alice", "Bob", 5)
    bc.new_transaction("Bob", "Charlie", 2.5)

    print("开始挖矿（难度 = 4 个前导 0）...")
    start = time.time()
    new_block = bc.mine()
    end = time.time()

    print(f"挖矿成功！耗时 {end - start:.2f} 秒")
    print(json.dumps(new_block, indent=2, ensure_ascii=False))
    print("-" * 50)

    # 再挖一个块
    bc.new_transaction("Charlie", "Alice", 1)
    print("再次挖矿...")
    start = time.time()
    new_block2 = bc.mine()
    end = time.time()
    print(f"挖矿成功！耗时 {end - start:.2f} 秒")
    print(json.dumps(new_block2, indent=2, ensure_ascii=False))
    print("-" * 50)

    print(f"当前链长度: {len(bc.chain)}")
    print(f"链是否合法: {bc.is_chain_valid()}")