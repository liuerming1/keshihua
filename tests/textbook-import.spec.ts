import { expect, test } from '@playwright/test';
import { createTextbookRepository, parseTextbookPackage } from '../src/modules/history/textbook';

const packageFixture = {
  documents: [{ id: 'doc-1', title: '教材', file_name: 'book.pdf' }],
  blocks: [{ id: 'block-1', page_id: 'page-1', raw_text: '公元前 100 年原文', clean_text: '公元前100年原文' }],
  assets: [{ id: 'asset-1', page_id: 'page-1', block_id: 'block-1', type: 'map', caption: '地图' }],
  places: [
    {
      id: 'place-verified', name_as_written: '已核验地点', coordinates: [116.4, 39.9],
      coordinate_evidence_block_ids: ['block-1'], coordinate_status: 'verified',
    },
    { id: 'place-unverified', name_as_written: '未核验地点', coordinates: [117, 40] },
  ],
  knowledge: [
    {
      id: 'dated', title: '有据事件', kind: 'event', content_type: 'war',
      time: { source_text: '公元前100年', mode: 'point', start_year: -100, end_year: null, end_status: 'not_applicable', evidence_block_ids: ['block-1'] },
      themes: ['war', 'politics'], place_refs: [{ place_id: 'place-verified', role: 'occurrence', evidence_block_ids: ['block-1'] }],
      summary: { text: '原文摘要', evidence_block_ids: ['block-1'] }, flow: [], points: [], background: null, impact: null,
      evidence_block_ids: ['block-1'], asset_ids: ['asset-1'], source_inventory_ids: [], uncertainties: [], review_status: 'pending_review',
    },
    {
      id: 'unknown-process', title: '结束年未知的过程', kind: 'process',
      time: { source_text: '某时期开始', mode: 'duration', start_year: -100, end_year: null, end_status: 'unknown' },
      themes: ['war'], place_refs: [{ place_id: 'place-unverified', role: 'occurrence', evidence_block_ids: [] }],
    },
    {
      id: 'ongoing-process', title: '明确持续中的过程', kind: 'process',
      time: { source_text: '从公元1年持续', mode: 'duration', start_year: 1, end_year: null, end_status: 'ongoing' },
      themes: ['culture'], place_refs: [],
    },
    {
      id: 'undated', title: '未定年知识', kind: null,
      time: { source_text: '大致同一时期', mode: 'unknown', start_year: null, end_year: null, end_status: 'unknown' },
      themes: ['culture'], place_refs: [], asset_ids: ['asset-1'],
    },
  ],
  relations: [], inventory: [],
};

test('导入保留教材证据、图片、多主题和未知时间', () => {
  const parsed = parseTextbookPackage(packageFixture);
  expect(parsed.knowledge).toHaveLength(4);
  expect(parsed.knowledge[0].themes).toEqual(['war', 'politics']);
  expect(parsed.knowledge[0].summary?.evidenceBlockIds).toEqual(['block-1']);
  expect(parsed.knowledge[0].assetIds).toEqual(['asset-1']);
  expect(parsed.knowledge[3].time.startYear).toBeNull();
});

test('时间查询不把缺少结束年的旧 process 当作 ongoing', () => {
  const repository = createTextbookRepository(packageFixture);
  expect(repository.query({ startYear: -100, endYear: -1, theme: 'war' }).items.map((item) => item.id)).toEqual(['dated']);
  expect(repository.query({ startYear: 1, endYear: 10 }).items.map((item) => item.id)).toEqual(['ongoing-process']);
  expect(repository.listUndated().map((item) => item.id)).toContain('unknown-process');
});

test('未定年条目可独立访问，主题筛选仍然生效', () => {
  const repository = createTextbookRepository(packageFixture);
  expect(repository.listUnknownTime('culture').map((item) => item.id)).toEqual(['undated']);
  expect(repository.get('undated')?.title).toBe('未定年知识');
  expect(repository.getEvidence('dated')[0].rawText).toContain('公元前 100 年');
  expect(repository.getAssets('dated')[0].caption).toBe('地图');
});

test('有证据的宽年代窗口仍可查询，不重复列为无法定位', () => {
  const sample = { ...packageFixture, knowledge: [{ id: 'bounded', title: '约1900年', kind: 'event', themes: ['文化'],
    time: { mode: 'uncertain', start_year: null, earliest_year: 1895, latest_year: 1905, end_status: 'known' } }] };
  const repository = createTextbookRepository(sample);
  expect(repository.query({ startYear: 1900, endYear: 1900 }).items.map((item) => item.id)).toEqual(['bounded']);
  expect(repository.listUndated()).toHaveLength(0);
});

test('地图 marker 只来自有有效坐标且显式核验的地点', () => {
  const repository = createTextbookRepository(packageFixture);
  const markers = repository.getMarkers({ startYear: -100, endYear: -1 });
  expect(markers).toHaveLength(1);
  expect(markers[0]).toMatchObject({ knowledgeId: 'dated', placeId: 'place-verified', coordinates: [116.4, 39.9] });
});

test('补充史料、图片内标签和 UNESCO 参考点分层保留', () => {
  const sample = {
    ...packageFixture,
    knowledge: [{ ...packageFixture.knowledge[0],
      summary: { text: '限定摘要', evidence_block_ids: ['block-1'], external_source_ids: ['source-1'] },
      finalization: { status: 'qualified', source_verification_status: 'needs_correction', patch_applied: true,
        supplemental_source_ids: ['source-1'] } }],
    map_layers: [{ id: 'map-1', raster_asset_id: 'asset-1', raster_file_path: '/textbook-assets/a.png',
      image_labels: [{ text: '图内地名', image_position: [0.5, 0.6] }], reference_point_ids: ['point-1'],
      georeferenced: false, geometry_status: 'not_digitized' }],
    map_reference_points: { features: [{ id: 'point-1', geometry: { type: 'Point', coordinates: [120, 30] },
      properties: { name: '遗产参考点', map_candidate_id: 'map-1', temporal_basis: '2019_world_heritage_property',
        historical_geometry: false } }] },
    verification_report: { external_source_registry: { 'source-1': { title: '官方来源', url: 'https://example.org/source' } } },
  };
  const repository = createTextbookRepository(sample);
  expect(repository.get('dated')?.summary?.externalSourceIds).toEqual(['source-1']);
  expect(repository.get('dated')?.finalization?.status).toBe('qualified');
  expect(repository.mapLayers[0].imageLabels[0].imagePosition).toEqual([0.5, 0.6]);
  expect(repository.mapLayers[0].georeferenced).toBe(false);
  expect(repository.mapReferencePoints[0]).toMatchObject({ coordinates: [120, 30], historicalGeometry: false });
  expect(repository.externalSources[0].url).toBe('https://example.org/source');
});
