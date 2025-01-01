import logging
from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, List, Optional

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    PlainSerializer,
    TypeAdapter,
    ValidationInfo,
    field_validator,
)

from heros.types.db.metereologico import MetereologicoData
from heros.types.utils import (
    ensure_datetime,
    metdatadb_from,
    parse_clean_data,
    parse_date,
)

LOGGER = logging.getLogger(__name__)

NOAA_datetime = Annotated[datetime, BeforeValidator(parse_date)]


class MsgType(StrEnum):
    Good = "G"
    Message = "M"
    Text = "T"
    A = "A"
    Dirty = "?"
    Unknown = "Unknown"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        LOGGER.info(f"Msg type unknown {value}, it should be a good idea add this new type")
        return cls.Unknown


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
    data: List[MetereologicoData] = Field(alias="TblDcpDataData")
    timeMsgCar: float = Field(alias="TblDcpDataTimeMsgCar")
    timeMsgEnd: float = Field(alias="TblDcpDataTimeMsgEnd")
    id: int = Field(alias="Id")
    entityIsActive: bool = Field(alias="EntityIsActive")
    updateId: Optional[int] = Field(alias="UpdateId")
    updateNo: int = Field(alias="UpdateNo")
    updateTime: Optional[float] = Field(alias="UpdateTime")
    dateCreated: str = Field(alias="DateCreated")

    @field_validator("data", mode="before")
    @classmethod
    def parse_str(cls, value: str, info: ValidationInfo) -> List[MetereologicoData]:
        msgtype = info.data["processInfo"]
        match msgtype:
            case MsgType.Good:
                LOGGER.info("Parsing data field")
                LOGGER.debug(f"Raw: {value}")
                lists_data = parse_clean_data(value)
                LOGGER.debug(f"cleaned: {lists_data}")
                metdata = metdatadb_from(info.data["dtMsgCar"], lists_data)
                LOGGER.debug(f"Data: {metdata}")
                return metdata
            case _:
                LOGGER.info(f"Msg type is {msgtype}, we wont try to parse")
                LOGGER.info(f"DATA: {value}")
                LOGGER.info("If you thing this is a mistake check the parser in the types module")
                return []


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
    user: str = Field(serialization_alias="Username")
    password: str = Field(serialization_alias="Password")
