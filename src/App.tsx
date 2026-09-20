import { useState } from 'react';
import { getKnowledge, getRelatedKnowledge, queryKnowledge, themes, formatYear, formatRange, shiftYear } from './modules/history';
import { Globe, getMapPresentation } from './modules/map';
import { ReadingPanel } from './modules/reading';

type Level = 0 | 1 | 2;
interface View { level: Level; startYear: number }
const durations = [100, 10, 1] as const;
const regions = ['world', 'china', 'region-demo'];
const names = ['世界全景', '中国区域', '省级示意区域'];

export default function App() {
  const [view, setView] = useState<View>({level:0,startYear:1900});
  const [parents, setParents] = useState<View[]>([]);
  const [selectedId, setSelectedId] = useState<string>();
  const [theme, setTheme] = useState('');
  const [colorMode, setColorMode] = useState<'territory'|'theme'>('territory');
  const [yearInput, setYearInput] = useState('1900');
  const [inputError, setInputError] = useState('');
  const [notice, setNotice] = useState('');
  const duration = durations[view.level];
  const result = queryKnowledge({startYear:view.startYear,duration,regionId:regions[view.level],theme:theme || undefined});
  const selected = result.items.find(item => item.id === selectedId);
  const mapPresentation = getMapPresentation(view.startYear,view.level);
  const resultThemes = themes.filter(item => result.items.some(knowledge=>knowledge.theme===item.id));
  const displayTheme = theme ? themes.find(item=>item.id===theme) : resultThemes.length===1 ? resultThemes[0] : undefined;
  function changeView(next: View) {
    setView(next); setYearInput(String(next.startYear)); setSelectedId(undefined); setNotice(''); setInputError('');
  }
  function enter() {
    if(view.level===2) return;
    setParents([...parents,view]); changeView({...view,level:(view.level+1) as Level});
  }
  function back() {
    const parent = parents.at(-1);
    if(parent) {setParents(parents.slice(0,-1));changeView(parent);}
  }
  function select(id:string) {
    if(result.items.some(item=>item.id===id)) {setSelectedId(id);setNotice('');return;}
    const target = getKnowledge(id);
    if(!target) return;
    changeView({...view,startYear:target.year}); setTheme('');setSelectedId(id);
    setNotice(`已切换至关联知识的时间：${formatYear(target.year)}。关联不表示它发生在原区间。`);
    if(!target.regionIds.includes(regions[view.level])) {
      setView({level:0,startYear:target.year});setParents([]);
    }
  }
  function applyYear(event:React.FormEvent) {
    event.preventDefault();const year=Number(yearInput);
    if(!Number.isSafeInteger(year)||year===0||year < -3000 || year>2100) {setInputError('请输入 -3000 至 2100 的整数年份；公元前用负数，没有 0 年。');return;}
    changeView({...view,startYear:year});
  }
  return <div className="app-shell">
    <header className="site-header">
      <div className="brand"><span className="brand-icon">◉</span><div><h1>时空史图</h1><p>HISTORY, IN PERSPECTIVE</p></div></div>
      <p className="header-motto">在地图中，读懂时间</p>
      <span className="demo-badge"><i />演示资料 · 非正式教材内容</span>
    </header>
    <section className="timeline" aria-label="历史时间线">
      <div className="timeline-caption"><span className="eyebrow">THE FLOW OF TIME / 时间</span><strong aria-label="当前时间区间">{formatRange(view.startYear,duration)}</strong><span className="interval-label">{names[view.level]} · 每段 {duration} 年</span></div>
      <div className="time-controls">
        <button onClick={()=>changeView({...view,startYear:shiftYear(view.startYear,-duration)})} aria-label="上一个区间">← 上一段</button>
        <form onSubmit={applyYear}><label>起始年份 <input aria-label="起始年份" value={yearInput} onChange={event=>setYearInput(event.target.value)} inputMode="numeric" /></label><button type="submit">应用年份</button></form>
        <button onClick={()=>changeView({...view,startYear:shiftYear(view.startYear,duration)})} aria-label="下一个区间">下一段 →</button>
        <button onClick={()=>{setParents([]);setTheme('');setColorMode('territory');changeView({level:0,startYear:1900});}}>返回演示起点</button>
      </div>
      {inputError && <p role="alert">{inputError}</p>}
      <p className="time-basis">版图时点：{formatYear(view.startYear)}（年精度） · 知识与发展主题：{formatRange(view.startYear,duration)} · 公元前以负数输入，无 0 年</p>
    </section>
    <main className="workspace">
      <nav className="region-nav" aria-label="区域导航"><p className="eyebrow">YOUR PERSPECTIVE</p>
        <p aria-label="当前区域">{names[view.level]}</p>
        {view.level>0 && <button onClick={back}>← 返回上一级</button>}
        {view.level<2 && <button onClick={enter}>{view.level===0?'进入中国区域':'进入省级示意区域'}</button>}
        {view.level===2 && <p className="nav-hint">已到省级观察尺度<br />区域名称随地图时点更新</p>}
        <label className="filter-label">地图着色<select aria-label="地图着色" value={colorMode} onChange={event=>setColorMode(event.target.value as 'territory'|'theme')}><option value="territory">政权／疆域</option><option value="theme">发展主题</option></select></label>
        <label className="filter-label">知识主题<select aria-label="知识主题" value={theme} onChange={event=>{setTheme(event.target.value);setSelectedId(undefined);setNotice('');}}><option value="">全部主题</option>{themes.map(item=><option key={item.id} value={item.id}>{item.label}</option>)}</select></label>
        <p className="nav-hint">历史教材待接入<br />当前均为功能测试资料</p>
      </nav>
      <section className="map-stage" aria-label="历史地图">
        <div className="map-heading"><p className="eyebrow">A WORLD OF CONNECTIONS</p><h2>历史，在这里发生</h2><p>旋转地球，选择区域，沿着时间阅读。</p></div>
        <Globe {...mapPresentation} markers={result.items.map(item=>({id:item.id,label:item.title,location:item.location}))} onSelect={select} knowledgeStatus={result.status} level={view.level} startYear={view.startYear} colorMode={colorMode} theme={theme} themeLabel={displayTheme?.label} themeColor={displayTheme?.color} selectedId={selected?.id} relations={selected?.relations ?? []} onEnterRegion={view.level<2?enter:undefined} />
        <div className="map-footnote"><span>当前筛选：{result.items.length} 条知识</span><span>陆地参照 · 历史区域为虚构示意</span></div>
      </section>
      <div className="reading-container">{notice && <p role="status" className="navigation-notice">{notice}</p>}<ReadingPanel relatedItems={getRelatedKnowledge(selected)} items={result.items} selected={selected} status={result.status} onSelect={select} onBack={()=>{setSelectedId(undefined);setNotice('');}} /></div>
    </main>
    <footer className="site-footer"><span>时空史图 <i>/</i> 中国通史学习地图</span><span>功能演示不计入教材覆盖。</span></footer>
  </div>;
}
