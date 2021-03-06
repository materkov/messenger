import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Api from './api.js';
import Login from './login.js';

class Messenger extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            conversations: null,
            messages: null,
            currentConversationId: 0,
            newConversationActive: false,
            authToken: '',
            user: null,
        };
    }

    async handleSelectConversation(id) {
        const messages = await Api.getMessages(id);

        const newState = Object.assign({}, this.state, {
            messages: messages.data.reverse(),
            currentConversationId: id,
        });
        this.setState(newState);
    }

    async handleSend(body) {
        const fakeMessage = {
            id: Math.random() * 2000000000,
            type: 'normal',
            body: body,
            user: this.state.user,
            date: (new Date()).toISOString(),
        };

        const newState = Object.assign({}, this.state);
        newState.messages.push(fakeMessage);
        this.setState(newState);

        await Api.sendMessage(this.state.currentConversationId, body);
    }

    async handleNewConversation(title) {
        const conversationId = await Api.newConversation(title);
        console.log(conversationId);
        const fakeConversation = {
            "id": conversationId,
            "title": title,
            "users": [this.state.user],
            "last_message": {
                "id": Math.random() * 1000000000,
                "type": "conversation_created",
                "body": "",
                "user": this.state.user,
            }
        };

        let newState = Object.assign({}, this.state, {newConversationActive: false});
        newState.conversations.unshift(fakeConversation);
        this.setState(newState);
    }

    toggleNewConversation() {
        const newState = Object.assign({}, this.state, {newConversationActive: !this.state.newConversationActive});
        this.setState(newState);
    }

    async handleLogin(authToken, user) {
        this.setState({authToken: authToken, user: user});
        Api.setToken(authToken);

        const conversations = await Api.getConversations();

        const newState = Object.assign({}, this.state, {conversations: conversations.data});
        this.setState(newState);
    }

    render() {
        return (
            <div className="messenger">
                <ConversationsList conversations={this.state.conversations}
                                   handleSelectConversation={(id) => this.handleSelectConversation(id)}
                                   currentConversationId={this.state.currentConversationId}
                                   toggleNewConversation={() => this.toggleNewConversation()}
                />
                <MessagesList messages={this.state.messages}/>
                <InputMessage handleSend={(body) => this.handleSend(body)} messages={this.state.messages}/>
                <NewConversationDialog handleNewConversation={(title) => this.handleNewConversation(title)}
                                       active={this.state.newConversationActive}
                                       toggleNewConversation={() => this.toggleNewConversation()}
                />
                <Login handleOnLogin={(authToken, user) => this.handleLogin(authToken, user)}
                       isAuthorized={this.state.authToken}
                />
            </div>
        )
    }
}

class ConversationsList extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let conversations = '';
        if (this.props.conversations !== null) {
            conversations = this.props.conversations.map((conversation) =>
                <Conversation key={conversation.id.toString()}
                              conversation={conversation}
                              handleSelectConversation={(id) => this.props.handleSelectConversation(id)}
                              currentConversationId={this.props.currentConversationId}
                />
            );
        }

        return (
            <ul className="conversations-list">
                <li className="conversations-top-panel">
                    <span onClick={this.props.toggleNewConversation}>Создать беседу</span>
                </li>

                {conversations}
            </ul>
        )
    }
}

class Conversation extends React.Component {
    render() {
        const c = this.props.conversation;
        const isActive = this.props.currentConversationId === c.id ? 'active' : '';

        return (
            <li className={"conversation " + isActive} onClick={() => this.props.handleSelectConversation(c.id)}>
                <div className="title">{c.title}</div>
                <div className="last-message">
                    <span className="last-message-user">{c.last_message.user.name}:</span>
                    <span className="last-message-body"> {c.last_message.body}</span>
                </div>
            </li>
        )
    }
}

class MessagesList extends Component {
    scrollToBottom() {
        this.messagesEnd.scrollIntoView();
    }

    componentDidMount() {
        this.scrollToBottom();
    }

    componentDidUpdate() {
        this.scrollToBottom();
    }

    render() {
        let messages = '';
        let zeroData = '';

        if (this.props.messages != null) {
            messages = this.props.messages.map((message) =>
                <Message key={message.id.toString()}
                         message={message}
                />
            );
        } else {
            zeroData = (<div className="zero-data"> ← Выберите диалог </div>);
        }

        return (
            <ul className="messages-list">
                {zeroData}
                {messages}
                <div ref={(el) => {
                    this.messagesEnd = el;
                }}/>
            </ul>
        )
    }
}

function Message(props) {
    switch (props.message.type) {
        case 'normal':
            return (<NormalMessage message={props.message}/>);
        case 'conversation_created':
            return (<ConversationCreatedMessage message={props.message}/>);
        case 'title_changed':
            return (<TitleChangedMessage message={props.message}/>);
        default:
            return (<li className="message"/>);
    }
}

function NormalMessage(props) {
    return (
        <li className="message">
            <div className="message-top-panel">
                <span className="username">{props.message.user.name}</span>
                <span className="date">{(new Date(props.message.date)).toLocaleString()}</span>
            </div>
            {props.message.body}
        </li>
    )
}

function ConversationCreatedMessage(props) {
    return (
        <li className="message service-message">
            Пользователь <span className="service-message-user">{props.message.user.name}</span> создал беседу
        </li>
    )
}

function TitleChangedMessage(props) {
    return (
        <li className="message service-message">
            Пользователь <span className="service-message-user">{props.message.user.name}</span> сменил название беседы
            на <span className="service-message-new-title">{props.message.title}</span>
        </li>
    )
}

class InputMessage extends Component {
    constructor(props) {
        super(props);
        this.state = {body: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
    }

    handleChange(event) {
        this.setState({body: event.target.value});
    }

    handleClick() {
        if (!this.state.body) {
            return;
        }

        this.props.handleSend(this.state.body);
        this.setState({body: ''});
    }

    handleKeyPress(event) {
        if (event.key === 'Enter') {
            this.handleClick();
            event.preventDefault();
        }
    }

    render() {
        if (this.props.messages === null) {
            return (<div className="messages-input empty"/>);
        }

        return (
            <div className="messages-input">
                <textarea value={this.state.body} onChange={this.handleChange} onKeyPress={this.handleKeyPress}/>
                <input type="button" value="Отправить" className="message-send" onClick={this.handleClick}/>
            </div>
        )
    }
}

class NewConversationDialog extends Component {
    constructor(props) {
        super(props);
        this.state = {title: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleContainerClick = this.handleContainerClick.bind(this);
    }

    handleChange(event) {
        this.setState({title: event.target.value});
    }

    handleClick() {
        if (!this.state.title) {
            return;
        }

        this.props.handleNewConversation(this.state.title);
        this.setState({title: ''});
    }

    handleContainerClick(event) {
        event.stopPropagation();
    }

    render() {
        const hiddenClass = this.props.active ? '' : 'hidden';

        return (
            <div className={"new-conversation-container " + hiddenClass}
                 onClick={() => this.props.toggleNewConversation()}>
                <div className="new-conversation" onClick={this.handleContainerClick}>
                    Введите имя беседы:<br/>
                    <input type="text" value={this.state.title} onChange={this.handleChange}/><br/>
                    <input type="button" value="Создать" onClick={this.handleClick}/>
                </div>
            </div>
        )
    }
}

// ========================================

ReactDOM.render(
    <Messenger/>,
    document.getElementById('root')
);
