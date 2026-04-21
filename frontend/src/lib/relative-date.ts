const units = [
	{ label: 'año', seconds: 31536000 },
	{ label: 'mes', seconds: 2592000 },
	{ label: 'semana', seconds: 604800 },
	{ label: 'dia', seconds: 86400 },
	{ label: 'hora', seconds: 3600 },
	{ label: 'minuto', seconds: 60 },
	{ label: 'segundo', seconds: 1 }
] as const;

type Unit = (typeof units)[number]['label'] | '';

export const timeAgo = (date: string | number | Date) => {
	const time = Math.floor((new Date().valueOf() - new Date(date).valueOf()) / 1000);
	const { interval, unit } = calculateTimeDifference(time);
	const suffix = getSuffix(interval, unit);
	return `hace ${interval} ${unit}${suffix}`;
};

export const calculateTimeDifference = (
	time: number
): {
	interval: number;
	unit: Unit;
} => {
	for (const { label, seconds } of units) {
		const interval = Math.floor(time / seconds);
		if (interval >= 1) {
			return {
				interval: interval,
				unit: label
			};
		}
	}
	return {
		interval: 0,
		unit: ''
	};
};

const getSuffix = (interval: number, unit: Unit) => {
	if (interval > 1) {
		return unit === 'mes' ? 'es' : 's';
	}
	return '';
};
