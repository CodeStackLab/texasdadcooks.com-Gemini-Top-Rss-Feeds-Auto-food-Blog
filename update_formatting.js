const fs = require('fs');
const files = [
    'c:/Users/mohda/OneDrive/Desktop/n8n workflow/Justcookdaily.com/justcookdaily.com — Gemini Google Trends Auto Blog_ — Expiry Date_ 11 April 2027 (Valid for 1 year) — Buyer_ dalfins33.json',
    'c:/Users/mohda/OneDrive/Desktop/n8n workflow/Justcookdaily.com/workflow_sanitized.json'
];

const jsCode = `// ============================================
// EXTRACT & PARSE ARTICLE — v11 FORMATTED
// Handles Table conversion, List wrapping, and Styled callouts
// ============================================

const createCleanSlug = (text) => {
  if (!text) return 'cooking-recipe';
  return text.toLowerCase()
    .replace(/[^a-z0-9\\s-]/g, '')
    .replace(/\\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 60)
    .replace(/-$/, '');
};

const d = $input.first().json;
const raw = d._aiRawOutput || '';
const forcedCatId = d._forcedCategoryId || 1;
const forcedCatName = d._forcedCategoryName || 'Quick & Easy Recipes';
const topicFallback = d.trendingTopic || 'Easy Cooking Recipes';

// Emergency fallback if AI completely failed
if (!raw || raw.length < 200) {
  return [{ json: {
    ...d,
    title: \`The Complete Guide to \${topicFallback}\`,
    articleHTML: \`<p>Discover our expert guide to \${topicFallback} with professional tips and techniques.</p><h2>Getting Started</h2><p>This comprehensive guide covers everything you need to know about \${topicFallback}.</p>\`,
    category_id: forcedCatId,
    slug: createCleanSlug(topicFallback),
    _hasContent: false
  } }];
}

// Parse the output
const lines = raw.split('\\n');
let title='', slug='', metaDesc='', tagsRaw='', excerpt='';
let imgQ1='', imgQ2='', imgQ3='', imgQ4='';
let articleStart = -1;

for (let i = 0; i < lines.length; i++) {
  const t = lines[i].trim();
  if (t.startsWith('TITLE:'))    title    = t.slice(6).trim().replace(/^[\\"']|[\\"']$/g, '');
  if (t.startsWith('SLUG:'))     slug     = createCleanSlug(t.slice(5).trim());
  if (t.startsWith('META:'))     metaDesc = t.slice(5).trim().substring(0, 155);
  if (t.startsWith('TAGS:'))     tagsRaw  = t.slice(5).trim();
  if (t.startsWith('EXCERPT:'))  excerpt  = t.slice(8).trim();
  if (t.startsWith('QUERY1:'))   imgQ1    = t.slice(7).trim();
  if (t.startsWith('QUERY2:'))   imgQ2    = t.slice(7).trim();
  if (t.startsWith('QUERY3:'))   imgQ3    = t.slice(7).trim();
  if (t.startsWith('QUERY4:'))   imgQ4    = t.slice(7).trim();
  if (t.includes('===START===')) { articleStart = i + 1; break; }
}

let articleHTML = '';
if (articleStart >= 0) {
  const rest = lines.slice(articleStart);
  const endIdx = rest.findIndex(l => l.includes('===END==='));
  articleHTML = (endIdx >= 0 ? rest.slice(0, endIdx) : rest).join('\\n').trim();
} else {
  const firstH = raw.indexOf('<p>');
  if (firstH >= 0) articleHTML = raw.substring(firstH);
  else articleHTML = raw;
}

// FORMATTING IMPROVEMENTS
// 1. Convert Markdown Tables to HTML
const convertTables = (html) => {
    const lines = html.split('\\n');
    let newLines = [];
    let tableData = [];
    let inTable = false;

    const flushTable = () => {
        if (tableData.length === 0) return '';
        let t = '<div style=\\"overflow-x:auto;margin:24px 0;\\"><table style=\\"width:100%;border-collapse:collapse;border:1px solid #eee;font-size:14px;\\">';
        const data = tableData.filter(row => !row.every(cell => cell.match(/^[ :\\-\\|]+$/)));
        data.forEach((row, i) => {
            const tag = i === 0 ? 'th' : 'td';
            const style = i === 0 ? 'background:#fdf2f0;color:#c0392b;padding:12px;border:1px solid #eee;text-align:left;' : 'padding:12px;border:1px solid #eee;';
            t += '<tr>';
            row.forEach(cell => { t += \`<\${tag} style=\\"\${style}\\">\${cell.trim()}</\${tag}>\`; });
            t += '</tr>';
        });
        t += '</table></div>';
        tableData = [];
        return t;
    };

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('|') && line.endsWith('|')) {
            inTable = true;
            tableData.push(line.split('|').slice(1, -1));
        } else {
            if (inTable) { newLines.push(flushTable()); inTable = false; }
            newLines.push(lines[i]);
        }
    }
    if (inTable) newLines.push(flushTable());
    return newLines.join('\\n');
};

articleHTML = convertTables(articleHTML);

// 2. Wrap loose <li> tags and handle markdown lists
articleHTML = articleHTML
  .replace(/^(?!<li|<ul|<ol)\\s*[\\*\\-]\\s+(.+)$/gm, '<li>$1</li>') // Convert * or - to <li>
  .replace(/(<li>[\\s\\S]*?<\\/li>)/g, (match) => {
      // This is a simple list wrapper - group adjacent <li> tags
      return match; 
  });
// More robust wrapping
const wrapLists = (html) => {
    return html.replace(/(<li>[\\s\\S]*?<\\/li>\\n?)+/g, (match) => {
        if (match.trim().startsWith('<ul') || match.trim().startsWith('<ol')) return match;
        return \`<ul>\\n\${match.trim()}\\n</ul>\\n\`;
    });
};
articleHTML = wrapLists(articleHTML);

// 3. Style Callouts (Pro Tips, Chef Tips, etc.)
articleHTML = articleHTML.replace(/<p>(<strong>)?(Pro Tip|Chef Tip|Science Behind the Magic|Nutrition Facts|Note):?\\s*(<\\/strong>)?([\\s\\S]*?)<\\/p>/gi, (match, s1, type, s2, content) => {
    return \`<div style=\\"background:#f9f9f9;border-left:4px solid #c0392b;padding:16px 20px;margin:24px 0;border-radius:0 8px 8px 0;\\"><strong>\${type}:</strong>\${content}</div>\`;
});

// 4. General Cleanup
articleHTML = articleHTML
  .replace(/^#{3}\\s+(.+)$/gm, '<h3>$1</h3>')
  .replace(/^#{2}\\s+(.+)$/gm, '<h2>$1</h2>')
  .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
  .replace(/__(.*?)__/g, '<strong>$1</strong>')
  .replace(/\\u2014/g, '-')
  .replace(/^---\\s*$/gm, '<hr style=\\"border:0;border-top:1px solid #eee;margin:32px 0;\\"/>');

let tags = tagsRaw.split(',').map(t => t.replace(/[\\\\\\[\\\\\\]\\"']/g,'').trim()).filter(t => t.length > 1).slice(0,6);

return [{ json: {
  ...d,
  title: title || topicFallback,
  articleHTML,
  category_id: forcedCatId,
  slug: slug || createCleanSlug(title),
  imgQuery1: imgQ1 || topicFallback,
  imgQuery4: imgQ4 || 'cooking chef'
} }];`;

