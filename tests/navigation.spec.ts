import { test, expect } from '@playwright/test';

test('02 下钻保留起点，返回恢复各层区间，刷新重置', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1900 年 — 公元 1999 年');
  await page.getByRole('button', {name:'进入中国区域',exact:true}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1900 年 — 公元 1909 年');
  await page.getByRole('button',{name:'下一个区间'}).click();
  await page.getByRole('button',{name:'进入省级示意区域',exact:true}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1910 年');
  await expect(page.getByRole('button',{name:'进入省级示意区域',exact:true})).toHaveCount(0);
  await page.getByRole('button',{name:'下一个区间'}).click();
  await page.getByRole('button',{name:'返回上一级'}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1910 年 — 公元 1919 年');
  await page.getByRole('button',{name:'返回上一级'}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1900 年 — 公元 1999 年');
  await page.getByRole('button',{name:'下一个区间'}).click();
  await page.reload();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1900 年 — 公元 1999 年');
});

