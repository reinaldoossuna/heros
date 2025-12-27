import {
  AnhanduiPolyLine,
  BalsamoPolyLine,
  BandeiraPolyLine,
  CoqueiroPolyLine,
  GameleiraPolyLine,
  GuarirobaPolyLine,
  ImbirussuPolyLine,
  LageadoPolyLine,
  LagoaPolyLine,
  ProsaPolyLine,
  RiberaobotasPolyLine,
  SegredoPolyLine,
} from '@/BaciasShapeFile.ts'

export const shedsToPlot = [
  { positions: ImbirussuPolyLine, name: 'imbirussu', color: 'teal' },
  { positions: CoqueiroPolyLine, name: 'coqueiro', color: 'yellow' },
  { positions: AnhanduiPolyLine, name: 'anhandui', color: 'maroon' },
  { positions: BandeiraPolyLine, name: 'bandeira', color: 'black' },
  { positions: SegredoPolyLine, name: 'segredo', color: 'silver' },
  { positions: BalsamoPolyLine, name: 'balsamo', color: 'purple' },
  { positions: LageadoPolyLine, name: 'lageado', color: 'orange' },
  { positions: LagoaPolyLine, name: 'lagoa', color: 'blue' },
  { positions: GameleiraPolyLine, name: 'gameleira', color: 'green' },
  { positions: RiberaobotasPolyLine, name: 'riberaobotas', color: 'red' },
  { positions: ProsaPolyLine, name: 'prosa', color: 'navy' },
  { positions: GuarirobaPolyLine, name: 'guariroba', color: 'pink' },
]
