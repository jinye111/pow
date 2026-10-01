import hashlib
import time
import rsa
import binascii


class POWAndRSA:
    def __init__(self, nickname):
        self.nickname = nickname
        self.target_nonce = None
        self.target_hash = None

    def mine_pow(self, difficulty):
        """
        挖矿：寻找满足指定数量0开头的hash
        difficulty: 0的个数
        """
        nonce = 0
        target_prefix = '0' * difficulty
        start_time = time.time()

        print(f"\n开始挖矿 - 难度: {difficulty}个0开头")
        print(f"昵称: {self.nickname}")

        while True:
            # 组合昵称和nonce
            data = f"{self.nickname}{nonce}"
            # 计算SHA256
            hash_result = hashlib.sha256(data.encode()).hexdigest()

            # 检查是否满足条件
            if hash_result.startswith(target_prefix):
                elapsed_time = time.time() - start_time
                print(f"✅ 找到有效的nonce: {nonce}")
                print(f"📝 数据: {data}")
                print(f"🔑 Hash: {hash_result}")
                print(f"⏱️  花费时间: {elapsed_time:.4f} 秒")

                if difficulty == 4:
                    self.target_nonce = nonce
                    self.target_hash = hash_result
                return nonce, hash_result, elapsed_time

            nonce += 1

            # 每10000次打印进度
            if nonce % 10000 == 0:
                print(f"  已尝试 {nonce} 次，当前hash: {hash_result[:8]}...")

    def rsa_demo(self):
        """
        RSA非对称加密演示
        """

        if self.nickname is None or self.target_hash is None:
            return
        print("\n" + "=" * 60)
        print("RSA 非对称加密演示")
        print("=" * 60)

        # 1. 生成公私钥对
        print("\n1️⃣ 生成RSA密钥对 (2048位)...")
        (pubkey, privkey) = rsa.newkeys(2048)
        print(f"✅ 公钥: {pubkey}")
        print(f"✅ 私钥: {privkey}")

        # 2. 准备签名数据
        message = f"{self.nickname}{self.target_nonce}"
        print(f"\n2️⃣ 准备签名的数据: {message}")

        # 3. 用私钥签名
        print("\n3️⃣ 使用私钥签名...")
        signature = rsa.sign(message.encode(), privkey, 'SHA-256')
        print(f"✅ 签名 (hex): {binascii.hexlify(signature).decode()[:64]}...")

        # 4. 用公钥验证
        print("\n4️⃣ 使用公钥验证签名...")
        try:
            # 验证签名
            verified_message = rsa.verify(message.encode(), signature, pubkey)
            print(f"✅ 验证成功！")
            print(f"📝 验证的消息: {message}")
            print(f"✅ 签名有效，数据完整未被篡改！")

            # 5. 测试篡改检测
            print("\n5️⃣ 测试篡改检测...")
            tampered_message = f"{self.nickname}{self.target_nonce}1"
            print(f"📝 篡改后的数据: {tampered_message}")
            try:
                rsa.verify(tampered_message.encode(), signature, pubkey)
                print("❌ 验证失败！")
            except rsa.VerificationError:
                print("✅ 成功检测到数据被篡改！")

        except rsa.VerificationError:
            print("❌ 验证失败！")

    def run(self):
        """
        运行完整流程
        """
        print("=" * 60)
        print("POW工作量证明 + RSA数字签名 完整演示")
        print("=" * 60)
        print(f"👤 昵称: {self.nickname}")

        # 1. 挖矿 - 4个0
        print("\n" + "=" * 60)
        print("第一阶段: POW - 4个0开头")
        print("=" * 60)
        self.mine_pow(4)

        # 2. 挖矿 - 5个0
        print("\n" + "=" * 60)
        print("第二阶段: POW - 5个0开头")
        print("=" * 60)
        self.mine_pow(5)

        # 3. RSA签名
        self.rsa_demo()