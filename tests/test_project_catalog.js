// Exercise the production filter controller against the actual project catalog.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const records = JSON.parse(fs.readFileSync(path.join(root, 'projects.json'), 'utf8'));
function harness(query = '') {
  function element(value = '') {
    return {value, dataset: {}, style: {}, hidden: false, textContent: '', listeners: {},
      addEventListener(k, fn) { this.listeners[k] = fn; },
      focus() { this.focused = true; }};
  }
  const nodes = Object.fromEntries(['q','cat','diff','sort','count','grid','projects-reset','projects-load-more','projects-more-wrap','projects-no-results'].map(k=>[k,element()]));
  nodes.cat.options = [{value:'', textContent:'All topics'}, ...[...new Set(records.map(p=>p.category))].map(value=>({value,textContent:value}))];
  nodes.diff.options = ['', 'Beginner','Intermediate','Advanced'].map(value=>({value}));
  nodes.sort.value = 'featured';
  const cards = records.map(p=>{
    const classes = new Set();
    return {...element(), dataset:{title:p.title.toLowerCase(), category:p.category, levels:p.levels.join(','), featured:p.featured?'1':'0'},
      href:p.href, setAttribute(){}, classList:{contains:c=>classes.has(c), toggle(c,on){if(on)classes.add(c);else classes.delete(c);},remove:c=>classes.delete(c)}};
  });
  nodes.grid.appendChild = card=>{cards.splice(cards.indexOf(card),1);cards.push(card);};
  const context = {document:{readyState:'complete',getElementById:id=>nodes[id]||null,querySelectorAll:()=>cards},
    location:{hash:'',pathname:'/projects.html',search:query},history:{replaceState(){}},URLSearchParams,window:{addEventListener(){}}};
  context.window.location = context.location;
  vm.runInNewContext(fs.readFileSync(path.join(root,'projects.js'),'utf8'),context);
  return {nodes,cards, filter:context.window.filterProjects,
    matches:()=>cards.filter(c=>!c.classList.contains('filter-hidden')),
    visible:()=>cards.filter(c=>!c.classList.contains('filter-hidden')&&!c.classList.contains('page-hidden'))};
}
test('every actual topic and difficulty combination matches catalog membership without duplicates',()=>{
  const h=harness();
  for(const category of h.nodes.cat.options.map(o=>o.value)) for(const level of h.nodes.diff.options.map(o=>o.value)) {
    h.nodes.cat.value=category;h.nodes.diff.value=level;h.filter();
    const expected=records.filter(p=>(!category||p.category===category)&&(!level||p.levels.includes(level)));
    assert.equal(h.matches().length,expected.length,category+' / '+level);
    assert.equal(new Set(h.matches().map(c=>c.href)).size,expected.length);
    assert.equal(h.nodes['projects-no-results'].hidden,expected.length!==0);
    assert.match(h.nodes.count.textContent,new RegExp('^'+expected.length+' projects found'));
  }
});
test('search, empty state, clear, load more and advanced deep link work',()=>{
  const h=harness(); assert.equal(h.visible().length,12);
  assert.equal(h.nodes['projects-more-wrap'].hidden,false);
  h.nodes['projects-load-more'].listeners.click();assert.equal(h.visible().length,records.length);
  assert.equal(h.cards[12].focused,true);
  assert.equal(h.nodes['projects-more-wrap'].hidden,true);
  h.nodes.q.value='no-such-project-123';h.filter();assert.equal(h.matches().length,0);
  assert.equal(h.nodes['projects-no-results'].hidden,false);
  h.nodes['projects-reset'].listeners.click();assert.equal(h.matches().length,records.length);assert.equal(h.visible().length,12);
  h.nodes.q.value='weather';h.filter();assert.equal(h.matches().length,records.filter(p=>p.title.toLowerCase().includes('weather')).length);
  h.nodes.sort.value='title';h.filter();assert.deepEqual(h.cards.map(c=>c.dataset.title),h.cards.map(c=>c.dataset.title).sort((a,b)=>a.localeCompare(b)));
  h.nodes.sort.value='category';h.filter();assert.deepEqual(h.cards.map(c=>c.dataset.category),h.cards.map(c=>c.dataset.category).sort((a,b)=>a.localeCompare(b)));
  const advanced=harness('?difficulty=Advanced');assert.equal(advanced.nodes.diff.value,'Advanced');
  assert.equal(advanced.matches().length,records.filter(p=>p.levels.includes('Advanced')).length);
});
