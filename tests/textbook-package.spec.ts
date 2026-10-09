import { expect, test } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { createTextbookRepository } from '../src/modules/history/textbook';

const data = JSON.parse(readFileSync('public/data/history_book_01.json', 'utf8'));
const repository = createTextbookRepository(data);

test('最终教材包可由现有网页直接加载，图片与地图可见', async ({ page }) => {
  await page.goto('/textbook');
  await expect(page.getByText(`${repository.knowledge.length} 条知识 · 256 张独立图片 · 45 张教材地图原图`)).toBeVisible();
  await expect(page.locator('.textbook-map-list button')).toHaveCount(45);
  await page.locator('.textbook-map-list button').first().click();
  const image = page.locator('.textbook-map-image img');
  await expect(image).toBeVisible();
  await expect.poll(() => image.evaluate((element: HTMLImageElement) => element.naturalWidth)).toBeGreaterThan(100);
  await expect(page.getByText(/PDF 图像坐标，未配准到经纬度/)).toBeVisible();
});

test('重清洗包保存全部原候选来源，香港澳门独立定年且证据可读', () => {
  expect(data.reclean_report.reviewed_candidate_count).toBe(819);
  expect(repository.knowledge.length + data.archived_knowledge_candidates.length).toBe(819);
  expect(data.knowledge_aliases.history_book_01_p0181_k003).toEqual([
    'history_book_01_p0191_k002', 'history_book_01_p0191_k003',
  ]);
  expect(repository.get('history_book_01_p0181_k003')).toBeUndefined();
  expect(repository.get('history_book_01_p0191_k002')?.time.startYear).toBe(1997);
  expect(repository.get('history_book_01_p0191_k003')?.time.startYear).toBe(1999);
  expect(repository.getEvidence('history_book_01_p0191_k002').map(b => b.id)).toContain('history_book_01_p0181_b002');
  expect(repository.getEvidence('history_book_01_p0191_k003').map(b => b.id)).toContain('history_book_01_p0181_b002');
  expect(repository.get('history_book_01_p0098_k001')?.time.mode).toBe('uncertain');
  expect(repository.get('history_book_01_p0098_k001')?.time.startYear).toBeNull();
  const yuanmou = repository.get('history_book_01_p0009_k002');
  expect(yuanmou?.time.startYear).toBeNull();
  expect(yuanmou?.time.earliestYear).toBeNull();
  expect(repository.listUndated().map(item => item.id)).toContain('history_book_01_p0009_k002');
  expect(repository.getMarkers({ startYear: -3000, endYear: 2100 })).toHaveLength(0);
});

test('主审内容回归：人口与壁画不串条，维新失败背景与影响保留', () => {
  expect(repository.get('history_book_01_p0071_k005')?.summary?.text).toContain('宴饮');
  expect(repository.get('history_book_01_p0071_k005')?.summary?.text).not.toContain('1110');
  expect(repository.get('history_book_01_p0072_k005')?.time.evidenceBlockIds).toContain('history_book_01_p0072_b003');
  const reform = repository.get('history_book_01_p0111_k001');
  expect(reform?.time.endYear).toBeNull();
  expect(reform?.background?.text).toContain('社会基础');
  expect(reform?.impact?.text).toContain('整个运动');
  const table = repository.blocks.find(b => b.id === 'history_book_01_p0038_b009');
  expect(table?.cleanText).toContain('賨');
});
