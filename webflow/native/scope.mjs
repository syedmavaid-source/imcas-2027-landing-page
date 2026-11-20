import fs from 'fs'; import postcss from 'postcss'; import prefixer from 'postcss-prefix-selector';
const src=fs.readFileSync(process.argv[2],'utf8');
const out=await postcss([prefixer({prefix:'#ev-native',transform(prefix,sel,pre){
  if(/^(html|body|:root)$/.test(sel)) return prefix;
  if(/^html\[data-phase=[a-z]+\]/.test(sel)) return sel.replace(/^(html\[data-phase=[a-z]+\])\s*/,'$1 '+prefix+' ');
  if(/^(html|body) /.test(sel)) return prefix+' '+sel.replace(/^(html|body) /,'');
  if(sel==='*') return prefix+', '+prefix+' *';
  if(sel.startsWith('dialog#planner')) return sel;
  return pre;}})]).process(src,{from:undefined});
fs.writeFileSync(process.argv[3],out.css);
