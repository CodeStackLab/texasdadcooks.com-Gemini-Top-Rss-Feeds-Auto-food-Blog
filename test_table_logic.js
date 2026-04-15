const mdTableToHtml = (md) => {
    const lines = md.split('\n');
    let html = '';
    let inTable = false;
    let tableData = [];

    const flushTable = () => {
        if (tableData.length === 0) return '';
        let t = '<div style="overflow-x:auto;margin:24px 0;"><table style="width:100%;border-collapse:collapse;border:1px solid #eee;font-size:14px;">';
        
        // Filter out the |---| separator row
        const data = tableData.filter(row => !row.every(cell => cell.match(/^[ :\-\|]+$/)));
        
        data.forEach((row, i) => {
            const tag = i === 0 ? 'th' : 'td';
            const style = i === 0 
                ? 'background:#fdf2f0;color:#c0392b;padding:12px;border:1px solid #eee;text-align:left;' 
                : 'padding:12px;border:1px solid #eee;';
            
            t += '<tr>';
            row.forEach(cell => {
                t += `<${tag} style="${style}">${cell.trim()}</${tag}>`;
            });
            t += '</tr>';
        });
        
        t += '</table></div>';
        tableData = [];
        return t;
    };

    const newLines = [];
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('|') && line.endsWith('|')) {
            inTable = true;
            const cells = line.split('|').slice(1, -1);
            tableData.push(cells);
        } else {
            if (inTable) {
                newLines.push(flushTable());
                inTable = false;
            }
            newLines.push(lines[i]);
        }
    }
    if (inTable) newLines.push(flushTable());
    
    return newLines.join('\n');
};

const testMd = `Here is a table:
| Protein | Sauce | Why |
|---|---|---|
| Chicken | Pesto | Rich |
| Steak | Red Wine | Deep |

More text.`;

console.log(mdTableToHtml(testMd));
