import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Api from './api.js';

class Messenger extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            conversations: null,
            messages: null,
            currentConversationId: 0,
            newConversationActive: false,
        };
    }

    async componentDidMount() {
        const conversations = await Api.getConversations();

        const newState = Object.assign({}, this.state, {conversations: conversations.data});
        this.setState(newState);
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
            user: {
                id: 0,
                name: 'me'
            }
        };

        const newState = Object.assign({}, this.state);
        newState.messages.push(fakeMessage);
        this.setState(newState);

        await Api.sendMessage(this.state.currentConversationId, body);
    }

    async handleNewConversation(title) {
        await Api.newConversation(this.state.currentConversationId, title);

        const newState = Object.assign({}, this.state, {newConversationActive: false});
        this.setState(newState);
    }

    activateNewConversation() {
        const newState = Object.assign({}, this.state, {newConversationActive: true});
        this.setState(newState);
    }

    render() {
        return (
            <div className="messenger">
                <ConversationsList conversations={this.state.conversations}
                                   handleSelectConversation={(id) => this.handleSelectConversation(id)}
                                   currentConversationId={this.state.currentConversationId}
                                   activateNewConversation={() => this.activateNewConversation()}
                />
                <MessagesList messages={this.state.messages}/>
                <InputMessage handleSend={(body) => this.handleSend(body)} messages={this.state.messages}/>
                <NewConversationDialog handleNewConversation={(title) => this.handleNewConversation(title)}
                                       active={this.state.newConversationActive}
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
                    <span onClick={this.props.activateNewConversation}>Создать беседу</span>
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
                <span className="last-message">{c.last_message.user.name}: {c.last_message.body}</span>
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
        if (this.props.messages != null) {
            messages = this.props.messages.map((message) =>
                <Message key={message.id.toString()}
                         message={message}
                />
            );
        }
        return (
            <ul className="messages-list">
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
            <div className="username">{props.message.user.name}</div>
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

    render() {
        const hiddenClass = this.props.active ? '' : 'hidden';

        return (
            <div className={"new-conversation-container " + hiddenClass}>
                <div className="new-conversation">
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
