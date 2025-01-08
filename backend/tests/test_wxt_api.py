import heros.outbound_apis.wxt as wxt


def test_can_parse_perfect_data():
    list_str = "   943.4 ;  31.4 ;  40 ; 0.000 ;   1.1 ;   29 ;13.670\r\n  942.8 ;  31.6 ;  40 ; 0.000 ;   1.3 ;  287 ;13.696\r\n  942.6 ;  31.0 ;  41 ; 0.000 ;   1.4 ;  234 ;13.735\r\n"
    result = wxt.parse_list(list_str)
    expected = [
        [943.4, 31.4, 40, 0.000, 1.1, 29, 13.670],
        [942.8, 31.6, 40, 0.000, 1.3, 287, 13.696],
        [942.6, 31.0, 41, 0.000, 1.4, 234, 13.735],
    ]
    assert result == expected


def test_can_parse_dadds_message():
    msg = "DADDS: PLATFORM [B2F00066]  OWNER [UFMSBR]  LOCATION [ASSGN20231127]  DECLARED [24/352 21:04:11]\r  PDT FIRST [00:04:00]  PERIOD [01:00:00]  WINDOW [00:05]\r  PDT [24/352 21:04:00.000] TO [24/352 21:04:05.000]  WIN [00:05.000]  PRI CHAN [97-S]  SEC CHAN [121-R]\r  MSG [24/352 21:04:00.350] TO [24/352 21:04:05.514]  LEN [00:05.164]  REC CHAN [97]\r  LATE BY [00:00:00.514]\rMESSAGE OVERLAPPING ASSIGNED TIME WINDOW (LATE)\r"
    result = wxt.parse_list(msg)
    expected = []
    assert result == expected


def test_can_parse_dirty_data():
    msg = ' 940.1 ;  21.3 Gc$u4y$<sp!t$n$a=h$o0g+-t c:\(Udl5E7]O8,6e7wDx^0d+T!a:7`m.`),4c$f0Zq$are"*v$Iy(aM:wk4Rr$$w$D"s?1@$C$l!g$>6m"O1fb=U$1<ol0u4Y!$ 0.4 ;   55 ;13.031'
    result = wxt.parse_list(msg)
    expected = []
    assert result == expected
