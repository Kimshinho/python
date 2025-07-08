class BaseStrategy:
    """
    모든 전략의 기본 클래스
    상속받아서 매수 조건과 매도 조건을 구현해야 합니다.
    """

    def should_buy(self, prices) -> bool:
        """
        매수 조건을 정의하는 메서드
        - prices: 가격 리스트 (예: [1, 2, 3, 4, 5])
        - return: 매수 조건이 충족되면 True, 아니면 False
        """
        pass

    def should_sell(self, prices) -> bool:
        """
        매도 조건을 정의하는 메서드
        - prices: 가격 리스트 (예: [1, 2, 3, 4, 5])
        - return: 매도 조건이 충족되면 True, 아니면 False
        """
        pass
