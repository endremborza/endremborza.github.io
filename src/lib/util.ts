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
	padLoc: 'top' | 'left' | 'none';
	unit: number;
	pSize: number;
};


export type Tile = { top: number; left: number; height: number; width: number };
export type Direction = 'left' | 'right' | 'up' | 'down';

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
	let upperPadLim = fibs[n - 2];
	let lowerPadLim = fibs[Math.max(0, n - 4)];
	let isLandscape = true;
	if (height <= width * ((smallD + upperPadLim) / sumD)) {
		if (height >= width * ((smallD + lowerPadLim) / sumD)) {
			let pSize = height - width * (smallD / sumD);
			return { unit: width / sumD, isLandscape, padLoc: 'top', pSize };
		}
		if (width >= height * ((sumD + lowerPadLim) / smallD)) {
			let pSize = width - height * (sumD / smallD);
			return { unit: height / smallD, isLandscape, padLoc: 'left', pSize };
		}
		// let heightScaler = height / width / (smallD / sumD);
	}
	isLandscape = false;
	if (width <= (height * (smallD + upperPadLim)) / sumD) {
		let pSize = height - width * (sumD / smallD);
		if (pSize > 0) return { unit: width / smallD, isLandscape, padLoc: 'top', pSize };
	}
	let pSize = width - height * (smallD / sumD);
	return { unit: height / sumD, isLandscape, padLoc: 'left', pSize }; //possibly wont fill it out?
}

export function tilesFromLayout(
	layout: Layout,
	extWidth: number,
	extHeight: number,
	fibs: number[],
	gap: number,
): Tile[] {
	const out: Tile[] = [];
	if (extWidth == undefined) return out;
	let top = gap / 2;
	let left = gap / 2;
	let width = extWidth;
	let height = extHeight;
	function addTile(sizeW: number, sizeH: number, d: Direction) {
		let size = { width: sizeW, height: sizeH };
		if (d == 'right') {
			out.push({ top, left, ...size });
			left += sizeW;
			width -= sizeW;
			top += sizeH;
		} else if (d == 'down') {
			left -= sizeW;
			out.push({ top, left, ...size });
			top += sizeH;
			height -= sizeH;
		} else if (d == 'left') {
			top -= sizeH;
			left -= sizeW;
			out.push({ top, left, ...size });
			width -= sizeW;
		} else if (d == 'up') {
			top -= sizeH;
			out.push({ top, left, ...size });
			height -= sizeH;
			left += sizeW;
		}
	}
	let ps = layout.pSize;
	if (layout.padLoc == 'left') {
		out.push({ top, left, width: ps, height });
		left += ps;
		width -= ps;
	}
	if (layout.padLoc == 'top') {
		out.push({ top, left, width, height: ps });
		top += ps;
		height -= ps;
	}
	const DIRS: Direction[] = ['right', 'down', 'left', 'up'];
	let dirInd = 0;
	for (let i = 0; i < fibs.length; i++) {
		let fibU = fibs[fibs.length - 1 - i] * layout.unit;
		if (i == 0) {
			let size = { height: fibU, width: fibU };
			out.push({ top, left, ...size });
			left += fibU;
			if (layout.isLandscape) {
				width -= fibU;
			} else {
				top += fibU;
				height -= fibU;
			}
		} else {
			addTile(fibU, fibU, DIRS[dirInd]);
		}
		if (!layout.isLandscape || i > 0) {
			dirInd = (dirInd + 1) % DIRS.length;
		}
	}
	out.sort((l, r) => Math.min(r.height, r.width) - Math.min(l.height, l.width))
	return out;
}


export function styleFromTile(tile: Tile) {
	return `top: ${tile.top}px; left: ${tile.left}px; width: ${tile.width}px; height: ${tile.height}px;`;
}
