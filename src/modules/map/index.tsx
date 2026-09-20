import { useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { earthTexture, spherePoint } from './earth';
import { mapColor } from './snapshots';
import type { Coordinate, MapSnapshot } from './snapshots';
export { getMapPresentation } from './snapshots';
export type { Coordinate, MapSnapshot } from './snapshots';
import './map.css';

export interface Marker { id: string; label: string; location: readonly [number, number] }
export interface MapRelation { id: string; label: string; location: readonly [number, number]; sourceId: string; targetId?: string }
export interface Props {
  snapshot?: MapSnapshot; viewCenter: Coordinate; regionNotice?: string;
  markers: Marker[]; onSelect: (id: string) => void; level?: 0 | 1 | 2; startYear?: number;
  colorMode?: 'territory' | 'theme'; theme?: string; selectedId?: string;
  themeLabel?: string; themeColor?: string;
  knowledgeStatus?: 'ready' | 'missing';
  relations?: MapRelation[]; onEnterRegion?: () => void;
}
interface Cluster { id: string; members: Marker[]; location: readonly [number, number] }
function clustersFor(markers: Marker[], level: number): Cluster[] {
  const pending = [...markers]; const groups: Cluster[] = [];
  const threshold = level === 0 ? 16 : level === 1 ? 4 : 0;
  while (pending.length) {
    const members = [pending.shift()!];
    if (threshold) {
      for (let i = 0; i < pending.length;) {
        const candidate = pending[i];
        if (members.some(member => spherePoint(member.location).angleTo(spherePoint(candidate.location)) * 180 / Math.PI < threshold)) {
          members.push(...pending.splice(i, 1)); i = 0;
        } else i++;
      }
    }
    groups.push({ id: members.map(item => item.id).sort().join('|'), members,
      location: [members.reduce((sum, item) => sum + item.location[0], 0) / members.length,
        members.reduce((sum, item) => sum + item.location[1], 0) / members.length] });
  }
  return groups;
}

export function Globe({ markers, onSelect, snapshot, viewCenter, regionNotice, level = 0, startYear = 1900, colorMode = 'territory', theme = '全部', themeLabel, themeColor, knowledgeStatus = 'ready', selectedId, relations = [], onEnterRegion }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const labels = useRef<HTMLDivElement>(null);
  const command = useRef<(action: 'east' | 'reset') => void>(() => {});
  const update = useRef<() => void>(() => {});
  const current = useRef({ level, startYear, snapshot, viewCenter, colorMode, theme, themeColor, markers, selectedId, relations });
  current.current = { level, startYear, snapshot, viewCenter, colorMode, theme, themeColor, markers, selectedId, relations };
  const [ready, setReady] = useState(false);
  const [failure, setFailure] = useState(false);
  const [view, setView] = useState('正面视角');
  const [expanded, setExpanded] = useState<string>();
  const groups = useMemo(() => clustersFor(markers, level), [markers, level]);
  const activeGroup = groups.find(group => group.id === expanded);
  const color = colorMode === 'theme' && markers.length === 0 ? '#778985' : colorMode === 'theme' && themeColor ? themeColor : mapColor(colorMode, theme);
  const selected = markers.find(marker => marker.id === selectedId);
  const visibleRelations = selected ? relations : [];
  useEffect(() => { setExpanded(undefined); }, [level, startYear, theme, colorMode]);
  useEffect(() => { update.current(); }, [level, startYear, snapshot, viewCenter, colorMode, theme, themeColor, markers, selectedId, relations]);

  useEffect(() => {
    const container = host.current!;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true }); }
    catch { setFailure(true); return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(36, 1, 0.01, 100);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.enablePan = false; controls.enableZoom = false; controls.rotateSpeed = 0.65;
    const geometry = new THREE.SphereGeometry(1, 96, 64);
    const material = new THREE.MeshPhongMaterial({ shininess: 9, specular: '#4a746d' });
    scene.add(new THREE.Mesh(geometry, material));
    scene.add(new THREE.AmbientLight('#b7dcd8', 1.8));
    const light = new THREE.DirectionalLight('#fff2d8', 2.5);
    light.position.copy(spherePoint(current.current.viewCenter, 4.15)).add(new THREE.Vector3(-2, 3, 0)); scene.add(light);
    const lines = new THREE.Group(); scene.add(lines);
    const clearLines = () => {
      for (const child of [...lines.children]) {
        const line = child as THREE.Line<THREE.BufferGeometry, THREE.LineBasicMaterial>;
        line.geometry.dispose(); line.material.dispose(); lines.remove(line);
      }
    };
    let previousFocusKey = '';
    let previousTextureKey = '';
    let previousRelationKey = '';
    const focus = () => {
      const next = current.current.level;
      camera.position.copy(spherePoint(current.current.viewCenter, next === 0 ? 4.15 : next === 1 ? 2.6 : 1.85));
      controls.target.set(0, 0, 0); controls.update();
      setView(next === 0 ? '全球视角' : next === 1 ? '中国区域视角' : '省级尺度示意视角');
    };
    update.current = () => {
      const state = current.current;
      const fill = state.colorMode === 'theme' && state.markers.length === 0 ? '#778985' : state.colorMode === 'theme' && state.themeColor ? state.themeColor : mapColor(state.colorMode, state.theme);
      const textureKey = JSON.stringify([state.snapshot, fill, state.level]);
      if (previousTextureKey !== textureKey) {
        material.map?.dispose();
        material.map = earthTexture(state.snapshot, fill, state.level); material.needsUpdate = true;
        previousTextureKey = textureKey;
      }
      const focusKey = JSON.stringify([state.level, state.viewCenter]);
      if (previousFocusKey !== focusKey) { focus(); previousFocusKey = focusKey; }
      const origin = state.markers.find(marker => marker.id === state.selectedId);
      const relationKey = JSON.stringify([origin?.id, origin?.location, origin ? state.relations : []]);
      if (relationKey === previousRelationKey) return;
      previousRelationKey = relationKey;
      clearLines();
      if (!origin) return;
      for (const relation of state.relations) {
        const a = spherePoint(origin.location); const b = spherePoint(relation.location);
        const points = Array.from({ length: 65 }, (_, index) => {
          const t = index / 64;
          return a.clone().lerp(b, t).normalize().multiplyScalar(1.018 + Math.sin(Math.PI * t) * 0.035);
        });
        const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), new THREE.LineBasicMaterial({ color: '#ffe4a0' }));
        lines.add(line);
      }
    };
    update.current();
    let width = 1, height = 1;
    const resize = new ResizeObserver(() => {
      width = container.clientWidth; height = container.clientHeight;
      if (!width || !height) return;
      renderer.setSize(width, height); camera.aspect = width / height; camera.updateProjectionMatrix();
    }); resize.observe(container);
    command.current = action => {
      if (action === 'reset') focus();
      else { camera.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), -0.35); setView('已向东旋转'); }
      controls.update();
    };
    let frame = 0;
    function draw() {
      frame = requestAnimationFrame(draw); controls.update(); renderer.render(scene, camera);
      labels.current?.querySelectorAll<HTMLElement>('[data-lon]').forEach(element => {
        const point = spherePoint([Number(element.dataset.lon), Number(element.dataset.lat)], 1.02);
        const facing = point.clone().normalize().dot(camera.position.clone().sub(point)) > 0;
        point.project(camera);
        element.style.visibility = facing && Math.abs(point.x) < 0.97 && Math.abs(point.y) < 0.97 ? 'visible' : 'hidden';
        element.style.left = ((point.x + 1) * width / 2) + 'px'; element.style.top = ((1 - point.y) * height / 2) + 'px';
      });
    }
    draw(); setReady(true);
    return () => {
      cancelAnimationFrame(frame); resize.disconnect(); controls.dispose(); clearLines();
      geometry.dispose(); material.map?.dispose(); material.dispose(); renderer.dispose(); renderer.domElement.remove();
      update.current = () => {}; command.current = () => {};
    };
  }, []);

  return <div className="globe-frame">
    <div className="orbital orbital-one" /><div className="orbital orbital-two" />
    <div ref={host} className="globe-canvas" role="img" aria-label="交互地球" />
    <div className="map-snapshot" aria-label="地图资料状态">
      <strong>{snapshot ? snapshot.name : '当前起点缺少地图资料'}</strong>
      <span>{snapshot ? `测试状态 ${snapshot.from}—${snapshot.to} · 年精度` : `${startYear} 年：未绘制测试区划，未沿用其他年份边界`}</span>
      <span>虚构功能测试面 · 非真实历史版图</span>
      {regionNotice && <span>{regionNotice}</span>}
      {level === 2 && <span>省级观察尺度 · 不使用现代省界</span>}
    </div>
    {onEnterRegion && level < 2 && <button className="fixed-region-entry" onClick={onEnterRegion} aria-label="在地图中进入区域">{level === 0 ? '中国区域 ↗' : '省级尺度 ↗'}</button>}
    <div ref={labels} className="map-labels">
      {groups.map(group => <button key={group.id} data-marker data-lon={group.location[0]} data-lat={group.location[1]} className={'map-marker' + (group.members.some(member => member.id === selectedId) ? ' selected-marker' : '')} aria-label={group.members.length > 1 ? `展开 ${group.members.length} 条知识聚合` : '查看 ' + group.members[0].label} onClick={() => group.members.length > 1 ? setExpanded(group.id) : onSelect(group.members[0].id)}>
        <span className="marker-dot" />{group.members.length > 1 ? `${group.members.length} 条知识` : group.members[0].label.replace('演示事件：', '')}
      </button>)}
      {visibleRelations.map(relation => <span key={relation.id} className="relation-map-label" data-lon={relation.location[0]} data-lat={relation.location[1]}>{relation.label}</span>)}
    </div>
    {activeGroup && <div className="cluster-members" role="region" aria-label="聚合知识成员">
      <div><strong>{activeGroup.members.length} 条知识</strong><button aria-label="关闭聚合成员" onClick={() => setExpanded(undefined)}>×</button></div>
      {activeGroup.members.map(marker => <button key={marker.id} onClick={() => { onSelect(marker.id); setExpanded(undefined); }}>{marker.label}</button>)}
      {level < 2 && onEnterRegion && <button onClick={() => { setExpanded(undefined); onEnterRegion(); }}>进入下一级展开气泡</button>}
    </div>}
    <div className="map-legend" aria-label="地图颜色图例"><span style={{ background: color }} />{colorMode === 'territory' ? '政权／疆域：虚构测试辖区' : markers.length === 0 ? knowledgeStatus === 'missing' ? '发展主题：资料不足，暂无法判断（灰色）' : '发展主题：当前筛选无匹配知识（灰色）' : `发展主题：${themeLabel || (!theme || theme === '全部' ? '多主题并存' : theme)}（测试配色）`}{!snapshot && ' · 暂无可着色历史面'}</div>
    {visibleRelations.length > 0 && <div className="map-relations" aria-label="地图关系连线">实线：{visibleRelations.map(relation => relation.label).join('；')}（测试关系）</div>}
    {level === 2 && <div className="map-overlap-hint">同位置知识可从右侧列表逐条阅读</div>}
    {failure && <div className="map-fallback" role="alert">此浏览器无法显示三维地球。仍可从右侧知识列表阅读内容。</div>}
    <div className="globe-tools"><button aria-label="向东旋转地球" onClick={() => command.current('east')}>↻</button><button aria-label="复位地球视角" onClick={() => command.current('reset')}>⌖</button><span>拖动地球 · 探索世界</span></div>
    <div className="render-status"><span>{ready ? '地球已就绪' : failure ? '地图不可用' : '地球准备中'}</span> · <span role="status" aria-label="视角状态">{view}</span></div>
  </div>;
}
