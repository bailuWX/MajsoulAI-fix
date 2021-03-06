# -*- coding: utf-8 -*-
from copy import deepcopy
from client.mahjong_tile import Tile


class WinCalc:

    @staticmethod
    def is_fulfilled(hand34, final_tile):
        """
        To check if current hand tiles satisfies the winning constrains
        :param hand34:
        :param final_tile:
        :return:
        """
        return len(WinCalc.win_parse(hand34, final_tile)) > 0

    @staticmethod
    def win_parse(hand34, final_tile):
        """
        To parse current hand tiles into melds which satisfies winning constrains
        :param hand34: tiles remaning in hand
        :param final_tile: the tile with which one finished his hand
        :return: list of list of list, different possibilities of partitioning total titles
        """
        hand_total = hand34 + [final_tile]
        hand_total_set = set(hand_total)
        res = []
        if all(hand_total.count(t) == 2 for t in hand_total_set) and len(hand_total) == 14:
             res.append([[t]*2 for t in hand_total_set])

        if all(t in hand_total for t in Tile.ONENINE) and all(t in Tile.ONENINE for t in hand_total):
            return [[[t]*hand_total.count(t) for t in Tile.ONENINE]]

        hand_total.sort()
        hand_man = [t for t in hand_total if t < 9]
        hand_pin = [t for t in hand_total if 9 <= t < 18]
        hand_suo = [t for t in hand_total if 18 <= t < 27]
        hand_chr = [t for t in hand_total if 27 <= t]
        man_parse = WinCalc._parse_nums(hand_man)
        pin_parse = WinCalc._parse_nums(hand_pin)
        suo_parse = WinCalc._parse_nums(hand_suo)
        chr_parse = WinCalc._parse_chrs(hand_chr)
        if hand_man and not man_parse:
            return res
        if hand_pin and not pin_parse:
            return res
        if hand_suo and not suo_parse:
            return res
        if hand_chr and not chr_parse:
            return res

        for a in man_parse:
            for b in pin_parse:
                for c in suo_parse:
                    res.append([m for m in a + b + c + chr_parse[0] if len(m) > 0])
        return res

    @staticmethod
    def fan_check(hand_partition, final_tile, melds, minkan, ankan, player_wind, round_wind):
        f, fd, m, md = WinCalc.fan_calc_long_para(hand_partition, final_tile, melds, minkan, ankan, False, player_wind, round_wind, False)
        return f > 0 or m > 0

    @staticmethod
    def cal_richii_fans(hand_partition, final_tile, melds, minkan, ankan, player_wind, round_wind):
        f, fd, m, md = WinCalc.fan_calc_long_para(hand_partition, final_tile, melds, minkan, ankan, False, player_wind, round_wind, True)
        if m > 0:
            return 12
        else:
            return f

    @staticmethod
    def _parse_nums(tiles):
        if len(tiles) == 0:
            return [[[]]]

        if len(tiles) == 1:
            return None

        if len(tiles) == 2:
            return [[tiles]] if tiles[0] == tiles[1] else None

        if len(tiles) == 3:
            ismeld = tiles[0] == tiles[1] == tiles[2] or (tiles[0] + 2) == (tiles[1] + 1) == tiles[2]
            return [[tiles]] if ismeld else None

        if len(tiles) % 3 == 1:
            return None

        res = []

        if len(tiles) % 3 == 2:
            if tiles[0] == tiles[1]:
                rec_res = WinCalc._parse_nums(tiles[2:])
                if rec_res:
                    for partition in rec_res:
                        res.append([tiles[0:2]] + partition)

        if tiles[0] == tiles[1] == tiles[2]:
            rec_res = WinCalc._parse_nums(tiles[3:])
            if rec_res:
                for partition in rec_res:
                    res.append([tiles[0:3]] + partition)

        if (tiles[0] + 1) in tiles and (tiles[0] + 2) in tiles:
            remain_tiles = deepcopy(tiles)
            remain_tiles.remove(tiles[0])
            remain_tiles.remove(tiles[0] + 1)
            remain_tiles.remove(tiles[0] + 2)
            rec_res = WinCalc._parse_nums(remain_tiles)
            if rec_res:
                for partition in rec_res:
                    res.append([[tiles[0], tiles[0] + 1, tiles[0] + 2]] + partition)

        return res if len(res) > 0 else None

    @staticmethod
    def _parse_chrs(tiles):
        if len(tiles) == 0:
            return [[]]

        if len(tiles) % 3 == 1 or any(tiles.count(t) == 1 for t in tiles):
            return None

        tiles_set = set(tiles)
        partition = [[t]*tiles.count(t) for t in tiles_set]

        return [partition] if len(partition) == (len(tiles) - 1) // 3 + 1 else None

    @staticmethod
    def cal_points(f, b, is_dealer, is_zimo):
            if f == 0:
                return 0, ''
            elif f < 5:
                if (b >= 40 and f >= 4) or (b >= 70 and f >= 3):
                    if is_dealer:
                        return 12000, "??????4000??????" if is_zimo else "??????12000???"
                    else:
                        return 8000, "??????2000-4000???" if is_zimo else "??????8000???"
                base_score = b * (2 ** (f + 2))
                if is_zimo:
                    if is_dealer:
                        each = ((base_score * 2 - 1) // 100 + 1) * 100
                        return each*3, "{}???{}???{}??????".format(b, f, each)
                    else:
                        dscore = ((base_score * 2 - 1) // 100 + 1) * 100
                        xscore = ((base_score - 1) // 100 + 1) * 100
                        return dscore + 2 * xscore, "{}???{}???{}-{}???".format(b, f, xscore, dscore)
                else:
                    score = ((base_score * 6 - 1) // 100 + 1) * 100 if is_dealer else ((base_score * 4 - 1) // 100 + 1) * 100
                    return score, "{}???{}???{}???".format(b, f, score)
            elif f == 5:
                if is_dealer:
                    return 12000, "??????4000??????" if is_zimo else "??????12000???"
                else:
                    return 8000, "??????2000-4000???" if is_zimo else "??????8000???"
            elif 6 <= f <= 7:
                if is_dealer:
                    return 18000, "??????6000??????" if is_zimo else "??????18000???"
                else:
                    return 12000, "??????3000-6000???" if is_zimo else "??????12000???"
            elif 8 <= f <= 10:
                if is_dealer:
                    return 24000, "??????8000??????" if is_zimo else "??????24000???"
                else:
                    return 16000, "??????4000-8000???" if is_zimo else "??????16000???"
            elif 11 <= f <= 12:
                if is_dealer:
                    return 36000, "?????????12000??????" if is_zimo else "?????????36000???"
                else:
                    return 24000, "?????????6000-12000???" if is_zimo else "?????????24000???"
            else:
                if is_dealer:
                    return 48000, "??????16000??????" if is_zimo else "??????48000???"
                else:
                    return 32000, "??????8000-16000???" if is_zimo else "??????32000???"

    @staticmethod
    def score_calc_long_para(hand34, final_tile, melds, minkan, ankan, is_zimo, player_wind, round_wind,
                             reach, bonus, benchan, reach_stick, is_dealer):
        """
        To calculate the winning point (passing player object)
        score = f(base, fan)
        Calls base_calc, fan_cals as subroutines
        :param hand34: hand tiles e.g. [1,2,3,11,12,13,22,22,22,24]
        :param final_tile: the last tile that makes it win e.g. 23
        :param melds: melds tiles e.g. [[1,2,3], [5,5,5]]
        :param minkan: minkan tiles e.g. [[4,4,4,4]]
        :param ankan: ankan tiles e.g. [[3,3,3,3]]
        :param is_zimo: if it was won by self drew tile or by dropped tile from opponents, bool
        :param player_wind: a special honor tile
        :param round_wind: a special honor tile
        :param reach: if the winner has called "richii"
        :param bonus: number of bonus tiles, which will be directly added on "fan"
        :param benchan: a parameter related to extra points added to base point
        :param reach_stick: a parameter related to extra points added to base point
        :param is_dealer: if the winner is dealer, bool
        :return: The score, score description, base description, corresponding result melds
        """
        res = {'best_score': 0, 'res_desc': "", 'base_desc': "", 'res_tiles': ""}
        win_parse = WinCalc.win_parse(hand34, final_tile)

        def form_tiles_string(h, m, mk, ak, ft):
            h_str = Tile.t34_to_g(h)
            m_str = Tile.t34_to_g(m + mk) + " *" + Tile.t34_to_g(ak)
            f_str = Tile.t34_to_g(ft)
            return "Final tiles: {} | {}, Win tile: {}".format(h_str, m_str, f_str)

        for p in win_parse:
            base, base_desc = WinCalc.base_calc_long_para(p, final_tile, melds, minkan, ankan, is_zimo, player_wind, round_wind)
            fan, fan_desc, maxi, maxi_desc = WinCalc.fan_calc_long_para(p, final_tile, melds, minkan, ankan, is_zimo, player_wind, round_wind, reach)
            if fan == 0 and maxi == 0:
                continue
            fan += bonus

            if maxi > 0:
                base_maxi_score = 48000 if is_dealer else 32000
                final_score = base_maxi_score * maxi + 1000 * reach_stick + benchan * 300
                if final_score > res['best_score']:
                    res['best_score'] = final_score
                    res['res_desc'] = "Result: ?????? {}??? {}??? -- {}".format(base_maxi_score * maxi, final_score, maxi_desc)
                    res['base_desc'] = ""
                    res['res_tiles'] = form_tiles_string(p, melds, minkan, ankan, final_tile)
            else:
                base_point, lose_desc = WinCalc.cal_points(fan, base, is_dealer, is_zimo)
                final_score = base_point + 1000 * reach_stick + benchan * (300 if base_point > 0 else 0)
                res_descript = "Result: {} {}??? -- {}".format(lose_desc, final_score, fan_desc)
                res_descript += "(???/???)??????({}???)".format(bonus) if bonus > 0 else ""
                if final_score > res['best_score']:
                    res['best_score'] = final_score
                    res['res_desc'] = res_descript
                    res['base_desc'] = base_desc
                    res['res_tiles'] = form_tiles_string(p, melds, minkan, ankan, final_tile)

        return res['best_score'], res['res_desc'], res['res_tiles'], res['base_desc']

    # base = number of occurances of certain melds
    @staticmethod
    def base_calc_long_para(hand_partition, final_tile, melds, minkan, ankan, is_zimo, player_wind, round_wind):

        # ???_calc three exceptions!
        if len(hand_partition) == 7:
            return 25, "Calc ???: ?????? ???25???"

        if len(hand_partition) + len(melds) == 5:
            chows = [m for m in hand_partition + melds if m[0] != m[1]]
            pair = [m for m in hand_partition if len(m) == 2][0]
            if len(chows) == 4 and pair[0] not in Tile.THREES + [player_wind, round_wind]:
                chows_with_final = [chow for chow in chows if final_tile in chow]
                if any((chw[0] == final_tile and chw[0] % 9 != 6) or (chw[2] == final_tile and chw[2] % 9 != 2)
                           for chw in chows_with_final):
                    if is_zimo and len(melds) == 0:
                        return 20, "Calc ???: ?????????????????? ?????? ???20???"
                    if not is_zimo and len(melds) > 0:
                        return 30, "Calc ???: ????????????????????? ???30???"

        res = {'base': 20, 'desc': "Calc ???: ?????????20"}

        def add_base(b, b_desc):
            res['base'] += b
            res['desc'] += b_desc

        def check_kezi():
            for meld in hand_partition:
                if len(meld) == 3:
                    if meld[0] == meld[1] == meld[2]:
                        if meld[0] in Tile.ONENINE:
                            if is_zimo or final_tile != meld[0]:
                                add_base(8, " ????????????+8")
                            else:
                                add_base(4, " ????????????+4")
                        else:
                            if is_zimo or final_tile != meld[0]:
                                add_base(4, " ????????????+4")
                            else:
                                add_base(2, " ????????????+2")

            for meld in melds:
                if meld[0] == meld[1]:
                    if meld[0] in Tile.ONENINE:
                        add_base(4, " ????????????+4")
                    else:
                        add_base(2, " ????????????+2")

        def check_kans():
            for mk in minkan:
                if mk[0] in Tile.ONENINE:
                    add_base(16, " ????????????+16")
                else:
                    add_base(8, " ????????????+8")
            for ak in ankan:
                if ak[0] in Tile.ONENINE:
                    add_base(32, " ????????????+32")
                else:
                    add_base(16, " ????????????+16")

        def check_pair(p):
            if p[0] in Tile.THREES:
                add_base(2, " ????????????+2")
            if p[0] == player_wind:
                add_base(2, " ????????????+2")
            if p[0] == round_wind:
                add_base(2, " ????????????+2")

        def check_waiting_type(p):
            chws = [m for m in hand_partition + melds if m[0] != m[1]]
            chws_with_final = [chow for chow in chws if final_tile in chow]
            if p[0] == final_tile and len(chws_with_final) == 0:
                add_base(2, " ??????+2")
            elif len(chws_with_final) > 0:
                if all((chw[1] == final_tile or (chw[0] == final_tile and chw[2] % 9 == 8)
                        or (chw[2] == final_tile and chw[0] % 9 == 0)) for chw in chws_with_final):
                    add_base(2, " ??????????????????+2")

        def check_win_type():
            if is_zimo:
                add_base(2, " ??????+2")
            if not is_zimo and len(melds + minkan) == 0:
                add_base(10, " ???????????????+10")

        pair = [m for m in hand_partition if len(m) == 2][0]
        check_kezi()
        check_kans()
        check_pair(pair)
        check_waiting_type(pair)
        check_win_type()

        res['desc'] += " = {}??? -> {}???".format(res['base'], ((res['base'] - 1) // 10 + 1) * 10)
        res['base'] = ((res['base'] - 1) // 10 + 1) * 10
        return res['base'], res['desc']

    # fan = number of special forms of tiles
    @staticmethod
    def fan_calc_long_para(hand_partition, final_tile, melds, minkan, ankan, is_zimo, player_wind, round_wind, reach):
        # result to be returned
        res = {'fan': 0, 'maxi': 0, 'fan_desc': "", 'maxi_desc': ""}

        # some preparation
        all_melds = hand_partition + melds + minkan + ankan
        all_melds_no_kan = hand_partition + melds
        all_tiles = [tile for meld in all_melds for tile in meld]
        is_menqing = len(melds + minkan) == 0
        len_open = len(melds + minkan + ankan)
        len_total = len_open + len(hand_partition)

        def add_fan(f, f_desc):
            res['fan'] += f
            res['fan_desc'] += f_desc

        def add_maxi(m, m_desc):
            res['maxi'] += m
            res['maxi_desc'] += m_desc

        def check_all_single_one_nine():
            if len(hand_partition) == 13:
                add_maxi(1, "????????????(??????) ")

        def check_seven_pairs():
            if len(hand_partition) == 7:
                add_fan(2, "?????????(2???) ")

        def check_win_type():
            if reach:
                add_fan(1, "??????(1???) ")
            if is_zimo and is_menqing:
                add_fan(1, "??????????????????(1???) ")

        def check_dori():
            for meld in all_melds:
                if len(meld) > 2 and meld[0] == meld[1]:
                    if meld[0] in Tile.THREES:
                        add_fan(1, "??????(1???) ")
                    if meld[0] == player_wind:
                        add_fan(1, "??????(1???) ")
                    if meld[0] == round_wind:
                        add_fan(1, "??????(1???) ")

        def check_no19():
            if all(t not in all_tiles for t in Tile.ONENINE):
                add_fan(1, "?????????(1???) ")

        def check_3chows_same_color():
            if len_total == 5:
                chows = list()
                for meld in all_melds_no_kan:
                    if len(meld) == 3 and meld[0] != meld[1]:
                        chows.append(meld)
                if len(chows) > 2:
                    for i in range(0, 7):
                        if all([i + t + 0, i + t + 1, i + t + 2] in chows for t in [0, 9, 18]):
                            if is_menqing:
                                add_fan(2, "????????????(2???) ")
                            else:
                                add_fan(1, "????????????(1???) ")
                            break

        def check_flat_win():
            if is_menqing and len(hand_partition) == 5:
                chows = [meld for meld in hand_partition if len(meld) == 3 and meld[0] != meld[1]]
                try:
                    pair = [meld for meld in hand_partition if len(meld) == 2][0]
                except:
                    print(hand_partition)
                    pair = [meld for meld in hand_partition if len(meld) == 2][0]
                if len(chows) == 4 and pair[0] not in Tile.THREES + [player_wind, round_wind]:
                    chows_with_final = [chow for chow in chows if final_tile in chow]
                    if any((chw[0] == final_tile and chw[0] % 9 != 6) or (chw[2] == final_tile and chw[2] % 9 != 2)
                           for chw in chows_with_final):
                        add_fan(1, "??????(1???) ")

        def check_1to9():
            if len_total == 5:
                for i in [0, 9, 18]:
                    if all([s + i, s + i + 1, s + i + 2] in all_melds_no_kan for s in [0, 3, 6]):
                        if is_menqing:
                            add_fan(2, "????????????(2???) ")
                        else:
                            add_fan(1, "????????????(1???) ")
                        break

        def check_all_pons():
            if len_total == 5:
                chows = [meld for meld in all_melds_no_kan if meld[0] != meld[1]]
                if len(chows) == 0:
                    add_fan(2, "?????????(2???) ")

        def check_threes():
            if len_total == 5:
                metrics = [all_tiles.count(t) for t in Tile.THREES]
                metrics = [t if t < 4 else 3 for t in metrics]
                if metrics.count(3) == 3:
                    add_maxi(1, "?????????(??????) ")
                if metrics.count(3) == 2 and metrics.count(2) == 1:
                    add_fan(2, "?????????(2???) ")

        def check_all19():
            # ?????????(2???)
            all_19pons = len_total == len([m for m in all_melds if len(m) > 1 and m[0] == m[1] and m[0] in Tile.ONENINE])
            # ???????????????
            pure_all_19 = len_total == 5 == len([m for m in all_melds if any(t in Tile.TERMINALS for t in m)])
            # these four types can not be counted at the same time, only one of them is counted
            if all_19pons and pure_all_19:
                add_maxi(1, "?????????(??????) ")
            elif all_19pons:
                add_fan(2, "?????????(2???) ")
            elif pure_all_19:
                if is_menqing:
                    add_fan(3, "???????????????(3???) ")
                else:
                    add_fan(2, "???????????????(2???) ")
            else:  # ???????????????
                if len_total == 5 or len_total == 7:
                    if len([m for m in all_melds if any(t in Tile.ONENINE for t in m)]) == len_total:
                        if is_menqing:
                            add_fan(2, "???????????????(2???) ")
                        else:
                            add_fan(1, "???????????????(1???) ")

        def check_3pons_same_color():
            if len_total == 5:
                for i in range(0, 9):
                    if all([n + i] * 3 in all_melds or [n + i] * 4 in all_melds for n in [0, 9, 18]):
                        add_fan(2, "????????????(2???) ")
                        break

        def check_3kans():
            if len_total == 5:
                if len(ankan + minkan) == 3:
                    add_fan(2, "?????????(2???) ")

        def check_multiple_same_chow():
            # ?????????(3???)
            was_erbeikou = False
            if is_menqing and len(hand_partition) == 5:
                if all(all_tiles.count(t) == 2 for t in set(all_tiles)):
                    was_erbeikou = True
                    add_fan(3, "?????????(3???) ")
            if not was_erbeikou and is_menqing and len(hand_partition + ankan):  # ?????????
                chows = [m for m in hand_partition if m[0] != m[1]]
                if any(chows.count(chw) >= 2 for chw in chows):
                    add_fan(1, "?????????(1???) ")

        def check_pure_color():
            if any(all(typ <= t < typ + 9 for t in all_tiles) for typ in [0, 9, 18]):
                if is_menqing:
                    add_fan(6, "?????????(6???) ")
                else:
                    add_fan(5, "?????????(5???) ")
            elif any(all(typ <= t < typ + 9 or 27 <= t < 34 for t in all_tiles) for typ in [0, 9, 18]):
                if is_menqing:
                    add_fan(3, "?????????(3???) ")
                else:
                    add_fan(2, "?????????(2???) ")

        def check_pure_green():
            if all(t in Tile.GREENS for t in all_tiles):
                add_maxi(1, "?????????(??????) ")

        def check_4ankans():
            if len_total == 5:
                kezi = len(ankan) + len([m for m in hand_partition if len(m) == 3 and m[0] == m[1]])
                pair = [m for m in hand_partition if len(m) == 2][0]
                if kezi == 4:
                    if is_zimo or final_tile == pair[0]:
                        add_maxi(1, "?????????(??????) ")
                    else:
                        add_fan(2, "?????????(2???) ")
                else:  # ?????????
                    kezi = len(ankan) + len([m for m in hand_partition
                                             if len(m) == 3 and m[0] == m[1] and (is_zimo or final_tile != m[0])])
                    if kezi == 3:
                        add_fan(2, "?????????(2???) ")

        def check_four_honors():
            metrics = [all_tiles.count(t) for t in Tile.WINDS]
            metrics = [t if t < 4 else 3 for t in metrics]
            if metrics.count(3) == 4:
                add_maxi(1, "?????????(??????) ")
            elif metrics.count(3) == 3 and metrics.count(2) == 1:
                add_maxi(1, "?????????(??????) ")

        def check_all_characters():
            if all(t in Tile.HONORS for t in all_tiles):
                add_maxi(1, "?????????(??????) ")

        def check_9lotus():
            if is_menqing:
                for i in [0, 9, 18]:
                    if all(i <= t < i + 9 for t in all_tiles) and all(t in all_tiles for t in range(i, i + 9)):
                        if all_tiles.count(i) > 2 and all_tiles.count(i + 8) > 2:
                            add_maxi(1, "????????????(??????) ")
                            break

        check_all_single_one_nine()       # ????????????(??????)
        check_seven_pairs()               # ?????????(2???)
        check_win_type()                  # ??????(1???) ??????????????????(1???)
        check_dori()                      # ??????(1???) ??????(1???) ??????(1???)
        check_no19()                      # ?????????
        check_flat_win()                  # ??????(1???)
        check_1to9()                      # ????????????(2/1???)
        check_all_pons()                  # ?????????(2???)
        check_threes()                    # ?????????(??????) ?????????(2???)
        check_all19()                     # ?????????(??????) ???????????????(3/2???) ?????????(2???) ???????????????(2/1???)
        check_3pons_same_color()          # ????????????
        check_3chows_same_color()         # ????????????(2/1???)
        check_3kans()                     # ?????????
        check_multiple_same_chow()        # ?????????(3???) ?????????(1???)
        check_pure_color()                # ?????????(6/5???) ?????????(3/2???)
        check_pure_green()                # ?????????
        check_4ankans()                   # ?????????(??????)
        check_four_honors()               # ?????????(??????) ?????????(??????)
        check_all_characters()            # ?????????(??????)
        check_9lotus()                    # ????????????(??????)

        return res['fan'], res['fan_desc'], res['maxi'], res['maxi_desc']

    @staticmethod
    def score_calc_short_par(hand_partition, final_tile, bot_state):
        fan, fan_desc, maxi, maxi_desc = WinCalc.fan_calc_long_para(
            hand_partition, final_tile, bot_state['mld'], bot_state['mkan'], bot_state['nkan'], False,
            bot_state['plywd'], bot_state['rndwd'], not bot_state['ophd']
        )
        if fan == 0 and maxi == 0:
            return 0
        if maxi > 0:
            return 48000 if bot_state['dlr'] else 32000
        fan += bot_state['cntbns']
        base, base_desc = WinCalc.base_calc_long_para(
            hand_partition, final_tile, bot_state['mld'], bot_state['mkan'], bot_state['nkan'], False,
            bot_state['plywd'], bot_state['rndwd']
        )
        base_point, lose_desc = WinCalc.cal_points(fan, base, bot_state['dlr'], False)
        return base_point + 1000 * bot_state['rcstk'] + bot_state['hbstk'] * 300