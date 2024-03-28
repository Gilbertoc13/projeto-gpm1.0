import React, { useState } from 'react';
import styles from './CadastroLogin.module.css';
import Logo from '../../assets/icon.png';
import { Link } from 'react-router-dom';

function CadastroLogin() {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [username, setUsername] = useState('');
    const [repetirSenha, setRepetirSenha] = useState('');
    const [isCadastro, setIsCadastro] = useState(false);

    const handleEmailChange = (event) => setEmail(event.target.value);
    const handleSenhaChange = (event) => setSenha(event.target.value);
    const handleUsernameChange = (event) => setUsername(event.target.value);
    const handleRepetirSenhaChange = (event) => setRepetirSenha(event.target.value);

    const handleSubmit = (event) => {
        event.preventDefault();
        if (isCadastro) console.log('cadastro:');
        else console.log('login:');
        console.log('Email:', email);
        console.log('Senha:', senha);
        console.log('Nome de usuário:', username);
        console.log('Repetir Senha:', repetirSenha);
    };

    const handleToggleCadastro = () => setIsCadastro(!isCadastro);

    return (
        <div className={styles.divLogin}>
            <Link to={'/'} style={{width: '100%'}}>
                <img src={Logo} alt="Logo" />
            </Link>
            <h1>Bem-Vindo!</h1>
            <p>{isCadastro ? 'Já possui uma conta?' : 'Novo por aqui?'}{' '}<span onClick={handleToggleCadastro}> {isCadastro ? 'Entrar' : 'Crie uma conta'} </span></p>
            <form onSubmit={handleSubmit}>
                {isCadastro && (
                    <input
                        type="text"
                        placeholder="Nome de usuário"
                        value={username}
                        onChange={handleUsernameChange}
                    />
                )}
                <input
                    type="text"
                    placeholder="Email"
                    value={email}
                    onChange={handleEmailChange}
                />
                <input
                    type="password"
                    placeholder="Senha"
                    value={senha}
                    onChange={handleSenhaChange}
                />
                {isCadastro && (
                    <input
                        type="password"
                        placeholder="Repetir senha"
                        value={repetirSenha}
                        onChange={handleRepetirSenhaChange}
                    />
                )}
                <button type="submit">
                    {isCadastro ? 'Cadastrar' : 'Entrar'}
                </button>
                <h3 className={styles.ajudaLogin}>Problemas com login?</h3>
            </form>
        </div>
    );
}

export default CadastroLogin;