files.forEach(path => {
    try {
        let content = fs.readFileSync(path, 'utf8');
        const escapedCode = jsCode.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
        
        const nodeMarkers = ['"name": "Extract & Parse Article"', '"name": "Extract & Store HTML"'];
        let nodeIdx = -1;
        for (const m of nodeMarkers) {
            nodeIdx = content.indexOf(m);
            if (nodeIdx !== -1) break;
        }
        
        if (nodeIdx === -1) {
            console.log(`Node not found in ${path}, skipping.`);
            return;
        }
        
        let jsCodeStart = content.lastIndexOf('"jsCode": "', nodeIdx);
        if (jsCodeStart === -1) throw new Error('jsCode start not found');
        jsCodeStart += '"jsCode": "'.length;
        
        let nextPropIdx = content.indexOf('},', jsCodeStart);
        if (nextPropIdx === -1) nextPropIdx = content.length;
        let stringEndIdx = content.lastIndexOf('"', nextPropIdx);
        
        const newContent = content.substring(0, jsCodeStart) + escapedCode + content.substring(stringEndIdx);
        fs.writeFileSync(path, newContent);
        console.log(`Successfully updated formatting logic in ${path}`);
    } catch (err) {
        console.error(`Error updating ${path}:`, err.message);
    }
});
