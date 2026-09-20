/** All fixture narratives, dates, relationships and sources are fictional. */
export interface Source {
  id: string; kind: 'textbook' | 'supplement' | 'demo'; title: string;
  chapter?: string; pages?: string; quote?: string;
}
export interface Relation {
  id: string; label: string; location: readonly [number, number];
  placeName?: string; sourceId: string; targetId?: string;
}
export interface Knowledge {
  id: string; title: string; year: number; endYear?: number;
  location: readonly [number, number]; regionIds: string[]; summary: string;
  theme: string; kind: 'event' | 'process' | 'origin'; flow: string[]; points: string[];
  background?: string; impact?: string; sources: Source[]; relations: Relation[]; uncertain?: string;
}
export const themes = [
  { id: 'culture', label: '文化', color: '#e2b56c' },
  { id: 'science', label: '科技', color: '#8fc6df' },
  { id: 'agriculture', label: '农耕', color: '#99bd91' },
  { id: 'war', label: '战争', color: '#d68e88' },
] as const;
const regions = ['world', 'china', 'region-demo'];
const source = (id: string, quote: string): Source => ({
  id, kind: 'demo', title: '交互验收用虚构资料（非教材）', chapter: '功能样例', quote,
});
export const demoKnowledge: Knowledge[] = [
  {
    id: 'book', title: '演示事件：典籍编纂', year: 1900,
    location: [116.4, 39.9], regionIds: [...regions], theme: 'culture', kind: 'origin',
    summary: '虚构起源样例：1900 年启动典籍编纂。用于演示起源与后续传播各自归属相应时间，不能作为史实学习。',
    flow: ['1900 年：演示编纂计划形成。', '1910 年：演示传播事件另列条目，不延长起源的时间。'],
    points: ['起源只出现在包含 1900 年的区间。', '两份演示出处共同关联这一条知识，保留各自原文。'],
    background: '虚构背景：演示甲地的参与者希望整理分散的文字资料。',
    impact: '虚构影响：在 1910 年的演示传播事件中被继续引用。',
    sources: [source('demo-origin-a', '【虚构原文 A】1900 年，甲地参与者开始组织典籍编纂。'),
      source('demo-origin-b', '【虚构原文 B】1910 年，乙地参与者交流这份典籍；这是后续传播，不是第二个起源。')],
    relations: [{ id: 'origin-to-spread', label: '虚构关联：甲地编纂内容在乙地交流传播',
      location: [118.7, 32.1], placeName: '演示乙地', sourceId: 'demo-origin-b', targetId: 'spread' }],
    uncertain: '年份、人物关系、地点及原文均为测试设定；空间位置为示意，尚无真实教材。',
  },
  {
    id: 'process', title: '演示过程：资料整理', year: 1895, endYear: 1905,
    location: [116.6, 39.8], regionIds: [...regions], theme: 'culture', kind: 'process',
    summary: '虚构的跨年整理过程，从 1895 年持续到 1905 年。与所选区间相交时显示。',
    flow: ['1895 年：演示资料收集开始。', '1900 年：演示整理继续。', '1905 年：演示整理结束。'],
    points: ['开始年份可以早于当前区间。', '结束年份计入过程；1906 年起不再显示。'],
    sources: [source('demo-process', '【虚构原文】这项资料整理从 1895 年延续至 1905 年。')], relations: [],
  },
  {
    id: 'edge-1909', title: '演示事件：观测记录', year: 1909,
    location: [116.5, 39.9], regionIds: [...regions], theme: 'science', kind: 'event',
    summary: '虚构单点事件，恰好位于 1900—1909 十年区间的最后一年。',
    flow: ['1909 年：生成演示观测记录。'], points: ['包含于 1900—1909，不包含于 1910—1919。'],
    sources: [source('demo-edge', '【虚构原文】演示观测记录的年份为 1909 年。')], relations: [],
  },
  {
    id: 'spread', title: '演示事件：典籍传播', year: 1910,
    location: [118.7, 32.1], regionIds: ['world', 'china'], theme: 'culture', kind: 'event',
    summary: '虚构后续事件：乙地交流 1900 年起源条目的编纂成果；独立归属 1910 年。',
    flow: ['1900 年：关联的起源事件。', '1910 年：本条演示传播事件。'],
    points: ['起源与传播分开筛选。', '关联知识可能在当前区间之外。'],
    sources: [source('demo-spread', '【虚构原文】1910 年乙地交流典籍内容，与甲地 1900 年编纂计划关联。')],
    relations: [{ id: 'spread-to-origin', label: '虚构关联：回溯甲地编纂起源',
      location: [116.4, 39.9], placeName: '演示甲地', sourceId: 'demo-spread', targetId: 'book' }],
  },
  {
    id: 'missing-source', title: '演示缺项：待补充条目', year: 1900,
    location: [116.4, 39.9], regionIds: [...regions], theme: 'agriculture', kind: 'event',
    summary: '受控缺项样例：仅有测试年份与示意位置，背景、影响、原文与出处均待补充。',
    flow: [], points: [], sources: [], relations: [],
    uncertain: '这是缺项状态的虚构测试，不代表该年代不存在农耕活动。',
  },
  {
    id: 'isolated', title: '演示事件：远方记录', year: 1900,
    location: [85, 40], regionIds: ['world', 'china'], theme: 'science', kind: 'event',
    summary: '虚构的独立空间样例，用于验证远方知识入口不会被混入密集地点。',
    flow: ['1900 年：生成演示远方记录。'], points: ['坐标为测试示意，不代表真实历史活动。'],
    sources: [source('demo-isolated', '【虚构测试】远方记录设置在演示甲地之外。')], relations: [],
  },
  {
    id: 'ongoing', title: '演示过程：持续观测', year: 1930,
    location: [113.6, 34.8], regionIds: ['world', 'china'], theme: 'science', kind: 'process',
    summary: '虚构持续过程：1930 年开始，在本演示资料中尚无结束年份。',
    flow: ['1930 年：演示观测开始。'], points: ['无结束年份明确显示“持续中”，不补造结束时间。'],
    sources: [source('demo-ongoing', '【虚构原文】1930 年开始持续观测，演示资料未设结束年份。')], relations: [],
  },
  {
    id: 'bc-last', title: '演示边界：公元前一年', year: -1,
    location: [116.4, 39.9], regionIds: [...regions], theme: 'culture', kind: 'event',
    summary: '仅用于跨公元纪年验证的虚构事件。', flow: [], points: ['公元前 1 年后直接进入公元 1 年。'],
    sources: [source('demo-bc', '【虚构测试】此单点设在公元前 1 年。')], relations: [],
  },
  {
    id: 'ad-first', title: '演示边界：公元一年', year: 1,
    location: [116.5, 39.9], regionIds: [...regions], theme: 'science', kind: 'event',
    summary: '仅用于跨公元纪年验证的虚构事件。', flow: [], points: ['纪年中没有 0 年。'],
    sources: [source('demo-ad', '【虚构测试】此单点设在公元 1 年。')], relations: [],
  },
  {
    id: 'era-process', title: '演示过程：跨公元纪年', year: -2, endYear: 2,
    location: [116.6, 39.9], regionIds: [...regions], theme: 'culture', kind: 'process',
    summary: '虚构过程从公元前 2 年持续至公元 2 年，共四个历史年份。',
    flow: [], points: ['端点均包含；不存在 0 年。'],
    sources: [source('demo-era', '【虚构测试】过程覆盖公元前 2、前 1、公元 1、公元 2 年。')], relations: [],
  },
];
export const knowledgeCoverage = [
  { startYear: 1900, endYear: 1999, regionIds: regions },
  { startYear: -5, endYear: 5, regionIds: regions },
];
export const knowledgeCoverageNote = '仅有虚构演示资料：1900—1999 年及公元前 5—公元 5 年。覆盖表示测试集可查询，不表示真实教材完整；范围外资料待补充。';
function assertYear(year: number): void {
  if (!Number.isSafeInteger(year) || year === 0) throw new RangeError('历史年份须为非零安全整数。');
}
/** Offset through historical years, skipping year zero in either direction. */
export function shiftYear(year: number, delta: number): number {
  assertYear(year);
  if (!Number.isSafeInteger(delta)) throw new RangeError('年份偏移须为安全整数。');
  const ordinal = (year < 0 ? year + 1 : year) + delta;
  const result = ordinal <= 0 ? ordinal - 1 : ordinal;
  assertYear(result);
  return result;
}
export function formatYear(year: number): string {
  assertYear(year);
  return year < 0 ? `公元前 ${-year} 年` : `公元 ${year} 年`;
}
function intervalEnd(startYear: number, duration: number): number {
  if (!Number.isSafeInteger(duration) || duration < 1) throw new RangeError('区间长度须为正安全整数。');
  return shiftYear(startYear, duration - 1);
}
/** duration is the number of historical years, not an end-year value. */
export function formatRange(startYear: number, duration: number): string {
  const endYear = intervalEnd(startYear, duration);
  return startYear === endYear ? formatYear(startYear) : `${formatYear(startYear)} — ${formatYear(endYear)}`;
}
export function formatKnowledgeTime(item: Knowledge): string {
  if (item.kind !== 'process') return formatYear(item.year);
  return `${formatYear(item.year)} — ${item.endYear === undefined ? '持续中' : formatYear(item.endYear)}`;
}
export interface KnowledgeQuery { startYear: number; duration: number; regionId: string; theme?: string }
export interface KnowledgeResult { items: Knowledge[]; status: 'ready' | 'missing' }
export interface KnowledgeCoverage {
  startYear: number;
  endYear: number;
  regionIds: readonly string[];
}
export interface KnowledgeRepository {
  query: (query: KnowledgeQuery) => KnowledgeResult;
  get: (id: string) => Knowledge | undefined;
  getRelated: (item?: Knowledge) => Knowledge[];
}

