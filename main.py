import copy


class Combo:
    """docstring for Combo"""

    def test_cards(self):
        normal_pool = sorted(self.pool, key=lambda card: card.val, reverse=True)

        pool_vals = [card.val for card in normal_pool]
        pool_suis = [card.sui for card in normal_pool]

        if 14 in pool_vals:
            ace_pool = copy.deepcopy(self.pool)
            for card in ace_pool:
                if card.val == 14:
                    card.val = 1
            ace_pool = sorted(ace_pool, key=lambda card: card.val, reverse=True)

        result = {}

        def put_result():
            self.cards = result['cards']

            cards_names = ' '.join([card.name for card in result['cards']])
            self.text = result['text'] + cards_names

            pre_power = ''.join([str(hex(card.val))[2:] for card in self.cards])

            if len(pre_power) == 2:
                pre_power += '000'

            power_0x = str(result['combo_index']) + pre_power

            self.power = int(power_0x, 16)

        def high_card():
            if self.power > 0:
                return None
            result['cards'] = normal_pool[:5]
            result['text'] = 'Старшая карта '
            result['combo_index'] = 0

            put_result()

        def one_pair():
            if self.power > 1:
                return None
            res = [card for card in normal_pool if pool_vals.count(card.val) == 2]

            if len(res) == 2:
                cards = [card for card in normal_pool if card.val != res[0].val]

                result['cards'] = res + cards[:3]
                result['text'] = 'Одна пара '
                result['combo_index'] = 1

                put_result()

        def two_pairs():
            if self.power > 2 or len(normal_pool) < 5:
                return None
            res = [card for card in normal_pool if pool_vals.count(card.val) == 2][:4]

            if len(res) == 4:
                cards = [card for card in normal_pool if card.val != res[0].val and card.val != res[2].val]

                result['cards'] = res + [cards[0]]
                result['text'] = 'Две пары '
                result['combo_index'] = 2

                put_result()

        def three():
            if self.power > 3 or len(normal_pool) < 5:
                return None
            res = [card for card in normal_pool if pool_vals.count(card.val) == 3]

            if len(res) == 3:
                cards = [card for card in normal_pool if card.val != res[0].val]

                result['cards'] = res + cards[:2]
                result['text'] = 'Тройка '
                result['combo_index'] = 3

                put_result()

        def straight():
            if self.power > 4 or len(normal_pool) < 5:
                return None

            def check_str(cards):
                straight_test = True
                x = 0
                while x < 4:
                    straight_test = straight_test and cards[x].val - 1 == cards[x + 1].val
                    x += 1
                return {'straight_test': straight_test, 'cards': cards}

            res_list = []

            if 14 in pool_vals:
                x = 0
                while True:
                    pre_res = check_str(ace_pool[-5 - x:][:5])
                    res_list.append(pre_res)
                    x += 1
                    if x == len(ace_pool) - 4:
                        break

            x = 0
            while True:
                pre_res = check_str(normal_pool[-5 - x:][:5])
                res_list.append(pre_res)
                x += 1
                if x == len(normal_pool) - 4:
                    break

            for res in res_list:
                if res['straight_test']:
                    result['cards'] = res['cards']
                    result['text'] = 'Стрит '
                    result['combo_index'] = 4

                    put_result()

        def flush():
            if self.power > 5 or len(normal_pool) < 5:
                return None
            res = [card for card in normal_pool if pool_suis.count(card.sui) > 4]

            if res:
                result['cards'] = res
                result['text'] = 'Флеш '
                result['combo_index'] = 5

                put_result()

        def full_house():
            if self.power > 6 or len(normal_pool) < 5:
                return None
            three_res = [card for card in normal_pool if pool_vals.count(card.val) > 2]
            if three_res:
                two_res = [card for card in normal_pool if
                           pool_vals.count(card.val) > 1 and card.val != three_res[0].val]
                if two_res:
                    result['cards'] = three_res[:3] + two_res[:2]
                    result['text'] = 'Фул-хаус '
                    result['combo_index'] = 6

                    put_result()

        def four():
            if self.power > 7 or len(normal_pool) < 5:
                return None

            res = [card for card in normal_pool if pool_vals.count(card.val) == 4]

            if res:
                cards = [card for card in normal_pool if card.val != res[0].val]

                result['cards'] = res + [cards[0]]
                result['text'] = 'Каре '
                result['combo_index'] = 7

                put_result()

        def straight_flush():
            if len(normal_pool) < 5:
                return None

            def check_sf(cards):
                straight_test = True
                flush_test = True
                x = 0
                while x < 4:
                    straight_test = straight_test and cards[x].val - 1 == cards[x + 1].val
                    flush_test = flush_test and cards[x].sui == cards[x + 1].sui
                    x += 1
                return {'straight_test': straight_test, 'flush_test': flush_test, 'cards': cards}

            res_list = []

            if 14 in pool_vals:
                x = 0
                while True:
                    pre_res = check_sf(ace_pool[-5 - x:][:5])
                    res_list.append(pre_res)
                    x += 1
                    if x == len(ace_pool) - 4:
                        break

            x = 0
            while True:
                pre_res = check_sf(normal_pool[-5 - x:][:5])
                res_list.append(pre_res)
                x += 1
                if x == len(normal_pool) - 4:
                    break

            for res in res_list:
                if res['straight_test'] and res['flush_test']:
                    result['cards'] = res['cards']
                    result['text'] = 'Стрит-флэш '
                    result['combo_index'] = 8

                    put_result()

        print(straight_flush())
        print(high_card())

    def __init__(self, pool):
        self.pool = pool
        self.power = 0
        self.text = ''
        self.cards = []
        self.test_cards()

