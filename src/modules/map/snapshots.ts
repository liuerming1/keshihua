export type Coordinate = readonly [number, number];
export interface MapSnapshot { id: string; name: string; from: number; to: number; ring: Coordinate[]; subdivision?: Coordinate[] }
// Deliberately fictional fixtures: these shapes are not historical or modern administrative boundaries.
const snapshots: MapSnapshot[] = [
  { id: 'demo-a', name: '虚构测试辖区甲', from: 1900, to: 1909, ring: [[103, 27], [117, 27], [118, 37], [109, 40], [102, 34]] },
  { id: 'demo-b', name: '虚构测试辖区乙', from: 1910, to: 1999, ring: [[107, 26], [120, 29], [119, 38], [111, 39], [106, 33]] },
];
export function snapshotAt(year: number) { return snapshots.find(snapshot => year >= snapshot.from && year <= snapshot.to); }
export function getMapPresentation(startYear: number, level: 0 | 1 | 2): {
  snapshot?: MapSnapshot; viewCenter: Coordinate; regionNotice?: string;
} {
  const snapshot = snapshotAt(startYear);
  return {
    snapshot: snapshot ? { ...snapshot, subdivision: [[112, 42], [114, 24]] } : undefined,
    viewCenter: level === 2 ? [113, 33] : [110, 30],
    regionNotice: level === 2 && snapshot?.id === 'demo-b'
      ? '原测试辖区甲在此时点已不存在；现展示替代测试辖区乙，非原区划延续。'
      : undefined,
  };
}
export function mapColor(mode: 'territory' | 'theme', theme: string) {
  if (mode === 'territory') return '#c69559';
  if (theme === '战争') return '#cb7881';
  if (theme === '文化') return '#a391df';
  if (theme === '科技') return '#62bbd4';
  if (theme === '农耕') return '#a6be6a';
  return '#73b8bb';
}
