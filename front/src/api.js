import axios from 'axios';

class Api {
    constructor() {
        this.instance = axios.create({
            baseURL: 'http://localhost:5000',
            timeout: 15000,
            headers: {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxNjMifQ.44pGOdE7_Wqvtk4uDt4BMo03U3wfWRSLqd_Yg9nQYKo'}
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
            const data = await this.instance.post('/conversations', {title: title, user_ids: [163]});
            return data.data.id;
        } catch (error) {
            console.error(error);
            return null;
        }
    }
}

export default new Api();
