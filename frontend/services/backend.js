export class Client {
	name = "travel_salesman"
	base_uri = "http://127.0.0.1:5000/api/"
	methods_with_body = ["POST", "PATCH", "PUT"]

	setAuthToken(access_token, refresh_token) {
		localStorage.setItem(`${this.name}-access-token`, access_token);
		localStorage.setItem(`${this.name}-refresh-token`, refresh_token);
	}
	getAuthHeader() {
		if(!this.getAccessToken())
			return {}
		return {
			Authorization: "Bearer " + this.getAccessToken()
		};
	}
	getAccessToken() {
		return localStorage.getItem(`${this.name}-access-token`) || ""
	}
	getTokenPair() {
		return {
			access: localStorage.getItem(`${this.name}-access-token`) || "",
			refresh: localStorage.getItem(`${this.name}-refresh-token`) || "",
		}
	}

	removeAuthToken() {
		localStorage.removeItem(`${this.name}-access-token`);
		localStorage.removeItem(`${this.name}-refresh-token`);
	}
	defaultHeaders() {
		return {
			'Content-Type': 'application/json'
		}
	}

	async call(method, path, body = {}, headers = {}) {

		const url = this.base_uri + path;
		headers = {
			...this.defaultHeaders(),
			...headers,
			...this.getAuthHeader()
		};
		body = this.methods_with_body.includes(method) ? {medataType: 'json', data: JSON.stringify(body)} : {}
		return await $.ajax({
			url: url,
			headers: headers,
			method: method,
			...body,
			error : function (request, status, error) {
				console.log(request)
				alert(Object.values(request.responseJSON)[0]);
			}
		});
	}
	async post(path, body) {
		return await this.call("POST", path, body);
	}
	async get(path) {
		return await this.call("GET", path);
	}
}
export class Backend {
	static client = new Client();

	static uri() {
		return this.client.base_uri
	}

	static async solver_nearest(points, delay) {
		return await this.client.post("v1/solver/nearest/", {points: points, delay: delay});
	}

	static async log_in(username, password) {
		try {
			const response = await this.client.post("token/", {username: username, password: password});
			this.client.setAuthToken(response["access"], response["refresh"]);
			return true;
		}
		catch (e) {
			console.log(e);
			return false;
		}
	}
	static async log_out() {
		// await this.client.post("token/blacklist/",
		// 	this.client.getTokenPair());
		this.client.removeAuthToken();
	}
	static async sing_up(username, password, confirmed_password) {
		try {
			this.client.removeAuthToken();
			const response = await this.client.post("v1/users/signup/",
				{username: username, password: password, confirmed_password: confirmed_password});

			console.log(response)
			this.client.setAuthToken(response["access"]);
			return true;
		}
		catch (e) {
			console.log(e);
			return false;
		}
	}
	static async is_logged() {
		try {
			await this.client.get("v1/users/is_logged/");
			return true;
		}
		catch (e) {
			return false;
		}
	}
	static async get_history() {
		return await this.client.get("v1/history/");
	}
	static async get_worker() {
		return await this.client.get("worker/");
	}
	static async record_history(path, length) {
		return await this.client.post("v1/history/", {"path": path, "length": length});
	}
}
