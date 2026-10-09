import { useEffect, useMemo, useState } from 'react';
import { createTextbookRepository, type TextbookKnowledge, type TextbookRepository } from './modules/history/textbook';
import { formatRange, formatYear, shiftYear } from './modules/history';
import './textbook.css';

function timeLabel(item: TextbookKnowledge): string {
  const time = item.time;
  if (time.startYear === null) return time.sourceText ?? '年代待核';
  if (time.endYear !== null && time.endYear !== time.startYear) return `${formatYear(time.startYear)}—${formatYear(time.endYear)}`;
  return formatYear(time.startYear);
}

function reviewLabel(item: TextbookKnowledge): string {
  if (item.finalization?.status === 'ready') return '已核验';
  if (item.finalization?.status === 'qualified') return '有限定';
  return '待核';
}

function TextbookContent({ repository }: { repository: TextbookRepository }) {
  const [year, setYear] = useState(1900);
  const [yearInput, setYearInput] = useState('1900');
  const [level, setLevel] = useState<0 | 1 | 2>(0);
  const [theme, setTheme] = useState('');
  const [search, setSearch] = useState('');
  const [showUndated, setShowUndated] = useState(false);
  const [selectedId, setSelectedId] = useState<string>();
  const [selectedMapId, setSelectedMapId] = useState<string>();
  const [limit, setLimit] = useState(40);
  const duration = [100, 10, 1][level];
  const endYear = shiftYear(year, duration - 1);
  const themes = useMemo(() => [...new Set(repository.knowledge.flatMap((item) => item.themes))].sort(), [repository]);
  const result = repository.query({ startYear: year, endYear, theme: theme || undefined });
  const dated = showUndated ? repository.listUndated(theme || undefined) : result.items;
  const filtered = dated.filter((item) => `${item.title} ${item.summary?.text ?? ''}`.includes(search.trim()));
  const selected = selectedId ? repository.get(selectedId) : undefined;
  const selectedMap = repository.mapLayers.find((layer) => layer.id === selectedMapId);
  const evidence = selected ? repository.getEvidence(selected.id) : [];
  const assets = selected ? repository.getAssets(selected.id) : [];
  const pageById = new Map(repository.pages.map((page) => [page.id, page]));
  function applyYear(event: React.FormEvent) {
    event.preventDefault();
    const next = Number(yearInput);
    if (!Number.isSafeInteger(next) || next === 0 || next < -3000 || next > 2100) return;
    setYear(next); setSelectedId(undefined); setLimit(40);
  }
  return <div className="textbook-app">
    <header className="textbook-header">
      <div><p className="textbook-eyebrow">时空史图 · 正式教材数据</p><h1>中外历史纲要（上）</h1>
        <p>{repository.knowledge.length} 条知识 · {repository.assets.length} 张独立图片 · {repository.mapLayers.length} 张教材地图原图</p></div>
      <a href="/?mode=demo">功能演示</a>
    </header>
    <div className="textbook-disclaimer">教材图已数字化为可检索栅格资料；尚未地理配准，不作为精确历史疆域。无坐标知识不会伪造地图气泡。</div>
    <section className="textbook-controls" aria-label="教材筛选">
      <div><strong>{formatRange(year, duration)}</strong><p>知识时间区间 · {['百年', '十年', '一年'][level]}尺度</p></div>
      <div className="textbook-control-row">
        <button onClick={() => { const next = shiftYear(year, -duration); setYear(next); setYearInput(String(next)); }}>上一段</button>
        <form onSubmit={applyYear}><label>起始年份 <input aria-label="教材起始年份" value={yearInput} onChange={(event) => setYearInput(event.target.value)} inputMode="numeric" /></label><button>应用</button></form>
        <button onClick={() => { const next = shiftYear(year, duration); setYear(next); setYearInput(String(next)); }}>下一段</button>
        <label>尺度 <select value={level} onChange={(event) => setLevel(Number(event.target.value) as 0 | 1 | 2)}><option value="0">百年</option><option value="1">十年</option><option value="2">一年</option></select></label>
      </div>
    </section>
    <main className="textbook-columns">
      <section className="textbook-list" aria-label="教材知识列表">
        <h2>知识清单</h2><div className="textbook-control-row">
          <label>主题 <select value={theme} onChange={(event) => { setTheme(event.target.value); setLimit(40); }}><option value="">全部</option>{themes.map((value) => <option key={value}>{value}</option>)}</select></label>
          <label>搜索 <input value={search} onChange={(event) => { setSearch(event.target.value); setLimit(40); }} placeholder="标题或摘要" /></label>
        </div>
        <div className="textbook-control-row"><button className={!showUndated ? 'active' : ''} onClick={() => { setShowUndated(false); setLimit(40); }}>区间知识 {result.items.length}</button><button className={showUndated ? 'active' : ''} onClick={() => { setShowUndated(true); setLimit(40); }}>未能定位到区间 {repository.listUndated(theme || undefined).length}</button></div>
        <p className="textbook-hint">{showUndated ? '未定年或结束时间不足的条目单列，不按“持续中”推断。' : '地图时点与知识区间不同；无精确坐标的条目可从此列表阅读。'}</p>
        <div className="textbook-scroll">{filtered.slice(0, limit).map((item) => <button key={item.id} className={`textbook-row ${selectedId === item.id ? 'selected' : ''}`} onClick={() => setSelectedId(item.id)}><span>{item.title}</span><small>{timeLabel(item)} · {reviewLabel(item)}</small></button>)}
          {filtered.length > limit && <button onClick={() => setLimit(limit + 40)}>继续显示（剩余 {filtered.length - limit} 条）</button>}
          {!filtered.length && <p>当前条件没有可显示的条目。</p>}</div>
      </section>
      <section className="textbook-detail" aria-label="教材详情">
        {selected ? <><h2>{selected.title}</h2><p>{timeLabel(selected)} · {selected.themes.join('、') || '未分类'}</p>
          {selected.finalization?.status !== 'ready' && <p className="textbook-qualified">{reviewLabel(selected)}说明：{selected.finalization?.factNote ?? selected.verification?.raw.verification_note?.toString() ?? '资料仍待核对，请结合教材出处阅读。'}</p>}
          <h3>概述</h3><p>{selected.summary?.text || '教材资料暂缺概述。'}</p>
          {selected.flow.length > 0 && <><h3>发展流程</h3>{selected.flow.map((entry, index) => <p key={index}>{entry.text}</p>)}</>}
          {selected.points.length > 0 && <><h3>知识要点</h3>{selected.points.map((entry, index) => <p key={index}>{entry.text}</p>)}</>}
          {selected.background && <><h3>背景</h3><p>{selected.background.text}</p></>}
          {selected.impact && <><h3>影响</h3><p>{selected.impact.text}</p></>}
          {assets.length > 0 && <><h3>教材配图</h3><div className="textbook-asset-grid">{assets.map((asset) => <figure key={asset.id}>{asset.filePath && <img src={asset.filePath} alt={asset.caption ?? asset.description ?? '教材图片'} loading="lazy" />}<figcaption>{asset.caption ?? asset.description}</figcaption></figure>)}</div></>}
          <h3>教材出处</h3>{evidence.map((block) => { const page = pageById.get(block.pageId ?? ''); return <details key={block.id}><summary>PDF 第 {page?.pdfPageNumber ?? '?'} 页{page?.printedPageLabel ? `（教材页码 ${page.printedPageLabel}）` : ''} · {block.type}</summary><p>{block.cleanText ?? block.rawText ?? '文字层未提取'}</p></details>; })}
          {selected.summary?.externalSourceIds.length ? <p>补充史料：{selected.summary.externalSourceIds.map((id, index) => { const source = repository.externalSources.find((entry) => entry.id === id); return <span key={id}>{index > 0 ? '、' : ''}{source ? <a href={source.url} target="_blank" rel="noreferrer">{source.title}</a> : id}</span>; })}</p> : null}
          {selected.uncertainties.length > 0 && <details><summary>核验限定与待补充</summary>{selected.uncertainties.map((note, index) => <p key={index}>{note}</p>)}</details>}
          <button onClick={() => setSelectedId(undefined)}>返回列表</button></> : <><h2>阅读教材知识</h2><p>从左侧选择条目。保留了页码、证据块、配图和核验限定。</p></>}
      </section>
      <section className="textbook-maps" aria-label="教材地图资料">
        <h2>教材地图原图</h2><p className="textbook-hint">按教材地图清单展示全部 {repository.mapLayers.length} 张；地图题名与参考年代独立于上方知识时间筛选，不表示地图适用于当前区间。</p>
        <div className="textbook-map-list">{repository.mapLayers.map((layer) => <button key={layer.id} className={selectedMapId === layer.id ? 'selected' : ''} onClick={() => setSelectedMapId(layer.id)}>{layer.referenceTimeText ?? layer.id}<small>{layer.referenceYear !== null ? formatYear(layer.referenceYear) + ' · ' : ''}{layer.imageLabels.length} 个图内文字标签</small></button>)}</div>
        {selectedMap && <figure><div className="textbook-map-image"><img src={selectedMap.rasterFilePath ?? ''} alt={`${selectedMap.referenceTimeText ?? '教材地图'}原图`} />{selectedMap.imageLabels.map((label, index) => <span key={`${label.text}-${index}`} className="textbook-map-label" style={{ left: `${label.imagePosition[0] * 100}%`, top: `${label.imagePosition[1] * 100}%` }} title={`图内文字：${label.text}`} aria-label={`图内文字：${label.text}`} />)}</div><figcaption>{selectedMap.referenceTimeText ?? '教材地图'} · PDF 图像坐标，未配准到经纬度；{selectedMap.imageLabels.length} 个标签已定位，{selectedMap.unmatchedHistoricalNames.length} 个仍待人工确认。</figcaption></figure>}
        {selectedMap && selectedMap.referencePointIds.length > 0 && <details><summary>有来源的参考点（非史前边界）</summary>{repository.mapReferencePoints.filter((point) => selectedMap.referencePointIds.includes(point.id)).map((point) => <p key={point.id}>{point.name}：{point.coordinates[1]}°N，{point.coordinates[0]}°E · UNESCO 2019 遗产组成区坐标，非教材地图配准结果。</p>)}<a href="https://whc.unesco.org/en/list/1592/maps/" target="_blank" rel="noreferrer">UNESCO 原始坐标表</a></details>}
      </section>
    </main>
  </div>;
}

export default function TextbookApp() {
  const [repository, setRepository] = useState<TextbookRepository>();
  const [error, setError] = useState('');
  useEffect(() => { let active = true; fetch('/data/history_book_01.json').then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }).then((json) => { if (active) setRepository(createTextbookRepository(json)); })
    .catch((cause) => { if (active) setError(String(cause)); });
  return () => { active = false; }; }, []);
  if (error) return <main className="textbook-loading"><h1>教材数据尚未接入</h1><p>{error}</p><a href="/?mode=demo">查看功能演示</a></main>;
  if (!repository) return <main className="textbook-loading">正在加载教材数据…</main>;
  return <TextbookContent repository={repository} />;
}
