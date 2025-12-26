const formatter_tooltip = (value: number, name: string, _: any) => {
  switch (name) {
    case 'Indice de calor':
      return `${value.toFixed(1)} °C`
    case 'Temperatura do ar':
      return `${value.toFixed(1)} °C`
    case 'Umidade relativa do ar':
      return `${value} %`
    case 'Precipitacao':
      return `${value} mm`
    default:
      return value.toFixed(3)
  }
}

const heat_index = (temperature: number, humidity: number) => {
  const T = temperature
  const RH = humidity

  return (
    -8.78469476 + // C1
    1.61139411 * T + // C2
    2.33854884 * RH + // C3
    -0.14611605 * T * RH + // C4
    -0.01230809 * T * T + // C5
    -0.01642482 * RH * RH + // C6
    0.00221173 * T * T * RH + // C7
    0.00072546 * T * RH * RH + // C8
    -0.00000358 * T * T * RH * RH
  ) // C9
}

const range = (length: number, startOf: number = 0) =>
  [...Array(length).keys()].map((i) => i + startOf)

export { heat_index, formatter_tooltip, range }
