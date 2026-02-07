export type TileContent = {
	title: string;
	body: string;
	zoomedBody?: string;
	children?: string[];
};

export type TileContents = Record<string, TileContent>

export type ShownContent = {
	title: string;
	id: string;
	body: string;
};

export type Layout = {
	isLandscape: boolean;
	isMaxed: boolean;
	padLoc: 'top' | 'left' | 'none';
	unit: number;
	pSize: number;
};


export type Tile = { top: number; left: number; height: number; width: number };
export type Direction = 'left' | 'right' | 'up' | 'down';

export const MAX_TILE = 720;

export function getFibs(n: number) {
	const out = [1, 1];
	while (out.length < n) {
		let l = out.length;
		out.push(out[l - 1] + out[l - 2]);
	}
	return out;
}

export function getColorArr(rate: number): [number, number, number] {
	return [120 + Math.sin(rate * 2 * Math.PI) * 100, 80 + Math.cos(rate * 2 * Math.PI) * 100, 200];
}

export function getColorByRate(rate: number): string {
	const hue = rate * 180 + 10; // avoid full wrap for smoother ends
	return `hsl(${hue}, 50%, 75%)`;
}

export function getColorMuted(rate: number): string {
	const hue = 200 + rate * 80;
	const light = 40 + Math.sin(rate * Math.PI) * 20;
	return `hsl(${hue}, 30%, ${light}%)`;
}

export function getLayout(width: number, height: number, fibs: number[]): Layout {
	let n = fibs.length;
	let smallD = fibs[n - 1];
	let sumD = smallD + fibs[n - 2];
	if (width > MAX_TILE * 2 && height > MAX_TILE * sumD / smallD) {
		return { padLoc: 'none', isMaxed: true, unit: MAX_TILE / smallD, isLandscape: false, pSize: 0 }

	}
	let isMaxed = false;
	let upperPadLim = fibs[n - 2];
	let lowerPadLim = fibs[Math.max(0, n - 4)];
	let isLandscape = true;
	if (height <= width * ((smallD + upperPadLim) / sumD)) {
		if (height >= width * ((smallD + lowerPadLim) / sumD)) {
			let pSize = height - width * (smallD / sumD);
			return { unit: width / sumD, isLandscape, padLoc: 'top', pSize, isMaxed };
		}
		if (width >= height * ((sumD + lowerPadLim) / smallD)) {
			let pSize = width - height * (sumD / smallD);
			return { unit: height / smallD, isLandscape, padLoc: 'left', pSize, isMaxed };
		}
	}
	isLandscape = false;
	if (width <= (height * (smallD + upperPadLim)) / sumD) {
		let pSize = height - width * (sumD / smallD);
		if (pSize > 0) return { unit: width / smallD, isLandscape, padLoc: 'top', pSize, isMaxed };
	}
	let pSize = width - height * (smallD / sumD);
	return { unit: height / sumD, isLandscape, padLoc: 'left', pSize, isMaxed }; //possibly wont fill it out?
}

export function tilesFromLayout(
	layout: Layout,
	extWidth: number,
	extHeight: number,
	fibs: number[],
	gap: number,
): Tile[] {
	const out: Tile[] = [];
	if ((extWidth == undefined) || isNaN(extWidth)) return out;
	let top = gap / 2;
	let left = gap / 2;

	if (layout.isMaxed) {
		let { topPad, leftPad } = getMaxedShape(extWidth, extHeight, fibs)
		top = topPad;
		left = leftPad;

	}
	let ps = layout.pSize;
	if (layout.padLoc == 'left') {
		out.push({ top, left, width: ps, height: extHeight });
		left += ps;
	}
	if (layout.padLoc == 'top') {
		out.push({ top, left, width: extWidth, height: ps });
		top += ps;
	}

	let dirInd = 0;
	if (layout.isLandscape) {
		dirInd = 3
		top += fibs[fibs.length - 1] * layout.unit;
	}
	fillTiles(out, fibs, left, top, dirInd, layout.unit)
	if (layout.isMaxed) {
		let { height, width, topPad, leftPad } = getMaxedShape(extWidth, extHeight, fibs)
		let left = width + leftPad;
		let top = height + topPad;
		fillTiles(out, fibs, left, top, 2, layout.unit)

	}
	out.sort((l, r) => Math.min(r.height, r.width) - Math.min(l.height, l.width))
	return out;
}

function getMaxedShape(extWidth: number, extHeight: number, fibs: number[]) {
	let n = fibs.length;
	let shortSide = fibs[n - 1]
	let longSide = shortSide + fibs[n - 2]
	let height = MAX_TILE * longSide / shortSide;
	let width = MAX_TILE * 2;
	return { height, width, topPad: (extHeight - height) / 2, leftPad: (extWidth - width) / 2 }

}


const DIRS: Direction[] = ['right', 'down', 'left', 'up'];

function fillTiles(out: Tile[], fibs: number[], left: number, top: number, dirInd: number, unit: number) {


	function addTile(sizeW: number, sizeH: number, d: Direction) {
		let size = { width: sizeW, height: sizeH };
		if (d == 'right') {
			out.push({ top, left, ...size });
			left += sizeW;
			top += sizeH;
		} else if (d == 'down') {
			left -= sizeW;
			out.push({ top, left, ...size });
			top += sizeH;
		} else if (d == 'left') {
			top -= sizeH;
			left -= sizeW;
			out.push({ top, left, ...size });
		} else if (d == 'up') {
			top -= sizeH;
			out.push({ top, left, ...size });
			left += sizeW;
		}
	}
	for (let i = 0; i < fibs.length; i++) {
		let fibU = fibs[fibs.length - 1 - i] * unit;
		addTile(fibU, fibU, DIRS[dirInd]);
		dirInd = (dirInd + 1) % DIRS.length;
	}
}


export function styleFromTile(tile: Tile) {
	return `top: ${tile.top}px; left: ${tile.left}px; width: ${tile.width}px; height: ${tile.height}px;`;
}
