import { test, expect, type Page } from '@playwright/test';
async function year(page:Page,value:number) {
  await page.getByLabel('起始年份',{exact:true}).fill(String(value));
  await page.getByRole('button',{name:'应用年份'}).click();
}
const reading = (page:Page,title:string)=>page.getByRole('button',{name:'阅读 '+title,exact:true});

test('03 时间端点、持续过程、起源与跨公元无零年', async ({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'进入中国区域',exact:true}).click();
  await expect(reading(page,'演示事件：观测记录')).toBeVisible();
  await expect(reading(page,'演示过程：资料整理')).toBeVisible();
  await expect(reading(page,'演示事件：典籍传播')).toHaveCount(0);
  await page.getByRole('button',{name:'下一个区间'}).click();
  await expect(reading(page,'演示事件：典籍传播')).toBeVisible();
  await expect(reading(page,'演示事件：典籍编纂')).toHaveCount(0);
  await expect(reading(page,'演示事件：观测记录')).toHaveCount(0);
  await expect(reading(page,'演示过程：资料整理')).toHaveCount(0);
  await page.getByRole('button',{name:'进入省级示意区域',exact:true}).click();
  await year(page,1905);await expect(reading(page,'演示过程：资料整理')).toBeVisible();
  await year(page,1906);await expect(reading(page,'演示过程：资料整理')).toHaveCount(0);
  await year(page,-1);await expect(reading(page,'演示边界：公元前一年')).toBeVisible();
  await expect(reading(page,'演示过程：跨公元纪年')).toBeVisible();
  await page.getByRole('button',{name:'下一个区间'}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1 年');
  await expect(reading(page,'演示边界：公元一年')).toBeVisible();
  await expect(reading(page,'演示边界：公元前一年')).toHaveCount(0);
  await page.getByRole('button',{name:'上一个区间'}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元前 1 年');
  await year(page,0);await expect(page.getByRole('alert')).toContainText('没有 0 年');
});

test('04/07/09 起点地图、主题一致、缺项与恢复',async({page})=>{
  await page.goto('/');
  await expect(page.getByLabel('地图资料状态')).toContainText('虚构测试辖区甲');
  await page.getByLabel('地图着色',{exact:true}).selectOption('theme');
  await page.getByLabel('知识主题',{exact:true}).selectOption('science');
  await expect(page.getByLabel('地图颜色图例')).toContainText('科技');
  await expect(page.getByRole('button',{name:/^阅读 /})).toHaveCount(3);
  await expect(reading(page,'演示事件：远方记录')).toBeVisible();
  await expect(reading(page,'演示事件：典籍编纂')).toHaveCount(0);
  await page.getByLabel('知识主题',{exact:true}).selectOption('war');
  await expect(page.getByText('当前筛选无匹配知识',{exact:true})).toBeVisible();
  await expect(page.getByLabel('地图颜色图例')).toContainText('无匹配');
  await page.getByLabel('知识主题',{exact:true}).selectOption('');
  await year(page,1910);await expect(page.getByLabel('地图资料状态')).toContainText('虚构测试辖区乙');
  await year(page,1800);await expect(page.getByLabel('地图资料状态')).toContainText('缺少地图资料');
  await expect(page.getByText('知识资料待补充',{exact:true})).toBeVisible();
  await expect(page.getByText('当前筛选无匹配知识',{exact:true})).toHaveCount(0);
  await page.getByRole('button',{name:'返回演示起点'}).click();
  await expect(reading(page,'演示事件：典籍编纂')).toBeVisible();
  await expect(page.getByLabel('地图资料状态')).toContainText('虚构测试辖区甲');
});

test('05/08 多出处、关系跳转和关闭清除关系',async({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'进入中国区域',exact:true}).click();
  await reading(page,'演示事件：典籍编纂').click();
  await expect(page.getByRole('heading',{name:'发展流程',exact:true})).toBeVisible();
  await expect(page.getByLabel('地图关系连线')).toContainText('乙地');
  await page.getByText('展开原文与出处（2 处）',{exact:true}).click();
  await expect(page.getByText(/【虚构原文 A】/)).toBeVisible();
  await expect(page.getByText(/【虚构原文 B】/)).toBeVisible();
  await page.getByRole('button',{name:/查看关联：演示事件：典籍传播/}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1910 年 — 公元 1919 年');
  await expect(page.getByRole('heading',{name:'演示事件：典籍传播',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'返回知识列表'}).click();
  await expect(page.getByLabel('地图关系连线')).toHaveCount(0);
  await page.getByRole('button',{name:'返回演示起点'}).click();
  await reading(page,'演示缺项：待补充条目').click();
  await expect(page.getByText('背景依据待补充。',{exact:true})).toBeVisible();
  await page.getByText('展开原文与出处（0 处）',{exact:true}).click();
  await expect(page.getByText('尚未提供可追溯出处，原文、章节与页码待补充。',{exact:true})).toBeVisible();
});

test('06 聚合成员数对应列表，同坐标可读；连续筛选清除详情',async({page})=>{
  await page.goto('/');
  const total = await page.getByRole('button',{name:/^阅读 /}).count();
  const counts = await page.locator('[data-marker]').evaluateAll(nodes=>nodes.map(node=>{
    const label=node.getAttribute('aria-label')??'';return label.startsWith('展开 ')?Number(label.match(/\d+/)?.[0]):1;
  }));
  expect(counts.reduce((a,b)=>a+b,0)).toBe(total);
  await page.getByRole('button',{name:/展开 .* 条知识聚合/}).first().click();
  const members=page.getByRole('region',{name:'聚合知识成员'});
  await expect(members.getByRole('button',{name:'演示事件：典籍编纂',exact:true})).toBeVisible();
  await members.getByRole('button',{name:'演示事件：典籍编纂',exact:true}).click();
  await page.getByLabel('知识主题',{exact:true}).selectOption('science');
  await expect(page.getByRole('heading',{name:'此刻的历史',exact:true})).toBeVisible();
  await expect(page.getByLabel('地图关系连线')).toHaveCount(0);
  await page.getByLabel('知识主题',{exact:true}).selectOption('');
  await page.getByRole('button',{name:'进入中国区域',exact:true}).click();
  await page.getByRole('button',{name:'进入省级示意区域',exact:true}).click();
  await reading(page,'演示缺项：待补充条目').click();
  await expect(page.getByRole('heading',{name:'演示缺项：待补充条目',exact:true})).toBeVisible();
});


test('07 全部主题图例随实际年份结果改变，资料不足不当作零匹配',async({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'进入中国区域',exact:true}).click();
  await page.getByRole('button',{name:'进入省级示意区域',exact:true}).click();
  await year(page,1905);
  await page.getByLabel('地图着色',{exact:true}).selectOption('theme');
  await expect(page.getByLabel('地图颜色图例')).toContainText('文化');
  await expect(page.getByLabel('地图颜色图例')).not.toContainText('多主题');
  await year(page,1909);await expect(page.getByLabel('地图颜色图例')).toContainText('科技');
  await year(page,2000);await expect(page.getByLabel('地图颜色图例')).toContainText('资料不足');
});

test('04 地图入口可点击，缺地图仍可读知识，资料末端不外推',async({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'在地图中进入区域',exact:true}).click();
  await expect(page.getByLabel('当前时间区间')).toHaveText('公元 1900 年 — 公元 1909 年');
  await page.getByRole('button',{name:'在地图中进入区域',exact:true}).click();
  await year(page,-1);
  await expect(page.getByLabel('地图资料状态')).toContainText('缺少地图资料');
  await reading(page,'演示边界：公元前一年').click();
  await expect(page.getByRole('heading',{name:'演示边界：公元前一年',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'返回演示起点'}).click();
  await year(page,1999);
  await expect(page.getByText('知识资料待补充',{exact:true})).toBeVisible();
  await expect(reading(page,'演示过程：持续观测')).toBeVisible();
  await year(page,2000);
  await expect(reading(page,'演示过程：持续观测')).toHaveCount(0);
});
