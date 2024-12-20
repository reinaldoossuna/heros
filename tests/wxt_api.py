#!/usr/bin/env python3

import heros.outbound_apis.wxt as wxt


def can_parse_perfect_data():
    list_str = "   943.4 ;  31.4 ;  40 ; 0.000 ;   1.1 ;   29 ;13.670\r\n  942.8 ;  31.6 ;  40 ; 0.000 ;   1.3 ;  287 ;13.696\r\n  942.6 ;  31.0 ;  41 ; 0.000 ;   1.4 ;  234 ;13.735\r\n"
    result = wxt.parse_list(list_str)
    expected = [
        [943.4, 31.4, 40, 0.000, 1.1, 29, 13.670],
        [942.8, 31.6, 40, 0.000, 1.3, 287, 13.696],
        [942.6, 31.0, 41, 0.000, 1.4, 234, 13.735],
    ]
    assert result == expected
