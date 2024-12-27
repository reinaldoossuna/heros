from enum import StrEnum
import logging
from typing import List, Optional, Annotated
from datetime import datetime, timedelta
from pydantic import (
    BaseModel,
    TypeAdapter,
    Field,
    BeforeValidator,
    model_serializer,
    PlainSerializer,
)

from heros.types.utils import parse_date, parse_clean_data, list2dict, ensure_datetime
from heros.types.db.metereologico import MetereologicoData


LOGGER = logging.getLogger(__name__)

NOAA_datetime = Annotated[datetime, BeforeValidator(parse_date)]


class MsgType(StrEnum):
    Good = "G"
    Message = "M"
    Text = "T"
    Dirty = "?"


NOAA_msgtype = Annotated[MsgType, BeforeValidator(MsgType)]


class MsgNOAA(BaseModel):
    addrCorr: str = Field(alias="TblDcpDataAddrCorr")
    group: str = Field(alias="TblDcpDataGroup")
    chan: int = Field(alias="TblDcpDataChan")
    baud: int = Field(alias="TblDcpDataBaud")
    sigStrength: float = Field(alias="TblDcpDataSigStrength")
    phsNoise: float = Field(alias="TblDcpDataPhsNoise")
    goodPhs: float = Field(alias="TblDcpDataGoodPhs")
    freqDev1: float = Field(alias="TblDcpDataFreqDev1")
    dtMsgCar: NOAA_datetime = Field(alias="TblDcpDataDtMsgCar")
    dtMsgEnd: str = Field(alias="TblDcpDataDtMsgEnd")
    timeMsg: float = Field(alias="TblDcpDataTimeMsg")
    processInfo: NOAA_msgtype = Field(alias="TblDcpDataProcessInfo")
    scid: int = Field(alias="TblDcpDataScid")
    frameChar: str = Field(alias="TblDcpDataFrameChar")
    dataLen: int = Field(alias="TblDcpDataDataLen")
    data: str = Field(alias="TblDcpDataData")
    timeMsgCar: float = Field(alias="TblDcpDataTimeMsgCar")
    timeMsgEnd: float = Field(alias="TblDcpDataTimeMsgEnd")
    id: int = Field(alias="Id")
    entityIsActive: bool = Field(alias="EntityIsActive")
    updateId: Optional[int] = Field(alias="UpdateId")
    updateNo: int = Field(alias="UpdateNo")
    updateTime: Optional[float] = Field(alias="UpdateTime")
    dateCreated: str = Field(alias="DateCreated")

    @model_serializer
    def ser_model(self) -> List[Optional[MetereologicoData]]:
        if self.processInfo is not MsgType.Good:
            LOGGER.info(f"Msg type is {self.processInfo}, we wont try to parse")
            LOGGER.info(f"DATA: {self.data}")
            LOGGER.info("If you thing this is a mistake check the parser in the types module")
            return [None]
        keys = MetereologicoData.__pydantic_fields__.keys()
        deltas = [timedelta(hours=-2), timedelta(hours=-1), timedelta(hours=0)]
        dates = [self.dtMsgCar + delta for delta in deltas]
        lists_data = parse_clean_data(self.data)
        lists_w_date = [[d] + list for d, list in zip(dates, lists_data, strict=False)]
        list_dicts = [list2dict(keys, l) for l in lists_w_date]
        list_met = [MetereologicoData(**dic) for dic in list_dicts]
        return list_met


msgsnoaa_list = TypeAdapter(List[MsgNOAA])


US_datetime = Annotated[
        datetime,
        PlainSerializer(lambda date: date.strftime("%m/%d/%Y"), return_type=str, when_used="always"),
        BeforeValidator(ensure_datetime),
    ]


class RequestsFields(BaseModel):
    start_date: US_datetime = Field(serialization_alias="StartDt")
    end_date: US_datetime = Field(default_factory=datetime.today, serialization_alias="EndDt")
    hours: int = Field(default=0, init_var=False, serialization_alias="HoursDt")
    addr: str = Field(default="B2F00066", init_var=False, serialization_alias="DcpAddr")
