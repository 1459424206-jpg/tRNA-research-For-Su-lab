
import fs from "node:fs";
const slides = JSON.parse(fs.readFileSync(new URL("../slides.json", import.meta.url), "utf8"));
const FONT = "Noto Sans SC";

function addFooter(slide, ctx, n) {
  ctx.addText(slide, { text: `mim-tRNAseq / Induro-tRNAseq | ${n}`, x: 38, y: 690, w: 1180, h: 18, fontSize: 8, color: "#333333", typeface: FONT });
}
function addText(ctx, slide, text, x, y, w, h, fontSize=12, bold=false) {
  return ctx.addText(slide, { text, x, y, w, h, fontSize, bold, color: "#000000", typeface: FONT, insets: { left: 4, right: 4, top: 2, bottom: 2 } });
}
export async function renderSlide(presentation, ctx, index) {
  const data = slides[index];
  const slide = presentation.slides.add();
  ctx.addShape(slide, { x: 0, y: 0, w: 1280, h: 720, fill: "#FFFFFF", line: ctx.line("#FFFFFF", 0) });
  addText(ctx, slide, data.title, 38, 26, 1204, 38, 16, true);
  ctx.addShape(slide, { x: 38, y: 68, w: 1204, h: 1, fill: "#111111", line: ctx.line("#111111", 0) });
  if (data.kind === "section") {
    addText(ctx, slide, data.body || "", 74, 120, 1125, 470, 12, false);
    addFooter(slide, ctx, index + 1);
    return slide;
  }
  if (data.image) {
    await ctx.addImage(slide, { path: data.image, x: 44, y: 92, w: 610, h: 560, fit: "contain", alt: data.imageLabel || data.title });
    ctx.addShape(slide, { x: 44, y: 654, w: 610, h: 1, fill: "#DDDDDD", line: ctx.line("#DDDDDD", 0) });
    addText(ctx, slide, data.imageLabel || "", 44, 660, 610, 26, 9, false);
    addText(ctx, slide, data.body || "", 690, 94, 540, 465, 12, false);
    if (data.note) addText(ctx, slide, data.note, 690, 575, 540, 70, 12, false);
    addFooter(slide, ctx, index + 1);
    return slide;
  }
  addText(ctx, slide, data.body || "", 58, 92, 1160, 570, 12, false);
  addFooter(slide, ctx, index + 1);
  return slide;
}
