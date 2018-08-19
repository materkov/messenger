import React, {Component} from 'react';
import './login.css';
import Api from './api.js';

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            login: '',
            password: '',
            isRegistration: false,
        };

        this.handleClick = this.handleClick.bind(this);
        this.handleLoginChange = this.handleLoginChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleModeClick = this.handleModeClick.bind(this);
    }

    componentDidMount() {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user'));
        if (token && user) {
            this.props.handleOnLogin(token, user);
        }
    }

    async handleClick() {
        if (this.state.isRegistration) {
            const result = await Api.register(this.state.login, this.state.login, this.state.password);
            if (result) {
                localStorage.setItem('token', result.token);
                localStorage.setItem('user', JSON.stringify(result.user));

                this.props.handleOnLogin(result.token, result.user);
            }
        } else {
            const result = await Api.login(this.state.login, this.state.password);

            localStorage.setItem('token', result.token);
            localStorage.setItem('user', JSON.stringify(result.user));

            this.props.handleOnLogin(result.token, result.user);
        }
    }

    handleLoginChange(event) {
        this.setState({login: event.target.value});
    }

    handlePasswordChange(event) {
        this.setState({password: event.target.value});
    }

    handleModeClick(event) {
        event.preventDefault();
        this.setState({isRegistration: !this.state.isRegistration});
    }

    render() {
        let label = (<span>Введите логин и пароль. <a href="" onClick={this.handleModeClick}>Регистрация</a></span>);
        let btnLabel = 'Войти';
        if (this.state.isRegistration) {
            label = (<span>Регистрация. Введите желаемый логин и пароль. <a href=""
                                                                            onClick={this.handleModeClick}>Вход</a></span>);
            btnLabel = 'Зарегистрироваться';
        }

        return (
            <div className={"login " + (this.props.isAuthorized ? 'hidden' : '')}>
                <div className="login-box">
                    {label}<br/>
                    <input type="text" value={this.state.login} onChange={this.handleLoginChange}/><br/>
                    <input type="password" value={this.state.password} onChange={this.handlePasswordChange}/><br/>
                    <input type="button" value={btnLabel} onClick={this.handleClick}/>
                </div>
            </div>
        )
    }
}

export default Login;