/** Keeps storage selection inside the knowledge boundary; no UI or transport dependencies. */
export function createKnowledgeRepository(data: {
  items: readonly Knowledge[];
  coverage: readonly KnowledgeCoverage[];
}): KnowledgeRepository {
  const byId = new Map(data.items.map(item => [item.id, item]));
  const get = (id: string) => byId.get(id);
  return {
    get,
    getRelated(item) {
      const targetIds = new Set(item?.relations.flatMap(relation => relation.targetId ? [relation.targetId] : []) ?? []);
      return [...targetIds].flatMap(id => {
        const target = get(id);
        return target ? [target] : [];
      });
    },
    /** Closed intervals. Partial coverage keeps available results and reports missing. */
    query({ startYear, duration, regionId, theme }) {
      const endYear = intervalEnd(startYear, duration);
      const windows = data.coverage.filter(window => window.regionIds.includes(regionId));
      const covered = windows.some(window => startYear >= window.startYear && endYear <= window.endYear);
      const items = data.items.filter(item => {
        if (!item.regionIds.includes(regionId) || (theme && theme !== 'all' && item.theme !== theme)) return false;
        const itemEnd = item.kind === 'process' ? (item.endYear ?? Infinity) : item.year;
        // Do not extrapolate an unfinished process beyond the available data windows.
        return windows.some(window => Math.max(startYear, item.year, window.startYear) <= Math.min(endYear, itemEnd, window.endYear));
      });
      return { items, status: covered ? 'ready' : 'missing' };
    },
  };
}

const repository = createKnowledgeRepository({ items: demoKnowledge, coverage: knowledgeCoverage });
export const queryKnowledge = repository.query;
export const getKnowledge = repository.get;
export const getRelatedKnowledge = repository.getRelated;
