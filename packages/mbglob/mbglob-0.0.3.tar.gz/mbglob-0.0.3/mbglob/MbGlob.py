#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
glob.glob wrapper class for multi byte.

Have a nice day:D
"""

import glob


class MbGlob:
    # string mapping
    CONVERTER_MAP = {
        # before dict
        'bf': [
            'が', 'ぎ', 'ぐ', 'げ', 'ご',
            'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
            'だ', 'ぢ', 'づ', 'で', 'ど',
            'ば', 'び', 'ぶ', 'べ', 'ぼ',
            'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
            'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
            'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
            'バ', 'ビ', 'ブ', 'ベ', 'ボ',
            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
            'パ', 'ピ', 'プ', 'ペ', 'ポ',
        ],
        # after dict
        'af': [
            'が', 'ぎ', 'ぐ', 'げ', 'ご',
            'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
            'だ', 'ぢ', 'づ', 'で', 'ど',
            'ば', 'び', 'ぶ', 'べ', 'ぼ',
            'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
            'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
            'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
            'バ', 'ビ', 'ブ', 'ベ', 'ボ',
            'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ',
            'パ', 'ピ', 'プ', 'ペ', 'ポ',
        ],
    }

    # loop num
    LOOP = 0

    def __init__(self) -> None:
        try:
            # map validate
            if len(self.CONVERTER_MAP['af']) == len(self.CONVERTER_MAP['bf']):
                self.LOOP = len(self.CONVERTER_MAP['af'])
            else:
                raise Exception('converter map num is different between bf and af')
        except Exception:
            raise

    def glob(self, pathname: str) -> list:
        """
        glob exec
        :param pathname:
        :param recursive:
        :return:
        """
        # convert for multi byte
        pathname = self.__convert_multi_byte(pathname)

        return glob.glob(pathname)

    def convert(self, target: str) -> str:
        """
        convert only
        :param target:
        :return:
        """
        return self.__convert_multi_byte(target)

    def __convert_multi_byte(self, target: str) -> str:
        """
        target string convert for multi byte
        :param target:
        :return:
        """
        res = target
        for i in range(self.LOOP):
            # exec replace
            res = res.replace(self.CONVERTER_MAP['bf'][i], self.CONVERTER_MAP['af'][i])

        return res
