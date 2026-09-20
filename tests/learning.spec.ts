import { test, expect } from '@playwright/test';

test('01 地球入口可以旋转并打开、关闭一条演示知识', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { name: '时空史图' })).toBeVisible();
  await expect(page.getByLabel('交互地球')).toBeVisible();
  await expect(page.getByText('地球已就绪', { exact: true })).toBeVisible();
  const canvas = page.getByLabel('交互地球').locator('canvas');
  const initialView = await canvas.screenshot();
  const bounds = (await canvas.boundingBox())!;
  await page.mouse.move(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2 + 90);
  await page.mouse.down();
  await page.mouse.move(bounds.x + bounds.width / 2 + 150, bounds.y + bounds.height / 2 + 90, { steps: 12 });
  await page.mouse.up();
  await expect.poll(async () => (await canvas.screenshot()).equals(initialView)).toBe(false);
  await page.getByRole('button', { name: '向东旋转地球' }).click();
  await expect(page.getByRole('status', { name: '视角状态' })).toContainText('已向东旋转');
  await page.getByRole('button', { name: '复位地球视角' }).click();
  await page.getByRole('button', { name: /展开 .* 条知识聚合/ }).first().click();
  await page.getByRole('region', { name: '聚合知识成员' }).getByRole('button', { name: '演示事件：典籍编纂', exact: true }).click();
  await expect(page.getByRole('heading', { name: '演示事件：典籍编纂' })).toBeVisible();
  await expect(page.getByText('演示资料，不是教材原文。', { exact: true })).toBeVisible();
  await expect(page.getByLabel('交互地球')).toBeVisible();
  await page.getByRole('button', { name: '返回知识列表' }).click();
  await expect(page.getByRole('heading', { name: '此刻的历史' })).toBeVisible();
  await page.getByRole('button', { name: '阅读 演示事件：典籍编纂' }).click();
  await expect(page.getByRole('heading', { name: '演示事件：典籍编纂' })).toBeVisible();
  await page.reload();
  await expect(page.getByRole('heading', { name: '此刻的历史' })).toBeVisible();
  expect(errors).toEqual([]);
});


