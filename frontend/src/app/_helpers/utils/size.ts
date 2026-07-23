export const base1000Units = ["bytes", "kB", "MB", "GB", "TB", "PB"] as const;

export type Base1000Unit = (typeof base1000Units)[number];

const isBase1000Unit = (unit: Unit): unit is Base1000Unit => base1000Units.includes(unit as Base1000Unit);

export const base1024Units = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB"] as const;

export type Base1024Unit = (typeof base1024Units)[number];

export type Unit = Base1000Unit | Base1024Unit;

export interface SizeResultBase1000 {
    values: number[];
    unit: Base1000Unit;
}

export interface SizeResultBase1024 {
    values: number[];
    unit: Base1024Unit;
}

export const getClosestBase1000Unit = (bytes: number[]): Base1000Unit => {
    let maxValue = Math.max(...bytes);
    let outputUnitIndex = 0;
    while (maxValue >= 1000) {
        maxValue /= 1000;
        outputUnitIndex++;
    }
    return base1000Units[outputUnitIndex];
};

export const getClosestBase1024Unit = (bytes: number[]): Base1024Unit => {
    let maxValue = Math.max(...bytes);
    let outputUnitIndex = 0;
    while (maxValue >= 1024) {
        maxValue /= 1024;
        outputUnitIndex++;
    }
    return base1024Units[outputUnitIndex];
};

export const getFormattedBytesWithClosestBase1000Unit = (bytes: number[]): SizeResultBase1000 => {
    const unit = getClosestBase1000Unit(bytes);
    return {
        values: bytes.map(x => convertBytesToBase1000Unit(x, unit)),
        unit
    };
};

export const getFormattedBytesWithClosestBase1024Unit = (bytes: number[]): SizeResultBase1024 => {
    const unit = getClosestBase1024Unit(bytes);
    return {
        values: bytes.map(x => convertBytesToBase1024Unit(x, unit)),
        unit
    };
};

export const getFormattedValuesWithClosestBase1000Unit = (values: number[], inputUnit: Unit): SizeResultBase1000 => {
    const bytes = values.map(value => convertUnitToBytes(value, inputUnit));
    return getFormattedBytesWithClosestBase1000Unit(bytes);
};

const defaultPrecisionMapBase1000 = {
    bytes: 0,
    kB: 0,
    MB: 1,
    GB: 1,
    TB: 2,
    PB: 2
} as const satisfies Record<Base1000Unit, number>;

const defaultPrecisionMapBase1024 = {
    bytes: 0,
    KiB: 0,
    MiB: 1,
    GiB: 1,
    TiB: 2,
    PiB: 2
} as const satisfies Record<Base1024Unit, number>;

export const bytesToLargestPossibleBase1000Unit = (bytes: number, separator: string): string => {
    const { values, unit } = getFormattedBytesWithClosestBase1000Unit([bytes]);
    const value = values[0];
    return `${value.toFixed(defaultPrecisionMapBase1000[unit]).replace(".", separator)} ${unit}`;
};

export const bytesToLargestPossibleBase1024Unit = (bytes: number, separator: string): string => {
    const { values, unit } = getFormattedBytesWithClosestBase1024Unit([bytes]);
    const value = values[0];
    return `${value.toFixed(defaultPrecisionMapBase1024[unit]).replace(".", separator)} ${unit}`;
};

export const sizeToLargestPossibleBase1000Unit = (size: number, inputUnit: Unit, separator: string): string =>
    bytesToLargestPossibleBase1000Unit(convertUnit(size, inputUnit, "bytes"), separator);

export const sizeToLargestPossibleBase1024Unit = (size: number, inputUnit: Unit, separator: string): string =>
    bytesToLargestPossibleBase1024Unit(convertUnit(size, inputUnit, "bytes"), separator);

const getBase1000UnitIndex = (unit: Base1000Unit): number => base1000Units.findIndex(x => x === unit);

const getBase1024UnitIndex = (unit: Base1024Unit): number => base1024Units.findIndex(x => x === unit);

const convertBase1000UnitToBytes = (size: number, unit: Base1000Unit) =>
    size * Math.pow(1000, getBase1000UnitIndex(unit));

const convertBase1024UnitToBytes = (size: number, unit: Base1024Unit) =>
    size * Math.pow(1024, getBase1024UnitIndex(unit));

const convertUnitToBytes = (size: number, unit: Unit) => {
    if (isBase1000Unit(unit)) return convertBase1000UnitToBytes(size, unit);
    return convertBase1024UnitToBytes(size, unit);
};

const convertBytesToBase1000Unit = (size: number, unit: Base1000Unit) =>
    size * Math.pow(1000, -getBase1000UnitIndex(unit));

const convertBytesToBase1024Unit = (size: number, unit: Base1024Unit) =>
    size * Math.pow(1024, -getBase1024UnitIndex(unit));

const convertBytesToUnit = (size: number, unit: Unit) => {
    if (isBase1000Unit(unit)) return convertBytesToBase1000Unit(size, unit);
    return convertBytesToBase1024Unit(size, unit);
};

export const convertUnit = (size: number, inputUnit: Unit, outputUnit: Unit) => {
    const bytes = convertUnitToBytes(size, inputUnit);
    return convertBytesToUnit(bytes, outputUnit);
};

export const convertUnitPrice = (size: number, inputUnit: Unit, outputUnit: Unit) => {
    return convertUnit(size, outputUnit, inputUnit);
};
