import { test, expect } from '@playwright/test';
  test.use({ launchOptions: { args: ['--disable-webgl'] } });
  test('明确提示且列表仍可阅读', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('alert')).toContainText('此浏览器无法显示三维地球');
    await page.getByRole('button', { name: '阅读 演示事件：典籍编纂' }).click();
    await expect(page.getByRole('heading', { name: '演示事件：典籍编纂' })).toBeVisible();
    await page.getByRole('button', { name: '返回知识列表' }).click();
    await expect(page.getByRole('heading', { name: '此刻的历史' })).toBeVisible();
  });
