export type TileContent = {
	title: string;
	id: string;
	assignedTile: number;
	body: string;
	zoomedBody?: string;
};

export type Layout = {
	isLandscape: boolean;
	padLoc: 'top' | 'left' | 'none';
	unit: number;
	pSize: number;
};

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
