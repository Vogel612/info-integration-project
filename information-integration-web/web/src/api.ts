export class Api {
    base: string;

    constructor(baseUrl: string = "api") {
        this.base = baseUrl;
    }

    async allTitles(this: Api): Promise<Array<any>> {
        return fetch(`${this.base}/titles/`, {
            method: 'GET',
        }).then(response => {
            if (response.ok) {
                return response.json() as unknown as Array<any>;
            } else {
                throw "Response was not OK";
            }
        });
    }
}

export default new Api()
