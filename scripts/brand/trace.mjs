// Step 2 of logo tracing: potrace the masks from trace_logos.py into
// single-color SVGs in public/brand/ (fill = currentColor, so CSS sets the color).
import { readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import potrace from 'potrace';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, '../../public/brand');
mkdirSync(out, { recursive: true });

const jobs = [
  { name: 'duck-icon', title: 'Urban Duck', scale: 1, color: '#243447' },
  { name: 'logo-corporate', title: 'Urban Duck', scale: 0.5, color: '#231F20' }, // mask was traced at 2x
];

const trace = (file) =>
  new Promise((resolve, reject) => {
    const t = new potrace.Potrace({ threshold: 128, turdSize: 20, optTolerance: 0.3, alphaMax: 1 });
    t.loadImage(file, (err) => (err ? reject(err) : resolve(t)));
  });

for (const job of jobs) {
  const t = await trace(path.join(here, '.build', `${job.name}.png`));
  const svg = t.getSVG();
  const [, w, h] = svg.match(/viewBox="0 0 (\d+) (\d+)"/) ?? svg.match(/width="(\d+)" height="(\d+)"/);
  const d = svg.match(/ d="([^"]+)"/)[1].replace(/\s+/g, ' ').trim();
  const vw = Math.round(w * job.scale);
  const vh = Math.round(h * job.scale);
  const g = job.scale === 1 ? '' : ` transform="scale(${job.scale})"`;
  const file = path.join(out, `${job.name}.svg`);
  writeFileSync(
    file,
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${vw} ${vh}" role="img" aria-label="${job.title}" color="${job.color}" fill="currentColor">` +
      `<title>${job.title}</title><path fill-rule="evenodd"${g} d="${d}"/></svg>\n`,
  );
  console.log(`${path.relative(process.cwd(), file)}  ${vw}x${vh}  ${Math.round(statSync(file).size / 1024)} KB`);
}
