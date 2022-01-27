
export function histogram<T, V extends PropertyKey>(valueExtractor: (d: T) => V): (values: T[]) => any {
    return function (data: T[]) {
        return data.reduce((acc: any, current: T) => {
            let value = valueExtractor(current);
            if (acc.hasOwnProperty(value)) {
                acc[value] += 1;
            } else {
                acc[value] = 1;
            }
            return acc;
        }, {})
    }
}
