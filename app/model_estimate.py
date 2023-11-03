# pylint: disable=C0114
class Estimation:
    """
    Class for counting daily_loss
    Some text
    And some text here
    """
    @staticmethod
    def daily_loss(baseline: str) -> int:
        """
        Def for counting daily loss for baseline
        :param baseline: 'constant-clean', 'constant-fraud', 'first-hypothesis'
        :return: daily loss in some currency
        """
        false_rate = {
            'constant-fraud': [1, 0],
            'constant-clean': [0, 1],
            'first-hypothesis': [0.177, 0.582]
        }

        fpr, fnr = false_rate[baseline]

        daily_purchases = 200000
        fraud_share = 0.05
        false_positive_cost = 10000
        false_negative_cost = 75000

        fraud_trans = daily_purchases * fraud_share
        clean_trans = daily_purchases * (1 - fraud_share)

        false_positive_trans = fpr * clean_trans
        false_negative_trans = fnr * fraud_trans

        false_positive_loss = false_positive_trans * false_positive_cost
        false_negative_loss = false_negative_trans * false_negative_cost

        total_loss = int(false_positive_loss + false_negative_loss)

        return total_loss
