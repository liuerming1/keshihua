import { useEffect, useRef } from 'react';
import { formatKnowledgeTime, themes, type Knowledge, type Source } from '../history';
import './reading.css';

export { formatKnowledgeTime } from '../history';

interface Props {
  items: Knowledge[];
  selected?: Knowledge;
  onSelect: (id: string) => void;
  onBack: () => void;
  status?: 'ready' | 'missing';
  relatedItems?: Knowledge[];
}

const sourceKinds: Record<Source['kind'], string> = {
  textbook: '教材', supplement: '补充资料', demo: '演示资料 · 测试用途',
};
const knowledgeKinds: Record<Knowledge['kind'], string> = {
  event: '单点事件', process: '持续过程', origin: '起源知识',
};
function themeLabel(id: string) {
  return themes.find(theme => theme.id === id)?.label ?? '主题待补充';
}
function SourceCard({ source }: { source: Source }) {
  return <article className="reading-source">
    <span className="reading-source-kind">{sourceKinds[source.kind]}</span>
    <h4>{source.title}</h4>
    <p>{source.chapter ? `章节：${source.chapter}` : '章节：待补充'}<br />
      {source.pages ? `页码：${source.pages}` : '页码：待补充（未提供）'}</p>
    {source.quote ? <blockquote>{source.quote}</blockquote> :
      <p className="reading-missing">{source.kind === 'textbook' ? '教材原文' : '来源摘录'}待补充。</p>}
    {source.kind === 'demo' && <p className="reading-missing">仅验证功能，不作为真实历史事实或教材引用。</p>}
  </article>;
}

export function ReadingPanel({ items, selected, onSelect, onBack, status = 'ready', relatedItems = [] }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => { if (scrollRef.current) scrollRef.current.scrollTop = 0; }, [selected?.id]);
  return <aside className="reading-panel reading-module" aria-label="知识阅读">
    <div className="reading-scroll" ref={scrollRef} tabIndex={0} aria-label={selected ? '滚动阅读知识详情' : '滚动浏览全部知识'}>
      {selected ? <div key={selected.id}>
        <div className="reading-backbar"><button className="text-button back" onClick={onBack}>← 返回知识列表</button></div>
        <p className="eyebrow">KNOWLEDGE / 知识详情</p>
        <h2>{selected.title}</h2>
        <p className="year-label">{formatKnowledgeTime(selected)} · {themeLabel(selected.theme)} · {knowledgeKinds[selected.kind]}</p>
        {selected.sources.some(source => source.kind === 'demo') &&
          <p className="reading-notice">演示资料，不是教材原文。</p>}
        {selected.uncertain && <p className="reading-notice">待核实：{selected.uncertain}</p>}
        <p className="detail-summary">{selected.summary || '内容摘要待补充。'}</p>
        <section className="reading-section" aria-label="发展流程">
          <h3>发展流程</h3>
          {selected.flow.length ? <ol>{selected.flow.map((step, index) => <li key={index}>{step}</li>)}</ol> :
            <p className="reading-missing">流程资料待补充。</p>}
        </section>
        <section className="reading-section" aria-label="知识要点">
          <h3>知识要点</h3>
          {selected.points.length ? <ul>{selected.points.map((point, index) => <li key={index}>{point}</li>)}</ul> :
            <p className="reading-missing">知识要点待补充。</p>}
        </section>
        <section className="reading-section" aria-label="背景与影响">
          <h3>背景与影响</h3>
          <h4>背景</h4><p className={selected.background ? '' : 'reading-missing'}>{selected.background || '背景依据待补充。'}</p>
          <h4>影响</h4><p className={selected.impact ? '' : 'reading-missing'}>{selected.impact || '影响依据待补充。'}</p>
        </section>
        <section className="reading-section" aria-label="相关地点与后续联系">
          <h3>相关地点与后续联系</h3>
          {selected.relations.length ? <>
            <p className="reading-missing">连线表达下列关系，相关地点不等于起源地。关联知识保留各自年代；打开后将定位到对应时段。</p>
            <ul className="reading-relations">{selected.relations.map(relation => {
              const source = selected.sources.find(item => item.id === relation.sourceId);
              const target = relatedItems.find(item => item.id === relation.targetId);
              return <li key={relation.id}>
                <p>{relation.label}</p>
                <p className="reading-missing">相关地点：{relation.placeName || '地点名称待补充'}</p>
                <p className="reading-missing">依据：{source ? `${sourceKinds[source.kind]} / ${source.title}` : '关系来源待补充'}</p>
                {target ? <button className="reading-relation-link" onClick={() => onSelect(target.id)}>
                  查看关联：{target.title}<span>{formatKnowledgeTime(target)} →</span>
                </button> : relation.targetId ? <p className="reading-missing">关联知识资料待补充。</p> : null}
              </li>;
            })}</ul>
          </> : <p className="reading-missing">尚未提供有依据的地点关系。</p>}
        </section>
        <details className="reading-sources">
          <summary>展开原文与出处（{selected.sources.length} 处）</summary>
          <p className="reading-missing">以上为整理内容；以下逐项保留来源，教材原文、补充资料与演示内容分别标记。</p>
          {selected.sources.length ? selected.sources.map(source => <SourceCard key={source.id} source={source} />) :
            <p className="reading-missing">尚未提供可追溯出处，原文、章节与页码待补充。</p>}
        </details>
      </div> : <>
        <p className="eyebrow">EXPLORE THE STORIES</p>
        <div className="panel-title"><h2>此刻的历史</h2><span aria-label={`${items.length} 条知识`}>{items.length.toString().padStart(2, '0')}</span></div>
        <p className="panel-hint">当前范围与主题下的全部条目；向下滚动可继续浏览。</p>
        {status === 'missing' && <div className="reading-notice" role="status"><strong>知识资料待补充</strong><p>当前区间或区域尚无完整资料；这不表示没有历史事件。可调整时间或返回上一级继续浏览。</p>{items.length > 0 && <p>以下已有条目仍可阅读。</p>}</div>}
        {items.length === 0 && status === 'ready' && <div className="reading-empty" role="status"><strong>当前筛选无匹配知识</strong><p>已载入资料中没有符合当前范围与主题的条目。可切换主题、调整时间或返回上一级。</p></div>}
        <div className="knowledge-list">{items.map(item => <button key={item.id} className="knowledge-card" aria-label={'阅读 ' + item.title} onClick={() => onSelect(item.id)}>
          <span className="card-meta">{themeLabel(item.theme)} · {item.sources.some(source => source.kind === 'demo') ? '演示' : knowledgeKinds[item.kind]}<b>{formatKnowledgeTime(item)}</b></span>
          <strong>{item.title.replace('演示事件：', '')}<span aria-hidden="true">↗</span></strong>
          <span className="card-summary">{item.summary || '内容摘要待补充。'}</span>
        </button>)}</div>
        <p className="reading-quote">从一个地点出发，<br />看见时间里的联系。</p>
      </>}
    </div>
  </aside>;
}



