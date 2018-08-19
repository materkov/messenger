import axios from 'axios';

class Api {
    constructor() {
        this.instance = axios.create({
            baseURL: 'http://localhost:5000',
            timeout: 15000,
        });

    }

    setToken(token) {
        this.instance = axios.create({
            baseURL: 'http://localhost:5000',
            timeout: 15000,
            headers: {'Authorization': 'Bearer ' + token}
        });
    }

    async getConversations() {
        try {
            return await this.instance.get('/conversations');
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async getMessages(id) {
        try {
            return await this.instance.get('/conversations/' + id.toString() + "/messages");
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async sendMessage(conversationId, body) {
        try {
            return await this.instance.post('/conversations/' + conversationId.toString() + "/write", {body: body});
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async newConversation(title) {
        try {
            const data = await this.instance.post('/conversations', {title: title, user_ids: []});
            return data.data.id;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async login(login, password) {
        try {
            const data = await this.instance.post('/login', {login: login, password: password});
            return data.data;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async register(login, name, password) {
        try {
            const data = await this.instance.post('/register', {login: login, name: name, password: password});
            return data.data;
        } catch (error) {
            console.error(error);
            return null;
        }
    }
}

export default new Api();
