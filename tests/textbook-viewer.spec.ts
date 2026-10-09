import { expect, test } from '@playwright/test';

test('教材页面直接读取 JSON，并让无时间条目可访问', async ({ page }) => {
  await page.route('**/data/history_book_01.json', async (route) => route.fulfill({ json: {
    documents: [{ id: 'book', title: '测试教材' }], pages: [], blocks: [], assets: [], places: [],
    knowledge: [
      { id: 'dated', title: '1900年条目', kind: 'event', themes: ['文化'],
        time: { mode: 'point', start_year: 1900, end_status: 'not_applicable' },
        summary: { text: '有年份摘要', evidence_block_ids: [] }, finalization: { status: 'ready' } },
      { id: 'undated', title: '未定年条目', kind: 'process', themes: ['文化'],
        time: { mode: 'unknown', start_year: null, end_status: 'unknown' },
        summary: { text: '无年份摘要', evidence_block_ids: [] }, finalization: { status: 'needs_review', fact_note: '源材料未给出确切年代。' } },
    ], relations: [], inventory: [], map_layers: [],
  } }));
  await page.goto('/textbook');
  await expect(page.getByRole('heading', { name: '中外历史纲要（上）' })).toBeVisible();
  await expect(page.getByRole('button', { name: /1900年条目/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /未定年条目/ })).toHaveCount(0);
  await page.getByRole('button', { name: /未能定位到区间/ }).click();
  await expect(page.getByRole('button', { name: /未定年条目/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /未定年条目/ })).toContainText('待核');
  await expect(page.getByRole('button', { name: /未定年条目/ })).not.toContainText('已核验');
  await page.getByRole('button', { name: /未定年条目/ }).click();
  await expect(page.getByText('无年份摘要')).toBeVisible();
  await expect(page.getByText('待核说明：源材料未给出确切年代。')).toBeVisible();
});
