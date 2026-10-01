def main():
    print("Hello from pow!")

from POWAndRSA import POWAndRSA
if __name__ == "__main__":
    """主函数"""
    # 创建实例
    demo = POWAndRSA("didingdingnaicha")

    # 运行POW
    print("=" * 50)
    print("POW工作量证明")
    print("=" * 50)
    demo.mine_pow(4)
    # demo.mine_pow(5)

    # 运行RSA
    demo.rsa_demo()
