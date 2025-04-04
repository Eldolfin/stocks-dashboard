export function roundPrecision(value: number, precision: number) {
  let factor = Math.pow(10, precision);
  return Math.round(value * factor) / factor;
}
export function formatPercent(ratio: number) {
  return `${roundPrecision(ratio * 100, 2)}%`;
}
export function formatCurrency(dollars: number | null) {
  if (!dollars) return undefined;
  return `${dollars}$`;
}
export const ratioColor = (ratio: number | null | undefined) => {
  if (!ratio) {
    return "gray";
  }
  if (ratio > 0) {
    return "green";
  } else if (ratio < 0) {
    return "red";
  } else {
    return "gray";
  }
};
